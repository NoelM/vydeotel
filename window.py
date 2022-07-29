from consts import *
from input import *
from connector import Connector
from typing import Optional


class Window:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            fg=CARACTERE_BLANC,
            bg=FOND_NORMAL,
            typo=GRANDEUR_NORMALE):

        # Position
        self.x = x
        self.y = y

        # Size
        self.width = width
        self.height = height

        # Style
        self.fg = fg
        self.bg = bg
        self.typo = typo

        # Input data
        self.buffer = ""
        self.inputs = list()
        self.active_input = -1

    def new_input(self, inpt: Input):
        self.inputs.append(inpt)

    def setup_inputs(self, c: Connector):
        if len(self.inputs) > 0:
            self.active_input = 0
            self.get_active_input().active(c)

    def get_active_input(self) -> Optional[Input]:
        if self.active_input < 0:
            return None
        return self.inputs[self.active_input]

    def active_next_input(self, c: Connector):
        if len(self.inputs) < self.active_input:
            self.active_input += 1
            self.get_active_input().active(c)

    def active_prev_input(self, c: Connector):
        if len(self.inputs) < self.active_input:
            self.active_input -= 1
            self.get_active_input().active(c)

    def default_style(self, c: Connector) -> None:
        c.set_attribute(self.typo)
        c.set_attribute(self.fg)
        c.set_attribute(self.bg)

    def draw(self, c: Connector) -> None:
        c.clean_screen()
        self.default_style(c)

        for inpt in self.inputs:
            inpt.draw(c)
        c.move_cursor_xy(self.x, self.y)

    def new_key(self, key: int):
        self.buffer += chr(key)

    def envoi(self, c: Connector):
        pass

    def annulation(self, c: Connector):
        pass

    def correction(self, c: Connector):
        pass

    def repetition(self, c: Connector):
        pass

    def sommaire(self, c: Connector):
        pass

    def retour(self, c: Connector):
        pass

    def guide(self, c: Connector):
        pass

    def suite(self, c: Connector):
        pass
