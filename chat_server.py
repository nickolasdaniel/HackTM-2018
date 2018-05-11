import socket
import select
import sys
import logging
from config_server import *
import struct


class Server(object):
    def __init__(self, server_address=None, setBlocking= False , reuse_port=True, reuse_address=True, port=8080):

        self.__server_logger=logging.getLogger(__name__ + ".chat_server")

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.data_struct = struct.Struct("I")

        if server_address:
            self.server_address = server_address
        else:
            self.server_address = (str(config_parser.get("server_config","host_address")),
                int(config_parser.get("server_config","port")))

        try:
            self.socket_server.bind(self.server_address)
        except socket.error as serr:
            self.__server_logger.exception("Error binding socket")
            sys.exit(1)
        if setBlocking:
            self.socket_server.setblocking(1)

        if reuse_address:
            self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket_server.listen(5)

        self.inputs = [self.socket_server]
        self.outputs = []

    def start_server(self):
        server_status = True

        while server_status:
            readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs)

            for sock in readable:
                if socket == self.socket_server:
                    pass
                else:
                    pass

            for sock in writeable:
                pass

            for sock in exceptional:
                pass

    def handle_client(self, client_socket):
        pass

    def send_message(self):
        pass

    """ def recv_message(self, board_serial):
         pass

     def send_signal(self, board_serial):
         pass
     """

    def recv_signal(self):
        pass