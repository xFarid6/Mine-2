import socket, struct

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost" #
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        self.pos = self.connect()
        self.pos = self.pos.decode()
        self.pos = self.pos.split(",")
        self.pos = [int(self.pos[0]), int(self.pos[1])]
        print(self.pos)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048)
        except:
            pass
        return None

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
            return None

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def main():
    n = Network()
    print(n.pos)
    while True:
        n.send(make_pos((0, 0)))
        print(read_pos(n.send(make_pos((0, 0)))))

main()
'''/*
 * Licensed to the Apache Software Foundation (ASF) under one
    * or more contributor license agreements.  See the NOTICE file
    * distributed with this work for additional information
    * regarding copyright ownership.  The ASF licenses this file
    * to you under the Apache License, Version 2.0 (the
    * "License"); you may not use this file except in compliance
    * with the License.  You may obtain a copy of the License at
    *
    *   http://www.apache.org/licenses/LICENSE-2.0
    *
    * Unless required by applicable law or agreed to in writing,
    * software distributed under the License is distributed on an
    * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    * KIND, either express or implied.  See the License for the
    * specific language governing permissions and limitations
    * under the License.
*/'''
