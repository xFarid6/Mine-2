import socket
from _thread import *

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Assign the socket to the server socket
serversocket.bind(('localhost', 8089))

# Create a server socket object
serversocket.listen(5)

# Accept a connection
connection, client_address = serversocket.accept()

# Receive data from the client_address
data = connection.recv(1024)

# Send data to the client_address
connection.send(data)

# Close the connections socket
connection.close()

# Close the server socket
serversocket.close()

print('Done')
