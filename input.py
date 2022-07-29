from enum import Enum
from connector import Connector


class Input:
    def __init__(self, x: int, y: int, length: int, dots=True):
        self.x = x
        self.y = y

        self.length = length

        self.dots = dots
        self.cursor = True

        self.buffer = ""

    def cursor_on(self):
        self.cursor = True

    def cursor_off(self):
        self.cursor = False

    def draw(self, c: Connector):
        c.move_cursor_xy(self.x, self.y)

        if self.dots:
            for i in range(self.length):
                c.print_char(".")

    def active(self, c: Connector):
        c.move_cursor_xy(self.x, self.y)

        if self.cursor:
            c.cursor()
        else:
            c.no_cursor()

    def new_char(self, c: Connector, char: chr):
        if len(self.buffer) < self.length:
            self.buffer += char
            c.print_char(char)

    def get_buffer(self) -> str:
        return self.buffer

    def correction(self, c: Connector):
        if len(self.buffer) > 0:
            self.buffer = self.buffer[:-1]
            c.move_cursor_left(1)
            if self.dots:
                c.print_char(".")
            else:
                c.clear_line_from_cursor()

    def annulation(self, c: Connector):
        c.move_cursor_xy(self.x, self.y)
        c.clear_line_from_cursor()
        self.draw(c)
