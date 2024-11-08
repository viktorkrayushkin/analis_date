from abc import ABC, abstractmethod


class AbstractDevice(ABC):
    transport = None
    config = None

    def __init__(self, transport, config):
        self.transport = transport
        self.config = config

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass


devclasses = {}


def register_deviceclass(name, dcls):
    if name in devclasses:
        raise Exception(f"Device {name} already registered")

    devclasses[name] = dcls


def get_deviceclass_by_name(name):
    return devclasses[name]
