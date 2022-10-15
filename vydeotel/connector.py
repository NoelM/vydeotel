from socket import socket
from serial import Serial


class Connector:
    def __init__(self):
        return

    def write(self, data: bytes) -> None:
        pass

    def readable(self) -> bool:
        pass

    def read(self) -> bytes:
        pass

    def set_baudrate(self, baudrate: int) -> None:
        pass


class TCPConnector(Connector):
    def __init__(self, socks: socket) -> None:
        super(TCPConnector, self).__init__()
        self.socks = socks
        self.socks.setblocking(True)
        self.buffer = b""

    def _load_in_buffer(self) -> None:
        buf = self.socks.recv(1024)

        if buf is not None:
            self.buffer += buf

    def write(self, data: bytes) -> None:
        self.socks.send(data)

    def readable(self) -> bool:
        if len(self.buffer) == 0:
            self._load_in_buffer()

        return len(self.buffer) != 0

    def read(self) -> bytes:
        if len(self.buffer) == 0:
            return None

        byte = self.buffer[0]
        self.buffer = self.buffer[1:]
        return byte


class SerialConnector(Connector):
    def __init__(self, port: str, speed: int):
        super(SerialConnector, self).__init__()
        self.serial = Serial(port, speed, timeout=0.1)

    def write(self, data: bytes) -> None:
        self.serial.write(data)

    def readable(self) -> bool:
        return self.serial.readable()

    def read(self) -> bytes:
        return self.serial.read()

    def set_baudrate(self, baudrate: int) -> None:
        self.serial.baudrate = baudrate
