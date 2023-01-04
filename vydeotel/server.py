from socketserver import BaseRequestHandler, TCPServer, ThreadingTCPServer
from socketserver import ThreadingTCPServer, BaseRequestHandler
from vydeotel.page import Page
from typing import Callable, Any


class Server(ThreadingTCPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        RequestHandlerClass: Callable[[Any, Any, Any], BaseRequestHandler],
        landing: Page,
        bind_and_activate: bool = ...,
    ) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.landing = landing
