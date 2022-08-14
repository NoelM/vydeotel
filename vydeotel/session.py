import imp
from connector import Connector
from application import Application
from consts import (
    ENVOI,
    ANNULATION,
    REPETITION,
    CORRECTION,
    SOMMAIRE,
    RETOUR,
    GUIDE,
    SUITE,
)
from videotext import VideoText


class Session:
    def __init__(self, connector: Connector, app: Application):
        self.videotxt = VideoText(connector)

    def start(self):
        self.page.draw()
        new_page = None

        while True:
            if new_page is not None:
                self.page = new_page
                self.page.draw()

                new_page = None

            key = self.videotxt.get_key_code()
            if key == ENVOI:
                new_page = self.page.envoi()
            elif key == ANNULATION:
                new_page = self.page.annulation()
            elif key == REPETITION:
                new_page = self.page.repetition()
            elif key == CORRECTION:
                new_page = self.page.correction()
            elif key == SOMMAIRE:
                new_page = self.page.sommaire()
            elif key == RETOUR:
                new_page = self.page.retour()
            elif key == GUIDE:
                new_page = self.page.guide()
            elif key == SUITE:
                new_page = self.page.suite()
            elif key is not None:
                self.page.new_key(key)
