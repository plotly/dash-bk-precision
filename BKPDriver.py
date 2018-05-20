import serial
import logging
import struct
import time
from threading import Lock

from driver import GenericPSUDriver
import numpy as np


class SyncBKPDriver(object):
    """ Thread safe synchronous driver for the BKP Precision PSU """

    # Status codes:
    CHECKSUM_INCORRECT = 0x90
    PARAM_INCORRECT = 0xA0
    UNRECOGNIZED = 0xB0
    INVALID_CMD = 0xC0
    SUCCESS = 0x80

    # properties
    MIN_VOLTS = 0
    MAX_VOLTS = 18
    MIN_CURRENT = 0
    MAX_CURRENT = 5

    def __init__(self, baudrate, dev_addr, serial_port=None):
        self.address = dev_addr
        self.baudrate = baudrate
        self.port = serial_port
        self.logger = logging.getLogger()
        self.controlling = False
        self.__serial_lock = Lock()

    def __check_crc(self, data, crc):
        s = sum(data) % 256
        return crc == s

    def __send(self, data, reply=False):
        with self.__serial_lock:
            with serial.Serial(self.port, self.baudrate) as ser:
                ser.write(data)
                reply_data = ser.read(26)
                return reply_data

    def __prepare_request(self, cmd, data_bytes, reply=False):
        request = np.zeros(26, dtype=np.uint8)
        request[0] = 0xAA
        request[1] = self.address
        request[2] = cmd
        for i, byte in enumerate(data_bytes):
            request[3 + i] = byte
        checksum = sum(request) % 256
        request[-1] = checksum
        msg = self.__send(bytearray(request))

        if not msg:
            raise IOError("Unable to send message")

        if not self.__check_crc(msg[:-1], msg[-1]):
            raise IOError("CRC check failed")

        if msg[3] == 0x12:  # Check for status msg
            statuscode = msg[4]
            if statuscode == SUCCESS:
                self.logger.debug("Request with cmd %d was successful", cmd)
            else:
                self.logger.warn(
                    "Request with cmd %d failed with error code %d", cmd,
                    statuscode)
            return statuscode == SUCCESS

        return msg

    def __enter__(self):
        self.set_control(True)
        return self

    def __exit__(self, *args):
        self.set_control(False)

    def __encode_float_value(self, val, fp=3):
        val_int = int(val * (10**fp))  # Convert to fixed point format.
        return struct.pack("<I", val_int)  # convert to little endian

    def __decode_to_float(self, val, fp=3):
        num = 0
        for i, byte in enumerate(val):
            num += byte << 8 * i
        return (float(num) / (10**fp))

    def set_control(self, control):
        """
        Sets the device to be controllable with remote session.
        Args:
            control: Boolean corresponding to the control status,
                     True for remote control, and False otherwise.
        Return:
            Boolean indication success.
        """
        cmd = 0x20  # Remote control mode
        data = [1 if control else 0]
        if self.__prepare_request(cmd, data, reply=False):
            self.controlling = True
            return True
        return False

    def set_state(self, state):
        """
        Sets the output state
        Args:
            state: Boolean with True for ON and False for OFF.
        Returns:
            True on success
        """
        # YA: Might be confusing with booleans for state and return.
        cmd = 0x21
        data = [1 if state else 0]

        if self.__prepare_request(cmd, data, reply=False):
            self.state = state
            return True

        return False

    def set_max_output_voltage(self, volts):
        """
        Set the maximum output voltage to a given value.
        Args:
            volts: Voltage to set.
        Returns:
            Boolean indicating success
        """
        if volts > self.MAX_VOLTS or volts < self.MIN_VOLTS:
            raise ValueError("Invalid voltage")
        cmd = 0x22
        return self.__prepare_request(
            cmd, self.__encode_float_value(volts), reply=False)

    def set_output_voltage(self, volts):
        """
        Set the output voltage to the given value.
        Args:
            volts: floating pointer value between 0 and 18.
        Returns:
            Boolean indicating success
        """
        if volts > self.MAX_VOLTS or volts < self.MIN_VOLTS:
            raise ValueError("Invalid voltage")
        cmd = 0x23
        return self.__prepare_request(
            cmd, self.__encode_float_value(volts), reply=False)

    def set_max_output_current(self, curr):
        """
        Set the maximum current output of the power supply.
        Args:
            curr: The maximum current to set.
        Returns:
            Boolean indicating success.
        """
        cmd = 0x24
        if curr > self.MAX_CURRENT or curr < self.MIN_CURRENT:
            raise ValueError("Invalid Current")
        return self.__prepare_request(
            cmd, self.__encode_float_value(curr), reply=False)

    def read_supply_values(self):
        """
        Reads a value dict from the power supply.
        Returns:
            A dict with the following:
                {
                    "output_current":xx.xx,
                    "output_voltage":xx.xx,
                    "state":boolean,
                    "voltage_value_setting":xx.xx,
                    "maximum_current_setting" : xx.xx,
                    "maximum_voltage_setting": xx.xx,
                }
        """
        cmd = 0x26
        reply = self.__prepare_request(cmd, [], reply=True)
        self.last_read_req = time.clock()
        self.last_reply = reply

        output = {
            "output_current": self.__decode_to_float(reply[3:5]),
            "output_voltage": self.__decode_to_float(reply[5:9]),
            "state": 1 == reply[9],
            "voltage_value_setting": self.__decode_to_float(reply[16:20]),
            "maximum_current_setting": self.__decode_to_float(reply[10:12]),
            "maximum_voltage_setting": self.__decode_to_float(reply[12:16]),
        }
        return output
