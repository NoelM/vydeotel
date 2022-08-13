import sys

sys.path.append("../")
import minitel as mn
import server as srv
from input import Input
from form import Form
from page import Page
from typing import Optional
from minitel import Minitel


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
                    minitel=mntl,
                    column=15,
                    row=4,
                    length=10,
                ),
                Input(
                    minitel=mntl,
                    column=15,
                    row=5,
                    length=10,
                ),
            ],
        )

        self.credentials = {
            "username": "",
            "password": ""
        }

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

    def save_credentials(self, credential: str):
        if self.is_first_input_active():  # username
            self.credentials["username"] = credential
        elif self.is_last_input_active():  # password
            self.credentials["password"] = credential

    def suite(self) -> None:
        credential = self.get_active_input().get_buffer()
        self.save_credentials(credential)

        self.activate_next_input()

    def envoi(self) -> Optional[Page]:
        credential = self.get_active_input().get_buffer()
        self.save_credentials(credential)

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
        self.credentials = {
            "username": "",
            "password": ""
        }
        self.buffer = ""

    def get_username(self):
        if len(self.credentials) == 0:
            return ""

        return self.credentials[0]

    def is_credentials_valid(self):
        return ("NONO", "TRANSPAC") == self.credentials


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
