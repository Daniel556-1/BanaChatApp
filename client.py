import tkinter as tk
import socket
import threading
import uuid
from packet import Packet
import random
import time

# Modes for testing
mode = {
    "lossRate": 0,
    "delay": 0,
    "duplicateRate": 0,
    "reorder": False,
}

def setNormalMode():
    mode.update({
        "lossRate": 0,
        "delay": 0,
        "duplicateRate": 0,
        "reorder": False,
    })
    print("Normal mode activated")

def setLossMode():
    mode.update({
        "lossRate": 0.3,
        "delay": 0,
        "duplicateRate": 0,
        "reorder": False,
    })
    print("Loss mode activated")

def setDelayMode():
    mode.update({
        "lossRate": 0,
        "delay": 1,
        "duplicateRate": 0,
        "reorder": False,
    })
    print("Delay mode activated")

def setDuplicateMode():
    mode.update({
        "lossRate": 0,
        "delay": 0,
        "duplicateRate": 1,
        "reorder": False,
    })
    print("Duplicate mode activated")

def setReorderMode():
    mode.update({
        "lossRate": 0,
        "delay": 0,
        "duplicateRate": 0,
        "reorder": True,
    })
    print("Reorder mode activated")

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

buffer = None
tot = 0

# Helper Functions
def wipe():
    for i in root.winfo_children():
        i.destroy()

def sendPacket(packet):
    clientSocket.sendto(packet.packetToBytes(), server_addr)

# Listener
def listen_for_packets():
    global handshake_state, expected_server_seq, buffer, tot
    while True:
        try:
            data, addr = clientSocket.recvfrom(4096)

            if random.random() < mode["lossRate"]:
                print("Dropped Packet")
                continue
            
            if mode["delay"] > 0:
                print("Delayed by " + str(mode["delay"]))
                time.sleep(mode["delay"])

            if mode["reorder"]:
                if buffer is None:
                    buffer = data
                    print("holding a packet")
                else:
                    print("using up buffer")
                    data, buffer = buffer, data
                
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
                ps = packet.sequence

                if expected_server_seq is None:
                    expected_server_seq = ps + 1
                    
                    ack = Packet(sequence, ps + 1, ["ACK"], "", room, username)
                    sequence += 1
                    sendPacket(ack)

                    message = f"{packet.user}: {packet.payload}"
                    chat_display.config(state = "normal")
                    chat_display.insert(tk.END, message + "\n")
                    chat_display.config(state = "disabled")
                    chat_display.see(tk.END)
                    tot += 1
                    print(tot)
                    continue
                if ps == expected_server_seq:
                    expected_server_seq += 1

                    ack = Packet(sequence, ps + 1, ["ACK"], "", room, username)
                    sequence += 1
                    sendPacket(ack)

                    message = f"{packet.user}: {packet.payload}"
                    chat_display.config(state = "normal")
                    chat_display.insert(tk.END, message + "\n")
                    chat_display.config(state = "disabled")
                    chat_display.see(tk.END)
                    tot += 1
                    print(tot)
                    continue
                elif ps < expected_server_seq:
                    ack = Packet(sequence, ps + 1, ["ACK"], "", room, username)
                    sequence += 1
                    sendPacket(ack)
        except:
            continue

listener_thread = threading.Thread(target = listen_for_packets, daemon = True)
listener_thread.start()

# Pages
def mainMenu():
    wipe()
    background = tk.Frame(root, bg = "lightblue")
    background.pack(expand = True, fill = "both")

    modeFrame = tk.Frame(background, bg = "lightblue")
    modeFrame.place(x = 10, y = 10)

    tk.Button(modeFrame, text = "Normal", font=("Sans Serif", 10), command = setNormalMode).pack(side = "left", padx = 2, pady = 2)
    tk.Button(modeFrame, text = "Loss", font=("Sans Serif", 10), command = setLossMode).pack(side = "left", padx = 2, pady = 2)
    tk.Button(modeFrame, text = "Delay", font=("Sans Serif", 10), command = setDelayMode).pack(side = "left", padx = 2, pady = 2)
    tk.Button(modeFrame, text = "Dupe", font=("Sans Serif", 10), command = setDuplicateMode).pack(side = "left", padx = 2, pady = 2)
    tk.Button(modeFrame, text = "Reorder", font=("Sans Serif", 10), command = setReorderMode).pack(side = "left", padx = 2, pady = 2)

    frame = tk.Frame(background)
    frame.place(relx = 0.5, rely = 0.5, anchor = "center")

    title = tk.Label(frame, text = "Banana Chat App", font = ("Sans Serif", 30, "bold"))
    title.pack(pady=20)

    prompt = tk.Label(frame, text = "Please enter a room name:", font = ("Sans Serif", 16))
    prompt.pack(pady=10)

    roomname_entry = tk.Entry(frame, font = ("Sans Serif", 16))
    roomname_entry.pack(pady = 10)

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
    chat_display = tk.Text(frame, state = "disabled", width = 60, height = 20)
    chat_display.pack(pady = 10)

    message_entry = tk.Entry(frame, font = ("Sans Serif", 16), width = 40)
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

    send_button = tk.Button(frame, text = "Send", font = ("Sans Serif", 16), command=sendMessage)
    send_button.pack(pady = 5)

# Start
mainMenu()
root.mainloop()