import socket
import sys
import select
import datetime

class ClientChat(object):

    MAX_RECV_BYTES = 1024

    def __init__(self, server_address):

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Trying to connect to {}... ".format(server_address[0], server_address[1]))
        try:
            self.client_socket.connect(server_address)
        except socket.error as serr:
            print("Failed to connect to server")
            sys.exit(1)
        else:
            print("Client connected ... ")

        self.inputs = [ sys.stdin , self.client_socket ]

    def send_message(self, message):

        try:
            self.client_socket.send(message.encode("utf-8"))
        except IOError as ierr:
            print("Error on sending data...")
            sys.exit(1)

    def recv_message(self, sock):
        try:
            recv_message = sock.recv(ClientChat.MAX_RECV_BYTES)
        except IOError as ierr:
            sys.exit(1)
        else:
            return recv_message.decode("utf-8")

    def connect_forever(self):

        while True:
            try:
                readable, writeable, exception = select.select(self.inputs, [], [])
                for sock in readable:
                    if sock == self.client_socket:
                        message = self.recv_message(sock)
                        print("[{}]: {}".format(datetime.datetime.now(),message))
                    else:
                        message = sys.stdin.readline()
                        self.send_message(message)
            except KeyboardInterrupt as kerr:
                self.client_socket.close()
                sys.exit(0)

if __name__=="__main__" :
    clt_obj = ClientChat(("10.10.0.193", 8080))
    clt_obj.connect_forever()
