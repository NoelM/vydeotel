from window import *
from connector import *


class Server:
    def __init__(self, connector: Connector, window: Window):
        self.connector = connector
        self.window = window

    def start(self):
        new_window = None
        self.window.draw(self.connector)
        while True:
            if new_window is not None:
                self.window = new_window
                new_window = None
                self.window.draw(self.connector)

            key = self.connector.get_key_code()
            if key == ENVOI:
                new_window = self.window.envoi(self.connector)
            elif key == ANNULATION:
                new_window = self.window.annulation(self.connector)
            elif key == REPETITION:
                new_window = self.window.repetition(self.connector)
            elif key == CORRECTION:
                new_window = self.window.correction(self.connector)
            elif key == SOMMAIRE:
                new_window = self.window.sommaire(self.connector)
            elif key == RETOUR:
                new_window = self.window.retour(self.connector)
            elif key == GUIDE:
                new_window = self.window.guide(self.connector)
            elif key == SUITE:
                new_window = self.window.suite(self.connector)
            else:
                self.window.new_key(self.connector, key)
