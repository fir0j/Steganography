#!/usr/bin/python

import socket
import Image
import stepic
import time

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def LocalIP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return IP


SERVER_IP = LocalIP()
SERVER_PORT = int(input("Enter the port on which you want your server to be operated: "))
SOCKET.bind((SERVER_IP, SERVER_PORT))
SOCKET.listen(5)  # no.of simultaneous connections
print("Server Started...Listening....at", SERVER_IP, SERVER_PORT)

CLIENTSOCKET, CLIENTADDRESS = SOCKET.accept()
print("Connection Established with: ", CLIENTADDRESS)
print("Waiting for the client response ...")


def SHOW_IMAGE():
    print("This is the image you have Received\n")
    R_IMG.show()


def DECODE_MESSAGE():
    print("Decoding Message from the receiced Image ...")
    time.sleep(1)
    print("\nYour Message is :\n---------------------------------\n%s\n---------------------------------\n" % IMAGE_DATA)


def BOTH():
    DECODE_MESSAGE()
    SHOW_IMAGE()


def switch(choice):
    switcher = {
        0: SHOW_IMAGE(),
        1: DECODE_MESSAGE(),
        2: BOTH()
    }
    return switcher.get(choice, "Invalid Choice")


try:
    IMAGE_SIZE_BYTES = CLIENTSOCKET.recv(4096)
    IMAGE_SIZE_STRING = IMAGE_SIZE_BYTES.decode('utf-8')

    if IMAGE_SIZE_STRING.startswith("SIZE"):
        TMP_TUPLE = IMAGE_SIZE_STRING.split()
        IMAGE_SIZE = int(TMP_TUPLE[1])
        # print("Image size received Successfully")
        CLIENTSOCKET.sendall("GOT SIZE".encode("utf-8"))

    elif IMAGE_SIZE_STRING.startswith("BYE"):
        SOCKET.close()
    else:
        print("Didn't Received Response from Client")

except Exception as E:
    print("Problem Encountered while exchanging Image size")
    print(E)

try:

    IMAGE_BYTES = CLIENTSOCKET.recv(40960000)
    IMAGE_FILE = open("RECEIVED_IMAGE.png", "wb")
    IMAGE_FILE.write(IMAGE_BYTES)
    IMAGE_FILE.close()
    CLIENTSOCKET.sendall("GOT IMAGE".encode('utf-8'))
    print("Image Received Successfully")
    R_IMG = Image.open("RECEIVED_IMAGE.png")
    s = stepic.decode(R_IMG)
    IMAGE_DATA = s.decode()
    print("\n0. Show the Steganofied Image\n1. Decode the Message from the Received Image \n2. Both\n3. Exit\n")
    flag = True

    while flag:
        choice = int(raw_input("Enter Your Choice: "))
        if (choice == 0):
            SHOW_IMAGE()
        elif (choice == 1):
            DECODE_MESSAGE()
        elif (choice == 2):
            BOTH()
        elif (choice == 3):
            flag = False
        else:
            print("Invalid Choice")

    # choice = 0
    # while(choice < 3):
    #     choice = int(raw_input("Enter Your Choice: "))
    #     switch(choice)

    SOCKET.close()

except Exception as E:
    print("Problem Encountered while exchanging Image")
    print(E)

finally:
    SOCKET.close()
