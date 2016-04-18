# Echo server program
import socket
from Constants import HOST
from Constants import PORT


class _Network:
    def __init__(self, do, send):
        self.do = do
        self.send = send
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_receive(self):
        while True:
            data = self.sock.recv(1024)
            unpacked = data.decode()
            self.execute(unpacked)

            if not self.send.empty():
                data = self.send.get(False)  # Does not wait for actions to contain something
            else:
                data = ' '

            packed = data.encode()
            self.sock.sendall(packed)

    def start_send(self):
        while True:
            if not self.send.empty():
                data = self.send.get(False)  # Does not wait for actions to contain something
            else:
                data = ' '

            packed = data.encode()
            self.sock.sendall(packed)

            data = self.sock.recv(1024)
            unpacked = data.decode()
            self.execute(unpacked)

    def execute(self, command):
        if not command == ' ':
            self.do.put(eval(command))


class Server(_Network):
    def __init__(self, do, send):
        _Network.__init__(self, do, send)
        self.isServer = True
        self.sock.bind((HOST, PORT))
        self.sock.listen(1)
        self.sock, addr = self.sock.accept()  # Wait for connect
        self.send.put('Start it!')

        self.start_receive()


class Client(_Network):
    def __init__(self, do, send):
        _Network.__init__(self, do, send)
        self.isServer = False
        self.sock.connect((HOST, PORT))
        self.send.put('Start it!')

        self.start_send()


