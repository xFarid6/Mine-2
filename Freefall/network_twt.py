import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost" # change this to your server ip address 
            # or domain name if you have one (e.g. "www.mydomain.com") 
            # or leave it as localhost if you are running the server on the same computer as the client (e.g. "localhost") 
            # or leave it as 127.0.0.1 if you are running the server on the same computer as the client (e.g. " localhost ")
            # his was 10.11.250.207
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e: print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)