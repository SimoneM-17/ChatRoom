#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

# handles receiving messages from the server
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkt.END, msg)
        except OSError:  # If client disconnects
            break

# handles sending messages to the server
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")  # Clear the input field
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        window.quit()

def on_closing(event=None):
    my_msg.set("{quit}")
    send()

# Sets up the GUI window
window = tkt.Tk()
window.title("ChatRoom")

messages_frame = tkt.Frame(window)
my_msg = tkt.StringVar()
my_msg.set("Write your messages here.")
scrollbar = tkt.Scrollbar(messages_frame)

# Listbox to display messages
msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
messages_frame.pack()

# Entry field for typing messages
entry_field = tkt.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", send)

entry_field.pack()
send_button = tkt.Button(window, text="Enter", command=send)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

# Gets the server host and port from the user
HOST = input('Enter the server host: ')
PORT = input('Enter the port of the server host: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

# Creates a socket and connect to the server
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# Starts the thread for receiving messages
receive_thread = Thread(target=receive)
receive_thread.start()
tkt.mainloop()  # Start the GUI loop