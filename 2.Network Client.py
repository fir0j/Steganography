#!/usr/bin/python3

import socket

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER_IP = input("Enter the Server IPaddess you want to connect: ")
SERVER_PORT = int(input("Enter the Port no. Server is Operating on: "))
ADDRESS = (SERVER_IP, SERVER_PORT)

try:
    print("Trying to Connect.... ", ADDRESS)
    SOCKET.connect(ADDRESS)
    print("Connection Successful\n")

    IMFILE = open("myimage.png", "rb")
    BYTES = IMFILE.read()
    SIZE = len(BYTES)

    print("Sending Image size to the Server: %s" % SIZE)
    SOCKET.sendall("SIZE 513286".encode('utf-8'))
    answer = SOCKET.recv(4096)
    answer = answer.decode('utf-8')

    if answer == "GOT SIZE":
        SOCKET.sendall(BYTES)

    # check what the server sent on receiving image
    answer = SOCKET.recv(4096)
    answer = answer.decode('utf-8')
    if answer == "GOT IMAGE":
        print("Image Successfully Sent to the Server")
        # SOCKET.sendall("BYE BYE SERVER :)")
    IMFILE.close()

except Exception as E:
    print(E)

finally:
    SOCKET.close()
