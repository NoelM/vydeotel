import sys
sys.path.append('../')
import connector as cn
import server as srv
from input import Input
from window import Window
from typing import Optional

import string
import random
import time
import feedparser


class LogWindow(Window):
    def __init__(self):
        super().__init__(0, 0, 40, 40)
        self.credentials = []

        self.inputs = [
            Input(14, 3, 10),
            Input(14, 4, 10)
        ]
        self.active_input = 0

    def draw(self, c: cn.Connector):
        super().draw(c)
        c.println("")
        c.set_attribute(cn.INVERSION_FOND)
        c.set_attribute(cn.DOUBLE_GRANDEUR)
        c.println("MESSAGERIE")

        self.default_style(c)
        c.println("PSEUDO")
        c.println("MOT DE PASSE")
        self.setup_inputs(c)

    def get_active_input(self) -> Optional[Input]:
        if self.active_input < 0:
            return None

        return self.inputs[self.active_input]

    def suite(self, c: cn.Connector) -> Optional[Window]:
        if len(self.credentials) == 0:  # username
            self.credentials.append(self.get_active_input().get_buffer())
            self.active_next_input(c)

        else:
            self.credentials.append(self.get_active_input().get_buffer())

        return None

    def envoi(self, c: cn.Connector) -> Optional[Window]:
        if not self.is_credentials_valid():
            self.reset()
            self.draw(c)
            return None

        return ChatWindow(self.get_username())

    def new_key(self, key: int):
        self.get_active_input().new_char(chr(key))

    def reset(self):
        self.credentials = []
        self.buffer = ""

    def get_username(self):
        if len(self.credentials) == 0:
            return ""

        return self.credentials[0]

    def is_credentials_valid(self):
        return True


class ChatWindow(Window):
    def __init__(self, username: str):
        super().__init__(0, 0, 40, 40)
        self.username = username

    def draw(self, c: cn.Connector):
        super().draw(c)
        c.println(f"Salut {self.username}, petit coquin va!")


if __name__ == "__main__":
    window = LogWindow()
    minitel = cn.Connector("/dev/ttyS0")

    server = srv.Server(minitel, window)
    server.start()

