import sys
from consts import DOUBLE_GRANDEUR, GRANDEUR_NORMALE, INVERSION_FOND
sys.path.append('../')
import vydeotel as vy

class LogWindow(vy.Window):
    def __init__(self, m: vy.Minitel):
        super().__init__(m, 0, 0, 40, 40)

    def draw(self):
        super().draw()
        self.m.set_attribute(DOUBLE_GRANDEUR)
        self.m.set_attribute(INVERSION_FOND)
        self.m.println("MESSAGERIE")

        self.default_style()
        self.m.println("PSEUDO       .............")
        self.m.println("MOT DE PASSE .............")