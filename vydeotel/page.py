from __future__ import annotations
from vydeotel.consts import *
from vydeotel.teleltel import Teletel
from vydeotel.utils import between_bounds
from typing import Optional


class Page:
    def __init__(
        self,
        column: int,
        row: int,
        width: int,
        height: int,
        fg=CARACTERE_BLANC,
        bg=FOND_NORMAL,
        typo=GRANDEUR_NORMALE,
    ) -> None:

        self.teletel = Teletel()

        # Position
        self.column = between_bounds(column, 1, COLONNES)
        self.row = between_bounds(row, 1, LIGNES)

        # Size
        self.width = width
        self.height = height

        # Style
        self.fg = fg
        self.bg = bg
        self.typo = typo

        self.buffer = ""

    def default_style(self) -> None:
        self.teletel.set_attribute(self.typo)
        self.teletel.set_attribute(self.fg)
        self.teletel.set_attribute(self.bg)

    def default_pos(self) -> None:
        self.teletel.move_cursor_xy(self.column, self.row)

    def draw(self) -> None:
        self.teletel.clean_screen()
        self.teletel.move_cursor_xy(self.column, self.row)
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
