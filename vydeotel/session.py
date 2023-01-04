import socketserver
from vydeotel.connector import Connector, TCPConnector
from vydeotel.page import Page
from vydeotel.consts import (
    ENVOI,
    ANNULATION,
    REPETITION,
    CORRECTION,
    SOMMAIRE,
    RETOUR,
    GUIDE,
    SUITE,
)
from vydeotel.minitel import Minitel


class Session(socketserver.BaseRequestHandler):
    def setup(self):
        self.connector = TCPConnector(self.request)
        self.minitel = Minitel(self.connector)

        self.landing = self.server.landing()
        self.current_page = None
        self.previous_page = None

    def handle(self):
        self._new_page(self.landing)
        while True:
            key = self.minitel.get_key_code()
            if key == ENVOI:
                self.envoi()
            elif key == ANNULATION:
                self.annulation()
            elif key == REPETITION:
                self.repetition()
            elif key == CORRECTION:
                self.correction()
            elif key == SOMMAIRE:
                self.sommaire()
            elif key == RETOUR:
                self.retour()
            elif key == GUIDE:
                self.guide()
            elif key == SUITE:
                self.suite()
            elif key is not None:
                self.new_key(key)

    def _draw(self):
        self.current_page.draw()

    def _new_page(self, page: Page):
        self.previous_page = self.current_page
        self.current_page = page
        self.current_page.setup(self.minitel)
        self._draw()

    def new_key(self, key):
        self.current_page.new_key(key)

    def envoi(self):
        p = self.current_page.envoi()
        if p is not None:
            self._new_page(p)

    def annulation(self):
        p = self.current_page.annulation()
        if p is not None:
            self._new_page(p)

    def correction(self):
        p = self.current_page.correction()
        if p is not None:
            self._new_page(p)

    def repetition(self):
        p = self.current_page.repetition()
        if p is not None:
            self._new_page(p)

    def sommaire(self):
        p = self.current_page.sommaire()
        if p is not None:
            self._new_page(p)

    def retour(self):
        p = self.current_page.retour()
        if p is not None:
            self._new_page(p)

    def guide(self):
        p = self.current_page.guide()
        if p is not None:
            self._new_page(p)

    def suite(self):
        p = self.current_page.suite()
        if p is not None:
            self._new_page(p)
