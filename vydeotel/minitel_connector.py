from serial import Serial
from connector import Connector


class MinitelConnector(Connector):
    def __init__(self, port: str, speed: int):
        super(MinitelConnector, self).__init__()
        self.serial = Serial(port, speed, timeout=0.1)

    def write(self, data: bytes) -> None:
        self.serial.write(data)

    def readable(self) -> bool:
        return self.serial.readable()

    def read(self) -> bytes:
        return self.serial.read()

    def set_baudrate(self, baudrate: int) -> None:
        self.serial.baudrate = baudrate
