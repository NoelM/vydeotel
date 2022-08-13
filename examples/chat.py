import sys

sys.path.append("../")
import minitel as mn
import server as srv
from input import Input
from form import Form
from page import Page
from typing import Optional
from minitel import Minitel

USERNAME = "username"
PASSWORD = "password"


class LogWindow(Form):
    def __init__(self, mntl: Minitel):
        super().__init__(
            minitel=mntl,
            column=1,
            row=1,
            width=mntl.columns,
            height=mntl.rows,
            inputs=[
                Input(
                    key=USERNAME,
                    minitel=mntl,
                    column=15,
                    row=4,
                    length=10,
                ),
                Input(
                    key=PASSWORD,
                    minitel=mntl,
                    column=15,
                    row=5,
                    length=10,
                ),
            ],
        )

        self.credentials = {}

    def draw(self) -> None:
        super().draw()
        self.default_pos()
        self.minitel.move_cursor_down(1)

        self.minitel.set_attribute(mn.INVERSION_FOND)
        self.minitel.set_attribute(mn.DOUBLE_GRANDEUR)
        self.minitel.println("MESSAGERIE")

        self.default_style()
        self.minitel.move_cursor_down(1)

        self.minitel.println("PSEUDO")
        self.minitel.println("MOT DE PASSE")

        self.activate_first_input()

    def envoi(self) -> Optional[Page]:
        self.credentials = self.get_form()

        if not self.is_credentials_valid():
            self.reset()
            self.failed_login()
            self.reset_inputs()
            self.activate_first_input()
            return None

        return ChatWindow(
            mntl=self.minitel,
            username=self.get_username(),
        )

    def failed_login(self):
        self.minitel.move_cursor_xy(1, 6)
        self.minitel.set_attribute(mn.INVERSION_FOND)
        self.minitel.println("Pseudo ou MDP invalide")
        self.default_style()

    def new_key(self, key: int):
        self.get_active_input().new_char(chr(key))

    def reset(self):
        self.buffer = ""

    def get_username(self):
        if USERNAME not in self.credentials:
            return ""

        return self.credentials[USERNAME]

    def is_credentials_valid(self):
        return {USERNAME: "NONO", PASSWORD: "TRANPAC"} == self.credentials


class ChatWindow(Page):
    def __init__(self, mntl: Minitel, username: str):
        super().__init__(
            minitel=mntl,
            column=1,
            row=1,
            width=mntl.columns,
            height=mntl.rows,
        )

        self.username = username

    def draw(self):
        super().draw()
        self.minitel.println(f"Salut {self.username}, petit coquin va!")


if __name__ == "__main__":
    minitel = mn.Minitel("/dev/ttyS0")
    login_window = LogWindow(minitel)

    server = srv.Server(minitel, login_window)
    server.start()
