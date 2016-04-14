# Echo server program
import socket
import pickle
from _thread import *

class Server:
    def __init__(self):
        self.connections = []
        HOST = 'localhost'       # Symbolic name meaning all available interfaces
        PORT = 8880              # Arbitrary non-privileged port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))

        start_new_thread(self.handle_joins, ())
        start_new_thread(self.handle_broadcast(), ())

    def handle_joins(self):
        while True:
            self.s.listen(1)
            conn, addr = self.s.accept()
            print('Connected by', addr)
            self.connections.append(conn)

    def handle_broadcast(self):
        while True:
            datas = []
            for conn in self.connections:
                data = conn.recv(1024)
                datas.append(data.decode())
            for conn in self.connections:
                conn.sendall(str(datas).encode())



class Client:
    def __init__(self):
        HOST = 'localhost'  # The remote host
        PORT = 8880  # The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        while True:
            s.sendall(b'Username')
            data = s.recv(1024)
            print(eval(data.decode()))
        s.close()
