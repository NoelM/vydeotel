import sys
sys.path.append("../vydeotel/")
import socket

from vydeotel.application import Application
from vydeotel.connector import TCPConnector
from vydeotel.input import Input
from vydeotel.form import Form
from vydeotel.page import Page
from vydeotel.consts import INVERSION_FOND, DOUBLE_GRANDEUR, COLONNES, LIGNES

from typing import Optional

USERNAME = "username"
PASSWORD = "password"


class LogWindow(Form):
    def __init__(self):
        super().__init__(
            column=1,
            row=1,
            width=COLONNES,
            height=LIGNES,
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
        self.teletel.move_cursor_down(1)

        self.teletel.set_attribute(INVERSION_FOND)
        self.teletel.set_attribute(DOUBLE_GRANDEUR)
        self.teletel.println("MESSAGERIE")

        self.default_style()
        self.teletel.move_cursor_down(1)

        self.teletel.println("PSEUDO")
        self.teletel.println("MOT DE PASSE")

        self.teletel.move_cursor_down(3)
        self.teletel.println("Saisissez votre Pseudo et Mot de Passe")
        self.teletel.println("en navigant avec SUITE et RETOUR")
        self.teletel.println("Tappez sur ENVOI lorsque tout est rempli")

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

    def failed_login(self):
        self.teletel.move_cursor_xy(1, 6)
        self.teletel.set_attribute(INVERSION_FOND)
        self.teletel.println("Pseudo ou MDP invalide")
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
        return {USERNAME: "NONO", PASSWORD: "NONO"} == self.credentials


class ChatWindow(Page):
    def __init__(self, username: str):
        super().__init__(
            column=1,
            row=1,
            width=COLONNES,
            height=LIGNES,
        )

        self.username = username

    def draw(self):
        super().draw()
        self.teletel.println(f"Salut {self.username}, petit coquin va!")


ADDRESS = ""
PORT = 3615

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ADDRESS, PORT))
server.listen(1)
client, adresseClient = server.accept()
print("Connection from:", adresseClient)

login_window = LogWindow()
chat_app = Application(login_window)
connector = TCPConnector(client)

chat_app.new_session(connector)