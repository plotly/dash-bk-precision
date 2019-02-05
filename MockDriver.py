from driver import GenericPSUDriver
import os
import numpy as np
import redis


class MockPSUDriver(object):
    """ Mock driver to be used without the instrument """
    # properties
    MIN_VOLTS = 0  # Volts
    MAX_VOLTS = 18  # Volts
    DEFAULT_VOLTS = 12  # Volts

    MIN_CURRENT = 0  # Amps
    MAX_CURRENT = 5  # Amps

    DEFAULT_RESISTANCE = 500  # Ohms

    def __init__(self, output_noise_mean, output_noise_std_dev):
        self.output_noise = lambda: output_noise_std_dev * np.random.randn() + output_noise_mean
        self.voltage_setting = self.DEFAULT_VOLTS
        self.state = False
        self.max_output_current_setting = self.MAX_CURRENT
        self.max_output_voltage_setting = self.MAX_VOLTS
        self.resistance = self.DEFAULT_RESISTANCE
        self.r = redis.StrictRedis.from_url(os.environ['REDIS_URL'])
        self.__set_redis_defautlts()

    def __set_redis_defautlts(self):
        self.voltage_setting = self.r.set('volts', self.voltage_setting)
        self.state = self.r.set('state', self.max_output_current_setting)
        self.resistance = self.r.set('resistance', self.resistance)
        self.max_output_current_setting = self.r.set(
            'max_curr', self.max_output_current_setting)
        self.max_output_voltage_setting = self.r.set(
            'max_volts', self.max_output_voltage_setting)

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

    def set_control(self, control):
        """
        Not used in mock driver.
        """
        pass

    def set_state(self, state):
        """
        Sets the output state
        Args:
            state: Boolean with True for ON and False for OFF.
        Returns:
            True on success
        """
        self.state = state
        self.r.set('state', state)
        return True

    def set_max_output_voltage(self, volts):
        """
        Set the maximum output voltage to a given value.
        Args:
            volts: Voltage to set.
        Returns:
            Boolean indicating success
        """
        curr_volts = float(self.r.get('volts'))
        if volts > self.MAX_VOLTS:
            raise ValueError(
                "This power supply cannot supply more than {}V!".format(
                    self.MAX_VOLTS))
        elif volts < curr_volts:
            raise ValueError(
                "Cannot set max voltage lower than the current voltage {}V!".
                format(curr_volts))

        self.max_output_voltage_setting = volts
        self.r.set('max_volts', volts)
        return True

    def set_max_output_current(self, curr):
        """
        Set the maximum output current to a given value.
        Args:
            curr: Current to set.
        Returns:
            Boolean indicating success
        """
        if curr > self.MAX_CURRENT or curr < self.MIN_CURRENT:
            raise ValueError(
                "This power supply cannot supply more than {}A!".format(
                    self.MAX_CURRENT))

        self.max_output_current_setting = curr
        self.r.set('max_curr', curr)
        return True

    def set_output_voltage(self, volts):
        """
        Set the output voltage to the given value.
        Args:
            volts: floating pointer value between 0 and 18.
        Returns:
            Boolean indicating success
        """
        max_volts = float(self.r.get('max_volts'))
        if volts > max_volts or volts < self.MIN_VOLTS:
            raise ValueError(
                "The maximum output voltage is {}V!".format(max_volts))

        self.voltage_setting = volts
        self.r.set('volts', volts)
        return True

    def set_output_current(self, curr):
        """
        Set the maximum current output of the power supply.
        Args:
            curr: The maximum current to set.
        Returns:
            Boolean indicating success.
        """
        if curr > self.MAX_CURRENT or curr < self.MIN_CURRENT:
            raise ValueError("Invalid Current")

        self.max_output_current_setting = curr
        self.r.set('max_curr', curr)
        return True

    def set_load(self, resistance):
        """
        Sets a load resistance.
        Args:
            resistance: Resistance to use
        """
        self.resistance = resistance
        self.r.set('resistance', resistance)

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
        self.voltage_setting = float(self.r.get('volts'))
        self.state = self.r.get('state') == b"True"
        self.resistance = float(self.r.get('resistance'))
        self.max_output_current_setting = float(self.r.get('max_curr'))
        self.max_output_voltage_setting = float(self.r.get('max_volts'))

        current = abs(self.output_noise()) + (
            self.voltage_setting / self.resistance) if self.state else 0
        voltage = abs(
            self.output_noise()) + (self.voltage_setting) if self.state else 0
        output = {
            "output_current": current,
            "output_voltage": voltage,
            "state": self.state,
            "voltage_value_setting": self.voltage_setting,
            "maximum_current_setting": self.max_output_current_setting,
            "maximum_voltage_setting": self.max_output_voltage_setting
        }
        return output
