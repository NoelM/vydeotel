from minitel import Minitel
from utils import between_bounds


class Input:
    def __init__(self, minitel: Minitel, column: int, row: int, length: int, dots=True):
        self.minitel = minitel

        self.column = between_bounds(column, 1, minitel.columns)
        self.row = between_bounds(row, 1, minitel.rows)
        self.length = between_bounds(length, 1, minitel.columns - self.column)

        self.dots = dots
        self.cursor = True

        self.buffer = ""

    def cursor_on(self):
        self.cursor = True

    def cursor_off(self):
        self.cursor = False

    def draw(self):
        self.minitel.move_cursor_xy(self.column, self.row)

        if self.dots:
            for i in range(self.length):
                self.minitel.print_char(".")

    def active(self):
        self.minitel.move_cursor_xy(self.column, self.row)

        if self.cursor:
            self.minitel.cursor()
        else:
            self.minitel.no_cursor()

    def new_char(self, char: chr):
        if len(self.buffer) < self.length:
            self.buffer += char
        else:
            self.minitel.clear_line_from_cursor()
            self.minitel.move_cursor_left(1)

    def get_buffer(self) -> str:
        return self.buffer

    def correction(self):
        if len(self.buffer) > 0:
            self.buffer = self.buffer[:-1]
            self.minitel.move_cursor_left(1)

            if self.dots:
                self.minitel.print_char(".")
                self.minitel.move_cursor_left(1)
            else:
                self.minitel.clear_line_from_cursor()

    def annulation(self):
        self.minitel.move_cursor_xy(self.column, self.row)
        self.minitel.clear_line_from_cursor()
        self.draw()
