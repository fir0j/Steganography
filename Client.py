#!/usr/bin/python

import socket
import Image
import stepic

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER_IP = raw_input("Enter the Server IPaddess you want to connect: ")
SERVER_PORT = int(input("Enter the Port no. Server is Operating on: "))
ADDRESS = (SERVER_IP, SERVER_PORT)

try:
    print("Trying to Connect.... ", ADDRESS)
    SOCKET.connect(ADDRESS)
    print("Connection Successful\n")

    IMAGE_NAME = raw_input("Enter the Absolute path of your Image: ")
    image1 = Image.open(IMAGE_NAME)
    print("Take a look at Your Image")
    image1.show()
    CIPHERTEXT = raw_input(
        "Enter The Message You want to embed into it:\n-------------------------------------------------------------\n")
    print("-------------------------------------------------------------\n")
    steg = stepic.encode(image1, CIPHERTEXT)
    print("Your Message has been Embedded into the image")
    # steg = stepic.encode(i, text)
    steg.save("stegnofied.png", "PNG")

    IMFILE = open("stegnofied.png", "rb")
    BYTES = IMFILE.read()
    SIZE = len(BYTES)

    # print("Sending Image size to the Server: %s" % SIZE)
    SOCKET.sendall("SIZE 513286".encode('utf-8'))
    answer = SOCKET.recv(4096)
    answer = answer.decode('utf-8')

    if answer == "GOT SIZE":
        SOCKET.sendall(BYTES)

    # check what the server sent on receiving image
    answer = SOCKET.recv(4096)
    answer = answer.decode('utf-8')
    if answer == "GOT IMAGE":
        print("The Image Successfully Sent to the Server")
        # SOCKET.sendall("BYE BYE SERVER :)")
    IMFILE.close()

except Exception as E:
    print(E)

finally:
    SOCKET.close()
