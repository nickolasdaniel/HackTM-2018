import socket
import select
import sys
import logging
from config_server import *
import struct

try:
    import queue
except ImportError:
    import Queue as queue


class Server(object):
    def __init__(self, server_address=None, setBlocking= False , reuse_address=True, port=8080):

        self.__server_logger=logging.getLogger(__name__ + ".chat_server")

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.message_queue= {}

        self.data_struct = struct.Struct("I")

        if server_address:
            self.server_address = server_address
        else:
            self.server_address = (str(config_parser.get("server_config","host_address")),
                int(config_parser.get("server_config","port")))

        try:
            self.socket_server.bind(self.server_address)
        except socket.error as serr:
            self.__server_logger.exception("[ ERROR ] Error binding socket")
            sys.exit(1)
        if setBlocking:
            self.socket_server.setblocking(1)

        if reuse_address:
            self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket,"SO_REUSEPORT"):
                self.socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

        self.socket_server.listen(5)
        self.__server_logger.info("[ SERVER ] Started listen on ({}:{})".format(self.server_address[0],self.server_address[1]))

        self.inputs = inputs =[self.socket_server]
        self.outputs = []

        self.server_status=True

    def start_server(self):

        while self.server_status:
            try:
                readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs)

                for sock in readable:
                    if sock is self.socket_server:
                        client_socket,client_adrr=self.socket_server.accept()
                        self.__server_logger.info("[ CLIENT ] Client just connected {}:{}".format(client_adrr[0],client_adrr[1]))

                        self.socket_server.setblocking(0)
                        self.inputs.append(client_socket)
                        self.message_queue[client_socket] = queue.Queue()
                    else:
                        self.handle_client(sock)

                for sock in writeable:

                    try:
                        message = self.message_queue[sock].get_nowait()
                    except queue.Empty as qerr:
                        self.__server_logger.exception("[ ERROR ] Queue is empty ")
                        sys.exit(1)
                    else:
                        for client in self.inputs[1:]:
                            self.send_message(client, message)

                for sock in exceptional:

                    self.__server_logger.exception("[ ERROR ] Client is no more active or something happened... ")
                    self.inputs.remove(sock)

                    if sock in self.outputs:
                        self.outputs.remove(sock)

                    del self.message_queue[sock]

                    sock.close()

            except KeyboardInterrupt as kerrr:
                self.shutdown_server()

    def handle_client(self, client_socket):
        MAX_RECV_BYTES = 1024

        data_buffer = ""

        try:
            data_buffer = client_socket.recv(MAX_RECV_BYTES)
        except IOError as ierr:
            self.__server_logger.error(str(ierr))
            sys.exit(1)

        else:
            if not data_buffer:
                self.disconnect_client(client_socket)
            else:
                self.message_queue[client_socket].put(data_buffer)
                if client_socket not in self.outputs:
                    self.outputs.append(client_socket)


    def shutdown_server(self):
        self.__server_logger.info("[ SERVER ] Server is closing...")
        for client in self.inputs:
            self.disconnect_client(client)
        self.server_status = False
        self.socket_server.close()
        sys.exit(0)

    def disconnect_client(self,client_socket):

        self.__server_logger.info("[ CLIENT ] Client just disconnected ")
        self.inputs.remove(client_socket)

        if client_socket in self.outputs:
            self.outputs.remove(client_socket)

        if client_socket in list(self.message_queue.keys()):
            del self.message_queue[client_socket]

        client_socket.close()

    def send_message(self,client_socket,message):

        try:
            client_socket.send(message)
        except IOError as kerr:
            self.__server_logger.error("[ ERROR ] Something wrong with the client")
        else:
            if client_socket in self.outputs:
                self.outputs.remove(client_socket)


    """ def recv_message(self, board_serial):
         pass

     def send_signal(self, board_serial):
         pass
     """

    """def recv_signal(self):
            pass"""
if __name__=="__main__":
    strv=Server()
    strv.start_server()
