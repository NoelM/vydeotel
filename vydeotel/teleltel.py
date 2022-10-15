from copy import deepcopy
from vydeotel.utils import *
from vydeotel.consts import *
from vydeotel.connector import Connector


class Teletel:
    def __init__(self):
        self.current_size = GRANDEUR_NORMALE

        self.write_buffer = bytes()

    def write_byte_buffer(self, byte: int):
        self.write_buffer += write_byte(byte)

    def flush(self) -> bytes:
        b = deepcopy(self.write_buffer)
        self.write_buffer = bytes()
        return b

    def write_word(self, word):
        self.write_byte_buffer(high_byte(word))
        self.write_byte_buffer(low_byte(word))

    def write_bytes_pro(self, n):
        self.write_byte_buffer(ESC)
        if n == 1:
            self.write_byte_buffer(0x39)
        elif n == 2:
            self.write_byte_buffer(0x3A)
        elif n == 3:
            self.write_byte_buffer(0x3B)

    def write_byte_p(self, n):
        if n <= 9:
            self.write_byte_buffer(0x30 + n)
        else:
            self.write_byte_buffer(0x30 + n // 10)
            self.write_byte_buffer(0x30 + n % 10)

    def set_attribute(self, attribute):
        self.write_byte_buffer(ESC)
        self.write_byte_buffer(attribute)
        if attribute == DOUBLE_HAUTEUR or attribute == DOUBLE_HAUTEUR:
            self.move_cursor_down(1)
            self.current_size = attribute
        elif attribute == GRANDEUR_NORMALE or attribute == DOUBLE_LARGEUR:
            self.current_size = attribute

    def move_cursor_xy(self, x, y):
        self.write_word(CSI)
        self.write_byte_p(y)
        self.write_byte_buffer(0x3B)
        self.write_byte_p(x)
        self.write_byte_buffer(0x48)

    def move_cursor_left(self, n):
        if n == 1:
            self.write_byte_buffer(BS)
        else:
            self.write_word(CSI)
            self.write_byte_p(n)
            self.write_byte_buffer(0x44)

    def move_cursor_right(self, n):
        if n == 1:
            self.write_byte_buffer(HT)
        else:
            self.write_word(CSI)
            self.write_byte_p(n)
            self.write_byte_buffer(0x43)

    def move_cursor_down(self, n):
        if n == 1:
            self.write_byte_buffer(LF)
        else:
            self.write_word(CSI)
            self.write_byte_p(n)
            self.write_byte_buffer(0x42)

    def move_cursor_up(self, n):
        if n == 1:
            self.write_byte_buffer(VT)
        else:
            self.write_word(CSI)
            self.write_byte_p(n)
            self.write_byte_buffer(0x41)

    def move_cursor_return(self, n):
        self.write_byte_buffer(CR)
        self.move_cursor_down(n)

    def clear_screen_from_cursor(self):
        self.write_word(CSI)
        self.write_byte_buffer(0x4A)

    def clear_screen_to_cursor(self):
        self.write_word(CSI)
        self.write_byte_buffer(0x31)
        self.write_byte_buffer(0x4A)

    def clean_screen(self):
        self.write_word(CSI)
        self.write_byte_buffer(0x32)
        self.write_byte_buffer(0x4A)

    def clear_line_from_cursor(self):
        self.write_word(CSI)
        self.write_byte_buffer(0x4B)

    def clear_line_to_cursor(self):
        self.write_word(CSI)
        self.write_byte_buffer(0x31)
        self.write_byte_buffer(0x4B)

    def clear_line(self):
        self.write_word(CSI)
        self.write_byte_buffer(0x32)
        self.write_byte_buffer(0x4B)

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
            self.write_byte_buffer(char_byte)

    def new_screen(self):
        self.write_byte_buffer(FF)
        self.current_size = GRANDEUR_NORMALE

    def graphic_mode(self):
        self.write_byte_buffer(SO)

    def graphic_at(self, byte, x, y):
        self.move_cursor_xy(x, y)
        self.graphic(byte)

    def graphic(self, byte):
        if byte <= 0b111111:
            byte = (
                0x20
                + bit_read(byte, 5)
                + bit_read(byte, 4) * 2
                + bit_read(byte, 3) * 4
                + bit_read(byte, 2) * 8
                + bit_read(byte, 1) * 16
                + bit_read(byte, 0) * 64
            )
            if byte == 0x7F:
                byte = 0x5F

            self.write_byte_buffer(byte)

    def repeat(self, n):
        self.write_byte_buffer(REP)
        self.write_byte_buffer(0x40 + n)

    def text_mode(self):
        self.write_byte_buffer(SI)

    def h_line(self, x1, y, x2, pos):
        self.text_mode()
        self.move_cursor_xy(x1, y)

        if pos == TOP:
            self.write_byte_buffer(0x7E)
        elif pos == CENTER:
            self.write_byte_buffer(0x60)
        elif pos == BOTTOM:
            self.write_byte_buffer(0x5F)

        self.repeat(x2 - x1)

    def v_line(self, x, y1, y2, pos, direction):
        self.text_mode()
        if direction == DOWN:
            self.move_cursor_xy(x, y1)
        elif direction == UP:
            self.move_cursor_xy(x, y2)

        for i in range(y2 - y1):
            if pos == LEFT:
                self.write_byte_buffer(0x7B)
            elif pos == CENTER:
                self.write_byte_buffer(0x7C)
            elif pos == RIGHT:
                self.write_byte_buffer(0x7D)

            if direction == DOWN:
                self.move_cursor_left(1)
                self.move_cursor_down(1)
            elif direction == UP:
                self.move_cursor_left(1)
                self.move_cursor_up(1)

    def cursor(self):
        self.write_byte_buffer(CON)

    def no_cursor(self):
        self.write_byte_buffer(COFF)

    def new_xy(self, i, j):
        if i == 1 and j == 1:
            self.write_byte_buffer(RS)
        else:
            self.write_byte_buffer(US)
            self.write_byte_buffer(0x40 + i)
            self.write_byte_buffer(0x40 + j)
