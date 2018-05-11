import socket
import logging
import config
import select
import struct

class Server(object):
    def __init__(self,setBlocking=False, server_address = None, reuse_port = True, reuse_address = True, port = 8080):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        if server_address:
            self.server_address=("127.0.0.1",port)
        else:
            self.server_address=(socket.gethostbyname(socket.gethostname()),port)
        
        self.data_struct = struct.Struct("I")
        try:
            self.socket_server.bind(server_address)
        except:
            pass
        if setBlocking:
            self.socket_server.setblocking(1)
        
        if reuse_port:
            self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            
        self.server_socket.listen(5)
        
        self.input = [self.socket_server]
        self.output = []
        
        
    def start_server():
        self.server_status = True    
            while self.server_status:
                readable, writeable, exceptional = select.select(input, output, input)
            
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
    
