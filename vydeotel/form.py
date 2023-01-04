from vydeotel.page import Page
from vydeotel.consts import *
from vydeotel.minitel import Minitel
from vydeotel.input import Input
from typing import Optional, List, Dict


class Form(Page):
    def __init__(
        self,
        inputs: List[Input],
        column: int = 1,
        row: int = 1,
        width: int = COLONNES,
        height: int = LIGNES,
        fg: int = CARACTERE_BLANC,
        bg: int = FOND_NORMAL,
        typo: int = GRANDEUR_NORMALE,
    ) -> None:

        super().__init__(column, row, width, height, fg, bg, typo)

        # Input data
        self.inputs = inputs
        self.active_input = -1

    def setup(self, minitel: Minitel):
        super().setup(minitel)
        for i in self.inputs:
            i.setup(minitel)

    def get_active_input(self) -> Optional[Input]:
        if len(self.inputs) == 0 or self.active_input < 0:
            return None
        return self.inputs[self.active_input]

    def is_first_input_active(self) -> bool:
        return self.active_input == 0

    def is_last_input_active(self) -> bool:
        return self.active_input == len(self.inputs) - 1

    def activate_first_input(self) -> None:
        if len(self.inputs) > 0:
            self.active_input = 0
            self.get_active_input().activate()

    def activate_next_input(self) -> None:
        if not self.is_last_input_active():
            self.active_input += 1
            self.get_active_input().activate()

    def activate_prev_input(self) -> None:
        if not self.is_first_input_active():
            self.active_input -= 1
            self.get_active_input().activate()

    def get_form(self) -> Dict[str, str]:
        form = {}
        for i in self.inputs:
            form[i.key] = i.value

        return form

    def draw(self) -> None:
        super().draw()

        for i in self.inputs:
            i.draw()

    def reset_inputs(self) -> None:
        for i in self.inputs:
            i.reset()

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
