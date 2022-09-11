import socket
import random
from threading import Thread
from datetime import datetime

SERVER_HOST = "localhost"
SERVER_PORT = 8888 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()

# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))

# prompt the client for a name
self_name = input("Enter your name to initialize the chat: ")
chat_person = input("Enter the person's name you wish to talk to initialize the chat: ")

name = self_name + ',' + chat_person
s.send(name.encode())

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)


# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    to_send =  input()
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"[{date_now}] {self_name}{separator_token}{to_send}"
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()



