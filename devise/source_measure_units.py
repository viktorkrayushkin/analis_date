from .base import AbstractDevice
from abc import abstractmethod


class SMU(AbstractDevice):

    def __init__(self, transport, config):
        super().__init__(transport, config)

    @abstractmethod
    def datasheet(self):
        pass

    @abstractmethod
    def set_voltage(self, channel, value, compliance):
        pass

    @abstractmethod
    def get_voltage(self, channel):
        pass

    @abstractmethod
    def set_current(self, channel, value, compliance):
        pass

    @abstractmethod
    def get_current(self, channel):
        pass

    @abstractmethod
    def enable(self, en, channel):
        pass

    @abstractmethod
    def trigger_in_mode(self, mode, channel):
        pass

    @abstractmethod
    def trigger(self):
        pass
