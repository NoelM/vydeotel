from page import Page
from consts import *
from minitel import Minitel
from input import Input
from typing import Optional, List


class Form(Page):
    def __init__(
        self,
        minitel: Minitel,
        column: int,
        row: int,
        width: int,
        height: int,
        inputs: List[Input],
        fg=CARACTERE_BLANC,
        bg=FOND_NORMAL,
        typo=GRANDEUR_NORMALE,
    ) -> None:

        super().__init__(minitel, column, row, width, height, fg, bg, typo)

        # Input data
        self.inputs = inputs
        self.active_input = -1

    def get_active_input(self) -> Optional[Input]:
        if len(self.inputs) == 0 or self.active_input < 0:
            return None
        return self.inputs[self.active_input]

    def activate_first_input(self) -> None:
        if len(self.inputs) > 0:
            self.active_input = 0
            self.get_active_input().activate()

    def activate_next_input(self) -> None:
        if self.active_input < len(self.inputs) - 1:
            self.active_input += 1
            self.get_active_input().activate()

    def activate_prev_input(self) -> None:
        if self.active_input > 0:
            self.active_input -= 1
            self.get_active_input().activate()

    def draw(self) -> None:
        super().draw()

        if len(self.inputs) == 0:
            return

        for i in self.inputs:
            i.draw()

    def new_key(self, key: int) -> None:
        self.get_active_input().new_char(chr(key))

    def annulation(self) -> None:
        self.get_active_input().annulation()

    def correction(self) -> None:
        self.get_active_input().correction()

    def suite(self) -> None:
        self.activate_next_input()

    def retour(self) -> None:
        self.activate_prev_input()
