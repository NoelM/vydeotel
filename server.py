from form import *
from minitel import *


class Server:
    def __init__(self, minitel: Minitel, page: Page):
        self.minitel = minitel
        self.page = page

    def start(self):
        self.page.draw()
        new_page = None

        while True:
            if new_page is not None:
                self.page = new_page
                self.page.draw()

                new_page = None

            key = self.minitel.get_key_code()
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
            else:
                self.page.new_key(key)
