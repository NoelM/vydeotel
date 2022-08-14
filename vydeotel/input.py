from videotext import VideoText
from utils import between_bounds


class Input:
    def __init__(
        self, key: str, minitel: VideoText, column: int, row: int, length: int
    ):
        self.key = key

        self.minitel = minitel

        self.column = between_bounds(column, 1, minitel.columns)
        self.row = between_bounds(row, 1, minitel.rows)
        self.length = between_bounds(length, 1, minitel.columns - self.column)

        self.buffer = ""

    @property
    def value(self) -> str:
        return self.buffer

    def draw(self) -> None:
        self.minitel.move_cursor_xy(self.column, self.row)

        for i in range(self.length):
            self.minitel.print_char(".")

    def activate(self) -> None:
        self.minitel.move_cursor_xy(
            self.column + min(len(self.buffer), self.length - 1), self.row
        )
        self.minitel.cursor()

    def new_char(self, char: chr) -> None:
        if len(self.buffer) < self.length - 1:
            self.buffer += char
        else:
            self.minitel.clear_line_from_cursor()
            self.minitel.move_cursor_left(1)
            self.minitel.print_char(self.buffer[-1])
            self.minitel.move_cursor_left(1)

    def correction(self) -> None:
        if len(self.buffer) > 0:
            self.buffer = self.buffer[:-1]
            self.minitel.move_cursor_left(1)

            self.minitel.print_char(".")
            self.minitel.move_cursor_left(1)

    def annulation(self) -> None:
        self.minitel.move_cursor_xy(self.column, self.row)
        self.minitel.clear_line_from_cursor()

        self.reset()
        self.activate()

    def reset(self) -> None:
        self.buffer = ""
        self.draw()
