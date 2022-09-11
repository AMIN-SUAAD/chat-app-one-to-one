import socket
from threading import Thread

# server's IP address
SERVER_HOST = "localhost"
SERVER_PORT = 8888 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = []
# create a TCP socket
s = socket.socket()

# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)

def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs[1].recv(1024).decode()
            
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")
        # iterate over all connected sockets
        for client_socket in client_sockets:
            if client_socket[0].split(",")[0] == cs[0].split(",")[1]:
            
                # and send the message
                client_socket[1].send(msg.encode())


while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    name = client_socket.recv(1024).decode()
    # add the new connected client to connected sockets
    client_sockets.append((name, client_socket))
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=((name, client_socket),))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()