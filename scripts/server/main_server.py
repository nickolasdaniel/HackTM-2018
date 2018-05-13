import socket
import select
import sys
import json
import logging
from ..exceptions import *

import piplates.RELAYplate as RELAY
import RPi.GPIO as GPIO

import struct
try:
    import queue
except ImportError:
    import Queue as queue

from ..config_server import *

import threading

class Server(object):

    def __init__(self, server_address=None, setBlocking= False , reuse_address=True, port=8080):

        self.data_to_send = {
            "Alarma" : False,
            "Bec1" : False,
            "Bec2" : False,
            "Bec3" : False,
            "Bec4" : False,
            "Bec5" : False
        }

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__server_logger=logging.getLogger(__name__ + ".chat_server")

        self.message_queue= {}

        self.data_struct = struct.Struct("I")

        if server_address:
            self.server_address = (server_address,port)
        else:
            self.server_address = (str(config_parser.get("server_config","host_address")), int(config_parser.get("server_config","port")))

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
        self.__server_logger.info("[ SERVER ] started listen on ({}:{})".format(self.server_address[0],self.server_address[1]))

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
                        self.__server_logger.info("[ CLIENT ] client just connected {}:{}".format(client_adrr[0],client_adrr[1]))

                        self.socket_server.setblocking(0)
                        self.inputs.append(client_socket)
                        self.message_queue[client_socket] = queue.Queue()
                        self.send_message(client_socket, self.data_to_send)
                    else:
                        self.handle_client(sock)

                for sock in writeable:

                    try:
                        self.data_to_send = self.message_queue[sock].get_nowait()
                    except queue.Empty as qerr:
                        self.__server_logger.exception("[ ERROR ] queue is empty ")
                        sys.exit(1)
                    else:
                        for client in self.inputs[1:]:
                            self.send_message(client,self.data_to_send)


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
            data=client_socket.recv(MAX_RECV_BYTES)
            unpacked_data=json.loads(data.decode("utf-8"))
            print(unpacked_data)
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

        packed_data  = (json.dumps(message)).encode("utf-8")
        print(type(packed_data))
        try:
            client_socket.send(packed_data)
        except IOError as kerr:
            self.__server_logger.error("[ ERROR ] something is wrong with your mother")
        else:
            if client_socket in self.outputs:
                self.outputs.remove(client_socket)

#board access
   def toggleAlarm(self):
        print (1)
        self.data_to_send["Alarma"] = not self.data_to_send["Alarma"]
        if self.data_to_send["Alarma"]:
            print (2)
            my_thread = threading.Thread(target=self.startem, args=())
            my_thread.start()

    def sensor(self):
        print (3)
        time.sleep(2)
        while 1:

            if GPIO.input(pir):
                print (4)
                return True

            if self.data_to_send["Alarma"] == False:
                return False

    def startem(self):
        if self.sensor() == True:
            RELAY.relayON(0, 2)
            for i in range(1, 11)

            RELAY.relayON(0, 1)

            RELAY.relayOFF(0, 2)
            RELAY.relayOFF(0, 1)
            else:
                pass


    def toggleButton(self, relay):
        RELAY.relayTOGGLE(0, relay)
        self.data_to_send["Bec"+str(relay)] = not self.data_to_send["Bec"+str(relay)]
