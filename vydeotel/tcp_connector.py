from connector import Connector
from socket import socket


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
