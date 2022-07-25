import sys
from consts import DOUBLE_GRANDEUR, GRANDEUR_NORMALE, INVERSION_FOND
sys.path.append('../')
import vydeotel as vy

class LogWindow(vy.Window):
    def __init__(self):
        super().__init__(0, 0, 40, 40)
        self.credentials = []
        self.next_window = ChatWindow()

    def draw(self):
        super().draw()
        self.m.set_attribute(DOUBLE_GRANDEUR)
        self.m.set_attribute(INVERSION_FOND)
        self.m.println("MESSAGERIE")

        self.default_style()
        self.m.println("PSEUDO       .............")
        self.m.println("MOT DE PASSE .............")

        self.m.move_cursor_xy(2, 13)
        self.m.cursor()

    def envoi(self) -> vy.Window:
        if len(self.credentials) == 0:  # username
            self.credentials.append(self.buffer)
            self.buffer = ""

            self.m.move_cursor_xy(3, 13)
            self.m.cursor()
            return None

        else:
            self.credentials.append(self.buffer)
            self.buffer = ""
            return self.next_window


class ChatWindow(vy.Window):
    def __init__(self):
        super().__init__(0, 0, 40, 40)

    def draw(self):
        self.m.println("Salut Coquin")


if __name__ == "__main__"
    window = LogWindow()

    minitel = vy.Minitel("/dev/ttyS0")
    minitel.set_window(window)

