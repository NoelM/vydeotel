from minitel import Minitel
from utils import between_bounds


class Input:
    def __init__(self, minitel: Minitel, column: int, row: int, length: int):
        self.minitel = minitel

        self.column = between_bounds(column, 1, minitel.columns)
        self.row = between_bounds(row, 1, minitel.rows)
        self.length = between_bounds(length, 1, minitel.columns - self.column)

        self.buffer = ""

    def draw(self):
        self.minitel.move_cursor_xy(self.column, self.row)

        for i in range(self.length):
            self.minitel.print_char(".")

    def activate(self):
        self.minitel.move_cursor_xy(self.column + len(self.buffer), self.row)
        self.minitel.cursor()

    def new_char(self, char: chr):
        if len(self.buffer) < self.length - 1:
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

            self.minitel.print_char(".")
            self.minitel.move_cursor_left(1)

    def annulation(self):
        self.minitel.move_cursor_xy(self.column, self.row)
        self.minitel.clear_line_from_cursor()
        self.draw()

        self.buffer = ""
