from re import S
import time

import serial
import asyncio
from struct import pack

from consts import *
from utils import *


class Minitel:
    def __init__(self, port, write_parity=True, read_parity=True):
        self.serial = serial.Serial(port, 1200, timeout=1000)
        self.current_size = GRANDEUR_NORMALE

        self.write_parity = write_parity
        self.read_parity = read_parity

    def set_window(self, w: Window):
        self.window = w

    def write_byte(self, byte: int):
        if self.write_parity:
            even = False
            for i in range(7):
                if bit_read(byte, i) == 1:
                    even = not even

            if even:
                byte = bit_write(byte, 7, 1)
            else:
                byte = bit_write(byte, 7, 0)

        self.serial.write(pack("B", byte))

    def write_word(self, word):
        self.write_byte(high_byte(word))
        self.write_byte(low_byte(word))

    def read_byte(self):
        byte = self.serial.read(1)
        byte = byte[0]  # keep only the first byte

        if not self.read_parity:
            return byte

        even = False
        for i in range(7):
            if bit_read(byte, i) == 1:
                even = not even

        if even == bit_read(byte, 7):
            if bit_read(byte, 7) == 1:
                byte = byte ^ (1 << 7)
            return byte
        else:
            return 0xff

    def write_bytes_pro(self, n):
        self.write_byte(ESC)
        if n == 1:
            self.write_byte(0x39)
        elif n == 2:
            self.write_byte(0x3A)
        elif n == 3:
            self.write_byte(0x3B)

    def write_byte_p(self, n):
        if n <= 9:
            self.write_byte(0x30 + n)
        else:
            self.write_byte(0x30 + n // 10)
            self.write_byte(0x30 + n % 10)

    def change_speed(self, bauds):
        self.write_bytes_pro(2)
        self.write_byte(PROG)

        if bauds == 300:
            self.write_byte(0b1010010)
            self.serial.baudrate = 300
        elif bauds == 1200:
            self.write_byte(0b1100100)
            self.serial.baudrate = 1200
        elif bauds == 4800:
            self.write_byte(0b1110110)
            self.serial.baudrate = 4800
        elif bauds == 9600:
            self.write_byte(0b1111111)
            self.serial.baudrate = 9600

        # TODO: respect the C implem
        return bauds

    def set_attribute(self, attribute):
        self.write_byte(ESC)
        self.write_byte(attribute)
        if attribute == DOUBLE_HAUTEUR or attribute == DOUBLE_HAUTEUR:
            self.move_cursor_down(1)
            self.current_size = attribute
        elif attribute == GRANDEUR_NORMALE or attribute == DOUBLE_LARGEUR:
            self.current_size = attribute

    def move_cursor_xy(self, x, y):
        self.write_word(CSI)
        self.write_byte_p(y)
        self.write_byte(0x3B)
        self.write_byte_p(x)
        self.write_byte(0x48)

    def move_cursor_left(self, n):
        if n == 1:
            self.write_byte(BS)
        else:
            self.write_word(CSI)
            self.write_byte_p(n)
            self.write_byte(0x44)

    def move_cursor_right(self, n):
        if n == 1:
            self.write_byte(HT)
        else:
            self.write_word(CSI)
            self.write_byte_p(n)
            self.write_byte(0x43)

    def move_cursor_down(self, n):
        if n == 1:
            self.write_byte(LF)
        else:
            self.write_word(CSI)
            self.write_byte_p(n)
            self.write_byte(0x42)

    def move_cursor_up(self, n):
        if n == 1:
            self.write_byte(VT)
        else:
            self.write_word(CSI)
            self.write_byte_p(n)
            self.write_byte(0x41)

    def move_cursor_return(self, n):
        self.write_byte(CR)
        self.move_cursor_down(n)

    def clear_screen_from_cursor(self):
        self.write_word(CSI)
        self.write_byte(0x4A)

    def clear_screen_to_cursor(self):
        self.write_word(CSI)
        self.write_byte(0x31)
        self.write_byte(0x4A)

    def clean_screen(self):
        self.write_word(CSI)
        self.write_byte(0x32)
        self.write_byte(0x4A)

    def clear_line_from_cursor(self):
        self.write_word(CSI)
        self.write_byte(0x4B)

    def clear_line_to_cursor(self):
        self.write_word(CSI)
        self.write_byte(0x31)
        self.write_byte(0x4B)

    def clear_line(self):
        self.write_word(CSI)
        self.write_byte(0x32)
        self.write_byte(0x4B)

    def print(self, msg):
        # TODO: add diacritic support
        for c in msg:
            self.print_char(c)

    def println(self, msg):
        if msg != "":
            self.print(msg)

        if self.current_size == DOUBLE_HAUTEUR or self.current_size == DOUBLE_GRANDEUR:
            self.move_cursor_return(2)
        else:
            self.move_cursor_return(1)

    def print_char(self, char):
        char_byte = get_char_byte(char)
        if is_valid_char(char_byte):
            self.write_byte(char_byte)

    def new_screen(self):
        self.write_byte(FF)
        self.current_size = GRANDEUR_NORMALE

    def graphic_mode(self):
        self.write_byte(SO)

    def graphic_at(self, byte, x, y):
        self.move_cursor_xy(x, y)
        self.graphic(byte)

    def graphic(self, byte):
        if byte <= 0b111111:
            byte = (0x20 +
                    bit_read(byte, 5) +
                    bit_read(byte, 4) * 2 +
                    bit_read(byte, 3) * 4 +
                    bit_read(byte, 2) * 8 +
                    bit_read(byte, 1) * 16 +
                    bit_read(byte, 0) * 64
                    )
            if byte == 0x7F:
                byte = 0x5F

            self.write_byte(byte)

    def repeat(self, n):
        self.write_byte(REP)
        self.write_byte(0x40 + n)

    def text_mode(self):
        self.write_byte(SI)

    def h_line(self, x1, y, x2, pos):
        self.text_mode()
        self.move_cursor_xy(x1, y)

        if pos == TOP:
            self.write_byte(0x7E)
        elif pos == CENTER:
            self.write_byte(0x60)
        elif pos == BOTTOM:
            self.write_byte(0x5F)

        self.repeat(x2-x1)

    def v_line(self, x, y1, y2, pos, direction):
        self.text_mode()
        if direction == DOWN:
            self.move_cursor_xy(x, y1)
        elif direction == UP:
            self.move_cursor_xy(x, y2)

        for i in range(y2-y1):
            if pos == LEFT:
                self.write_byte(0x7B)
            elif pos == CENTER:
                self.write_byte(0x7C)
            elif pos == RIGHT:
                self.write_byte(0x7D)

            if direction == DOWN:
                self.move_cursor_left(1)
                self.move_cursor_down(1)
            elif direction == UP:
                self.move_cursor_left(1)
                self.move_cursor_up(1)

    def page_mode(self):
        self.write_bytes_pro(2)
        self.write_byte(STOP)
        self.write_byte(ROULEAU)

        return self.working_mode()

    def scroll_mode(self):
        self.write_bytes_pro(2)
        self.write_byte(START)
        self.write_byte(ROULEAU)

        return self.working_mode()

    def working_mode(self):
        while not self.serial.readable():
            continue

        trame = 0
        while trame >> 8 != 0x1B3A73:  # PRO2, REP_STATUS_FCT
            if self.serial.readable():
                trame = (trame << 8) + self.read_byte()

        return trame

    def cursor(self):
        self.write_byte(CON)

    def no_cursor(self):
        self.write_byte(COFF)

    def new_xy(self, i, j):
        if i == 1 and j == 1:
            self.write_byte(RS)
        else:
            self.write_byte(US)
            self.write_byte(0x40 + i)
            self.write_byte(0x40 + j)

    def get_cursor_xy(self):
        self.write_byte(ESC)
        self.write_byte(0x61)

        while not self.serial.readable():
            continue

        trame = 0
        while trame >> 16 != US:
            trame = (trame << 8) + self.read_byte()

        return trame

    def get_key_code(self):
        code = 0

        if self.serial.readable():
            code = self.read_byte()

        if code == 0x19:
            while not self.serial.readable():
                continue
            code = (code << 8) + self.read_byte()
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
            while not self.serial.readable():
                continue
            code = (code << 8) + self.read_byte()
        elif code == 0x1B:
            time.sleep(0.02)
            if self.serial.readable():
                code = (code << 8) + self.read_byte()
                if code == 0x1B5B:
                    while not self.serial.readable():
                        continue
                    code = (code << 8) + self.read_byte()
                    if code == 0x1B5B34 or code == 0x1B5B32:
                        while not self.serial.readable():
                            continue
                        code = (code << 8) + self.read_byte()

        return code

    async def event_loop(self):
        new_window = None
        while True:
            if new_window is not None:
                new_window.set_minitel(self)
                new_window.set_prev_window(self.window)
                self.window = window

            key = self.get_key_code()
            if key == ENVOI:
                new_window = self.window.envoi()
            elif key == ANNULATION:
                new_window = self.window.annulation()
            elif key == REPETITION:
                new_window = self.window.repetition()
            elif key == CORRECTION:
                new_window = self.window.correction()
            elif key == SOMMAIRE:
                new_window = self.window.sommaire()
            elif key == RETOUR:
                new_window = self.window.retour()
            elif key == GUIDE:
                new_window = self.window.guide()
            elif key == SUITE:
                new_window = self.window.suite()
            else:
                self.window.new_key(key)

        def start(self):
            asyncio.get_event_loop().run_until_end(self.event_loop())
            asyncio.get_event_loop().run_forever()


class Window:
    def __init__(self, x: int, y: int, width: int, height: int, border = False, fg = CARACTERE_BLANC, bg = FOND_NORMAL, typo = GRANDEUR_NORMALE):
        self.buffer = ""

        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.border = border

        self.fg = fg
        self.bg = bg
        self.typo = typo
        
        self.prev_window = None
        self.next_window = None

    def set_minitel(self, m: Minitel) -> None:
        self.m = m

    def set_prev_window(self, w: Window) -> None:
        self.prev_window = w

    def set_next_window(self, w: Window) -> None:
        self.next_window = w
    
    def default_style(self) -> None:
        self.m.set_attribute(self.typo)
        self.m.set_attribute(self.fg)
        self.m.set_attribute(self.bg)

    def draw(self) -> None:
        self.m.clean_screen()
        self.m.move_cursor_xy(self.x, self.y)
        self.default_style()

    def new_key(self, key: int):
        self.buffer += chr(key)

    def envoi(self) -> Window:
        pass

    def annulation(self) -> Window:
        pass

    def correction(self) -> Window:
        pass

    def repetition(self) -> Window:
        pass

    def sommaire(self) -> Window:
        pass

    def retour(self) -> Window:
        return self.prev_window

    def guide(self) -> Window:
        pass

    def suite(self) -> Window:
        return self.next_window
