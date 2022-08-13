from __future__ import annotations
from consts import *
from minitel import Minitel
from utils import between_bounds
from typing import Optional


class Page:
    def __init__(
        self,
        minitel: Minitel,
        column: int,
        row: int,
        width: int,
        height: int,
        fg=CARACTERE_BLANC,
        bg=FOND_NORMAL,
        typo=GRANDEUR_NORMALE,
    ) -> None:

        self.minitel = minitel

        # Position
        self.column = between_bounds(column, 1, minitel.columns)
        self.row = between_bounds(row, 1, minitel.rows)

        # Size
        self.width = width
        self.height = height

        # Style
        self.fg = fg
        self.bg = bg
        self.typo = typo

        self.buffer = ""

    def default_style(self) -> None:
        self.minitel.set_attribute(self.typo)
        self.minitel.set_attribute(self.fg)
        self.minitel.set_attribute(self.bg)

    def draw(self) -> None:
        self.minitel.clean_screen()
        self.minitel.move_cursor_xy(self.column, self.row)
        self.default_style()

    def new_key(self, key: int) -> None:
        self.buffer += chr(key)

    def envoi(self) -> Optional[Page]:
        pass

    def annulation(self) -> Optional[Page]:
        pass

    def correction(self) -> Optional[Page]:
        pass

    def repetition(self) -> Optional[Page]:
        pass

    def sommaire(self) -> Optional[Page]:
        pass

    def retour(self) -> Optional[Page]:
        pass

    def guide(self) -> Optional[Page]:
        pass

    def suite(self) -> Optional[Page]:
        pass
