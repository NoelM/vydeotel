from socket import socket
from serial import Serial
from vydeotel.utils import bit_read, write_byte
from vydeotel.consts import ESC, US, PROG, START, STOP, ROULEAU
from time import sleep


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

    def _read_byte(self):
        byte = self.read()

        even = False
        for i in range(7):
            if bit_read(byte, i) == 1:
                even = not even

        if even == bit_read(byte, 7):
            if bit_read(byte, 7) == 1:
                byte = byte ^ (1 << 7)
            return byte
        else:
            return 0xFF

    def get_cursor_xy(self):
        buf = bytes()
        buf += write_byte(ESC)
        buf += write_byte(0x61)
        self.write(buf)

        while not self.readable():
            continue

        trame = 0
        while trame >> 16 != US:
            trame = (trame << 8) + self._read_byte()

        return trame

    def working_mode(self):
        while not self.readable():
            continue

        trame = 0
        while trame >> 8 != 0x1B3A73:  # PRO2, REP_STATUS_FCT
            if self.readable():
                trame = (trame << 8) + self._read_byte()

        return trame

    def page_mode(self):
        self.write_bytes_pro(2)
        self.write_byte_buffer(STOP)
        self.write_byte_buffer(ROULEAU)

        return self.working_mode()

    def scroll_mode(self):
        self.write_bytes_pro(2)
        self.write_byte_buffer(START)
        self.write_byte_buffer(ROULEAU)

        return self.working_mode()

    def change_speed(self, bauds):
        self.write_bytes_pro(2)
        self.write_byte(PROG)

        if bauds == 300:
            self.write_byte(0b1010010)
            self.conn.baudrate = 300
        elif bauds == 1200:
            self.write_byte(0b1100100)
            self.conn.baudrate = 1200
        elif bauds == 4800:
            self.write_byte(0b1110110)
            self.conn.baudrate = 4800
        elif bauds == 9600:
            self.write_byte(0b1111111)
            self.conn.baudrate = 9600

        # TODO: respect the C implem
        return bauds

    def get_key_code(self):
        code = 0

        if self.readable():
            code = self._read_byte()

        if code == 0x19:
            while not self.readable():
                continue
            code = (code << 8) + self._read_byte()
            if code == 0x1923:
                code = 0xA3
            elif code == 0x1927:
                code = 0xA7
            elif code == 0x1930:
                code = 0xB0
            elif code == 0x1931:
                code = 0xB1
            elif code == 0x1938:
                code = 0xF7
            elif code == 0x197B:
                code = 0xDF
        elif code == 0x13:
            while not self.readable():
                continue
            code = (code << 8) + self._read_byte()
        elif code == 0x1B:
            sleep(0.02)
            if self.readable():
                code = (code << 8) + self._read_byte()
                if code == 0x1B5B:
                    while not self.readable():
                        continue
                    code = (code << 8) + self._read_byte()
                    if code == 0x1B5B34 or code == 0x1B5B32:
                        while not self.readable():
                            continue
                        code = (code << 8) + self._read_byte()

        return code


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
