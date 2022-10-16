import socket
from _thread import *
import sys

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

# Bind the socket to the server socket
try:
    serversocket.bind((server, port))
except socket.error as e:
    print(str(e))


# Create a server socket object
serversocket.listen(2)
print('Waiting for a connection, Server Started')

currentId = "first id"
pos = ["0:50,50", "1:100,100"]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "second id"
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode()
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print('Received: ', reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = "second id"
                if id == 1: nid = "first id"

                reply = pos[1-id][:]
                print('Sending : ', reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print('Lost connection')
    conn.close()

while True:
    # Accept a connection
    conn, addr = serversocket.accept()
    print('Connected to: ', addr)

    # Start a new thread for each client
    start_new_thread(threaded_client, (conn,))

# Have two funcs in the game file that are:
# send_data(data) and get_data()
# these will send data to the server in a certain format and get data back