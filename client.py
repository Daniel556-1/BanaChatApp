import tkinter as tk
import socket
from packet import Packet

# App setup
root = tk.Tk()
root.geometry("1000x600")
root.resizable(False, False)
root.title("Banana Chat App Client")

# Packet data
sequence = 1
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# variables
room = ""


# Wipe helper function
def wipe():
    for i in root.winfo_children():
        i.destroy()

def test():
    global sequence
    pk = Packet(sequence, 0, ["SYN"], "Hello server")
    sequence += 1
    clientSocket.sendto(pk.packetToBytes(), ("127.0.0.1", 6789))
    print("SYN packet sent!")

# Main Menu Function
def mainMenu():
    wipe()

    background = tk.Frame(root, bg = "lightblue")
    background.pack(expand = True, fill = "both")

    frame = tk.Frame(background)
    frame.place(relx = 0.5, rely = 0.5, anchor = "center")

    title = tk.Label(frame, text = "Banana Chat App", font = ("Sans Serif", 30, "bold"))
    title.pack(pady = 20, padx = 20)

    prompt = tk.Label(frame, text = "Please enter a room name:", font = ("Sans Serif", 16))
    prompt.pack(pady = 10, padx = 20)

    roomname = tk.Entry(frame, font = ("Sans Serif", 16))
    roomname.pack(pady = 10, padx = 20)

    # Joining room logic here

    button = tk.Button(frame, text = "Enter", font = ("Sans Serif", 16), command = test)
    button.pack(pady = 20, padx = 20)

def connectingPage():
    wipe()

    background = tk.Frame(root, bg = "lightblue")
    background.pack(expand = True, fill = "both")

    frame = tk.Frame(background)
    frame.place(relx = 0.5, rely = 0.5, anchor = "center")

    title = tk.Label(frame, text = "Connecting...", font = ("Sans Serif", 30))
    title.pack(pady = 20, padx = 20)

    # Connection logic here


# Chat Page Function
def chatPage():
    wipe()

    background = tk.Frame(root, bg = "lightblue")
    background.pack(expand = True, fill = "both")

    frame = tk.Frame(background)
    frame.place(relx = 0.5, rely = 0.5, anchor = "center")

    title = tk.Label(frame, text = "Connected to room: ", font = ("Sans Serif", 30))
    title.pack(pady = 20, padx = 20)

# Start
mainMenu()
root.mainloop()