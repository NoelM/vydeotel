from threading import Thread
from vydeotel.connector import Connector
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
from vydeotel.teleltel import Teletel


class Session:
    def __init__(self, connector: Connector, landing: Page):
        self.connector = connector

        self.landing = landing
        self.current_page = landing
        self.previous_page = None

        self.thread = None

    def start(self):
        self.thread = Thread(target=self._loop)
        self.thread.start()

    def _loop(self):
        self._new_page(self.landing)
        while True:
            key = self.connector.get_key_code()
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
        self.connector.write(self.current_page.flush())

    def _new_page(self, page: Page):
        self.previous_page = self.current_page
        self.current_page = page
        self._draw()

    def new_key(self, key):
        self.current_page.new_key(key)
        self.connector.write(self.current_page.flush())

    def envoi(self):
        p = self.current_page.envoi()
        if p is not None:
            self._new_page(p)
        else:
            self.connector.write(self.current_page.flush())

    def annulation(self):
        p = self.current_page.annulation()
        if p is not None:
            self._new_page(p)
        else:
            self.connector.write(self.current_page.flush())

    def correction(self):
        p = self.current_page.correction()
        if p is not None:
            self._new_page(p)
        else:
            self.connector.write(self.current_page.flush())

    def repetition(self):
        p = self.current_page.repetition()
        if p is not None:
            self._new_page(p)
        else:
            self.connector.write(self.current_page.flush())

    def sommaire(self):
        p = self.current_page.sommaire()
        if p is not None:
            self._new_page(p)
        else:
            self.connector.write(self.current_page.flush())

    def retour(self):
        p = self.current_page.retour()
        if p is not None:
            self._new_page(p)
        else:
            self.connector.write(self.current_page.flush())

    def guide(self):
        p = self.current_page.guide()
        if p is not None:
            self._new_page(p)
        else:
            self.connector.write(self.current_page.flush())

    def suite(self):
        p = self.current_page.suite()
        if p is not None:
            self._new_page(p)
        else:
            self.connector.write(self.current_page.flush())
