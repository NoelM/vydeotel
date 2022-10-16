import sys

sys.path.append("../vydeotel/")
import hashlib
import dbm

from vydeotel.server import Server
from vydeotel.session import Session
from vydeotel.input import Input
from vydeotel.form import Form
from vydeotel.page import Page
from vydeotel.consts import INVERSION_FOND, DOUBLE_GRANDEUR

from typing import Optional

USERNAME = "username"
PASSWORD = "password"
PASSWORD_VALID = "password_valid"

users = dbm.open("users.db", "c")


class LogWindow(Form):
    def __init__(self):
        super().__init__(
            inputs=[
                Input(
                    key=USERNAME,
                    column=15,
                    row=4,
                    length=10,
                ),
                Input(
                    key=PASSWORD,
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

        self.minitel.set_attribute(INVERSION_FOND)
        self.minitel.set_attribute(DOUBLE_GRANDEUR)
        self.minitel.println("MESSAGERIE")

        self.default_style()
        self.minitel.move_cursor_down(1)

        self.minitel.println("PSEUDO")
        self.minitel.println("MOT DE PASSE")

        self.minitel.move_cursor_down(3)
        self.minitel.println("Saisissez votre Pseudo et Mot de Passe")
        self.minitel.println("en navigant avec SUITE et RETOUR")
        self.minitel.println("Tappez sur ENVOI lorsque tout est rempli")

        self.minitel.move_cursor_down(2)
        self.minitel.println("Pour vous inscrire GUIDE")

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
            username=self.get_username(),
        )

    def guide(self) -> Page:
        return SignInWindow()

    def failed_login(self):
        self.minitel.move_cursor_xy(1, 6)
        self.minitel.set_attribute(INVERSION_FOND)
        self.minitel.println("Pseudo ou MDP invalides")
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
        h = hashlib.sha3_256()
        h.update(bytes(self.credentials[PASSWORD], "utf-8"))

        return (
            self.credentials[USERNAME] in users
            and users[self.credentials[USERNAME]] == h.digest()
        )


class SignInWindow(Form):
    def __init__(self):
        super().__init__(
            inputs=[
                Input(
                    key=USERNAME,
                    column=25,
                    row=4,
                    length=10,
                ),
                Input(
                    key=PASSWORD,
                    column=25,
                    row=5,
                    length=10,
                ),
                Input(
                    key=PASSWORD_VALID,
                    column=25,
                    row=6,
                    length=10,
                ),
            ],
        )

        self.credentials = {}

    def draw(self) -> None:
        super().draw()

        self.default_pos()
        self.minitel.move_cursor_down(1)

        self.minitel.set_attribute(INVERSION_FOND)
        self.minitel.set_attribute(DOUBLE_GRANDEUR)
        self.minitel.println("INSCRIPTION")

        self.default_style()
        self.minitel.move_cursor_down(1)

        self.minitel.println("PSEUDO")
        self.minitel.println("MOT DE PASSE")
        self.minitel.println("MOT DE PASSE (COPIE)")

        self.minitel.move_cursor_down(3)
        self.minitel.println("Choisissez votre Pseudo et Mot de Passe")
        self.minitel.println("en navigant avec SUITE et RETOUR")
        self.minitel.println("Tappez sur ENVOI lorsque tout est rempli")

        self.activate_first_input()

    def envoi(self) -> Optional[Page]:
        self.credentials = self.get_form()

        if not self.is_credentials_valid():
            self.reset()
            self.reset_inputs()
            self.activate_first_input()
            return None

        self.register()

        return LogWindow()

    def is_credentials_valid(self):
        print(self.credentials)
        return (
            self.credentials[USERNAME] not in users
            and self.credentials[PASSWORD] == self.credentials[PASSWORD_VALID]
        )

    def reset(self):
        self.buffer = ""

    def register(self):
        h = hashlib.sha3_256()
        h.update(bytes(self.credentials[PASSWORD], "utf-8"))
        users[self.credentials[USERNAME]] = h.digest()

        self.credentials = {}


class ChatWindow(Page):
    def __init__(self, username: str):
        super().__init__()
        self.username = username

    def draw(self):
        super().draw()
        self.minitel.println(f"Salut {self.username}, petit coquin va!")


ADDRESS = ""
PORT = 3615

minitel_tcp_server = Server((ADDRESS, PORT), Session)
minitel_tcp_server.serve_forever()
