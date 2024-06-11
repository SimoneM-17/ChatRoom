#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# accepts new client connections
def accept_connection():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s connected." % client_address)
        client.send(bytes("Please enter your name and press Enter", "utf8"))
        addresses[client] = client_address
        Thread(target=manage_client, args=(client,)).start()

# manages communication with a connected client
def manage_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome to the chat %s. Write {quit} to leave.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s joined the chat" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s left the chat." % name, "utf8"))
            break

# sends messages to all clients
def broadcast(msg, prefix=""):
    for user in clients:
        user.send(bytes(prefix, "utf8")+msg)

# dictionaries to keep track of clients and their addresses
clients = {}
addresses = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

# creates a server socket
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)  # Listen for incoming connections
    print("Waiting for a new connection...")
    ACCEPT_THREAD = Thread(target=accept_connection)
    ACCEPT_THREAD.start()  # Start the thread to accept connections
    ACCEPT_THREAD.join()  # Wait for the thread to complete
    SERVER.close()  # Close the server
