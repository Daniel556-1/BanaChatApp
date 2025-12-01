import tkinter as tk
import socket
import threading
import uuid
from packet import Packet

# App setup
root = tk.Tk()
root.geometry("1000x600")
root.resizable(False, False)
root.title("Banana Chat App Client")

# Networking
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ("127.0.0.1", 6789)

sequence = 1
handshake_state = "NIL"
expected_server_seq = None
room = ""
username = "User-" + str(uuid.uuid4())

# Helper Functions
def wipe():
    for i in root.winfo_children():
        i.destroy()

def sendPacket(packet):
    clientSocket.sendto(packet.packetToBytes(), server_addr)

# Listener
def listen_for_packets():
    global handshake_state, expected_server_seq
    while True:
        try:
            data, addr = clientSocket.recvfrom(4096)
            packet = Packet.bytesToPacket(data)

            if "SYN" in packet.flags and "ACK" in packet.flags and handshake_state == "SYN_SENT":
                expected_server_seq = packet.sequence + 1
                handshake_state = "SYNACK_RECEIVED"
                global sequence
                pk = Packet(sequence, expected_server_seq, ["SYN", "ACK"], "", room, username)
                sequence += 1
                sendPacket(pk)
                print("4th handshake sent")

            elif "WELCOME" in packet.flags and handshake_state == "SYNACK_RECEIVED":
                expected_server_seq = packet.sequence + 1
                handshake_state = "WELCOME_RECEIVED"
                pk = Packet(sequence, expected_server_seq, ["ACK"], "", room, username)
                sequence += 1
                sendPacket(pk)
                handshake_state = "CONNECTED"
                print("Connected to server!")
                chatPage()

            elif handshake_state == "CONNECTED":
                message = f"{packet.user}: {packet.payload}"
                chat_display.config(state = "normal")
                chat_display.insert(tk.END, message + "\n")
                chat_display.config(state = "disabled")
                chat_display.see(tk.END)
        except:
            continue

listener_thread = threading.Thread(target=listen_for_packets, daemon=True)
listener_thread.start()

# Pages
def mainMenu():
    wipe()
    background = tk.Frame(root, bg="lightblue")
    background.pack(expand=True, fill="both")
    frame = tk.Frame(background)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    title = tk.Label(frame, text="Banana Chat App", font=("Sans Serif", 30, "bold"))
    title.pack(pady=20)

    prompt = tk.Label(frame, text="Please enter a room name:", font=("Sans Serif", 16))
    prompt.pack(pady=10)

    roomname_entry = tk.Entry(frame, font=("Sans Serif", 16))
    roomname_entry.pack(pady=10)

    def joinRoom():
        global room, handshake_state, sequence
        room = roomname_entry.get()
        handshake_state = "SYN_SENT"
        pk = Packet(sequence, 0, ["SYN"], "", room, username)
        sequence += 1
        sendPacket(pk)
        print("SYN sent")

    button = tk.Button(frame, text="Enter", font=("Sans Serif", 16), command=joinRoom)
    button.pack(pady = 20)

def chatPage():
    wipe()
    background = tk.Frame(root, bg = "lightblue")
    background.pack(expand=True, fill = "both")
    frame = tk.Frame(background)
    frame.place(relx = 0.5, rely = 0.5, anchor = "center")

    un = tk.Label(frame, text = "Username: " + str(username), font = ("Sans Serif", 14))
    un.pack(pady = 10)
    title = tk.Label(frame, text = "Connected to room: " + str(room), font = ("Sans Serif", 14))
    title.pack(pady = 10)

    global chat_display
    chat_display = tk.Text(frame, state="disabled", width = 60, height = 20)
    chat_display.pack(pady = 10)

    message_entry = tk.Entry(frame, font=("Sans Serif", 16), width = 40)
    message_entry.pack(pady = 5)

    def sendMessage():
        global sequence
        msg = message_entry.get()
        if msg.strip() == "":
            return
        pk = Packet(sequence, expected_server_seq, ["CHAT"], msg, room, username)
        sequence += 1
        sendPacket(pk)
        message_entry.delete(0, tk.END)

    send_button = tk.Button(frame, text="Send", font=("Sans Serif", 16), command=sendMessage)
    send_button.pack(pady = 5)

# Start
mainMenu()
root.mainloop()