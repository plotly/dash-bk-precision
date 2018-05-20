from abc import ABCMeta, abstractmethod


class GenericPSUDriver(ABCMeta):
    @abstractmethod
    def set_control(self, control):
        raise NotImplementedError

    @abstractmethod
    def set_state(self, state):
        raise NotImplementedError

    @abstractmethod
    def set_max_output(self, volts):
        raise NotImplementedError

    @abstractmethod
    def set_output_voltage(self, volts):
        raise NotImplementedError

    @abstractmethod
    def set_output_current(self, current):
        raise NotImplementedError

    @abstractmethod
    def read_supply_values(self):
        raise NotImplementedError
