from vydeotel.page import Page
from vydeotel.connector import Connector
from vydeotel.session import Session


class Application:
    def __init__(self, landing: Page):
        self.landing = landing
        self.sessions = []

    def new_session(self, conn: Connector):
        s = Session(conn, self.landing)
        s.start()
        self.sessions.append(s)
