from __future__ import annotations
from vydeotel.consts import *
from vydeotel.minitel import Minitel
from vydeotel.utils import between_bounds
from typing import Optional


class Page:
    def __init__(
        self,
        column: int = 1,
        row: int = 1,
        width: int = COLONNES,
        height: int = LIGNES,
        fg: int = CARACTERE_BLANC,
        bg: int = FOND_NORMAL,
        typo: int = GRANDEUR_NORMALE,
    ) -> None:

        self.minitel = None

        # Position
        self.column = column
        self.row = row

        # Size
        self.width = width
        self.height = height

        # Style
        self.fg = fg
        self.bg = bg
        self.typo = typo

        self.buffer = ""

    def setup(self, minitel: Minitel):
        self.minitel = minitel
        self.column = between_bounds(self.column, 1, self.minitel.columns)
        self.row = between_bounds(self.row, 1, self.minitel.rows)

    def default_style(self) -> None:
        self.minitel.set_attribute(self.typo)
        self.minitel.set_attribute(self.fg)
        self.minitel.set_attribute(self.bg)

    def default_pos(self) -> None:
        self.minitel.move_cursor_xy(self.column, self.row)

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
