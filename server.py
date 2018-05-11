import socket
import logging
import config
import select

class Server(object):
    def __init__(self,setBlocking=False, server_address = None, reuse_port = True, reuse_address = True, port = 8080):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        if server_address:
            self.server_address=("127.0.0.1",port)
        else:
            self.server_address=(socket.gethostbyname(socket.gethostname()),port)
        
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
                
        
        