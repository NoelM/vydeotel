import sys
sys.path.append('../')
import vydeotel as vy

class LogWindow(vy.Window):
    def __init__(self):
        super().__init__(0, 0, 40, 40)
        self.credentials = []

    def draw(self):
        super().draw()
        self.m.set_attribute(vy.DOUBLE_GRANDEUR)
        self.m.set_attribute(vy.INVERSION_FOND)
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
            return ChatWindow(self.credentials[0])


class ChatWindow(vy.Window):
    def __init__(self, username: str):
        super().__init__(0, 0, 40, 40)
        self.username = username

    def draw(self):
        self.m.println(f"Salut {self.username}, petit coquin va!")


if __name__ == "__main__":
    window = LogWindow()

    minitel = vy.Minitel("/dev/ttyS0")
    minitel.set_window(window)
    minitel.start()

