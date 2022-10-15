import imp
from vydeotel.teleltel import Teletel
from vydeotel.utils import between_bounds
from vydeotel.consts import COLONNES, LIGNES


class Input:
    def __init__(self, key: str, column: int, row: int, length: int):
        self.key = key

        self.teletel = Teletel()

        self.column = between_bounds(column, 1, COLONNES)
        self.row = between_bounds(row, 1, LIGNES)
        self.length = between_bounds(length, 1, COLONNES - column)

        self.buffer = ""

    @property
    def value(self) -> str:
        return self.buffer

    def flush(self) -> bytes:
        return self.teletel.flush()

    def draw(self) -> None:
        self.teletel.move_cursor_xy(self.column, self.row)

        for i in range(self.length):
            self.teletel.print_char(".")

    def activate(self) -> None:
        self.teletel.move_cursor_xy(
            self.column + min(len(self.buffer), self.length - 1), self.row
        )
        self.teletel.cursor()

    def new_char(self, char: chr) -> None:
        if len(self.buffer) < self.length - 1:
            self.buffer += char
        else:
            self.teletel.clear_line_from_cursor()
            self.teletel.move_cursor_left(1)
            self.teletel.print_char(self.buffer[-1])
            self.teletel.move_cursor_left(1)

    def correction(self) -> None:
        if len(self.buffer) > 0:
            self.buffer = self.buffer[:-1]
            self.teletel.move_cursor_left(1)

            self.teletel.print_char(".")
            self.teletel.move_cursor_left(1)

    def annulation(self) -> None:
        self.teletel.move_cursor_xy(self.column, self.row)
        self.teletel.clear_line_from_cursor()

        self.reset()
        self.activate()

    def reset(self) -> None:
        self.buffer = ""
        self.draw()
