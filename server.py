# This class is where we are going to use UDP and then use that to simulate the 3 way TCP handshake.
# The way this works is that every time a packet is going to send, we're gonna use the 3 way TCP handshake
# to verify. In this sense, we won't be using a concurrent connection, but rather use a brand new connection
# each time.

import socket
import random
import time
from packet import Packet

chatrooms = {}

# client states: 1 = syn, 2 = synack, 
clients = {}

# UDP
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(("0.0.0.0", 6789))

def recievePacket(payload, source):
    packet = Packet.bytesToPacket(payload)

    if source not in clients:
        clients[source] = {
            "state": "NIL",
            "serverSeqNum": random.randint(1, 999999999),
        }

    state = clients[source]["state"]
    serverSeqNum = clients[source]["serverSeqNum"]

    print(source)

    if packet.hasSynFlag() == True and packet.hasAckFlag() == False:
        print("SYN recieved from " + str(source))
        
        synAck = Packet(serverSeqNum, packet.sequence + 1, ["SYN", "ACK"], {})
        serverSocket.sendto(synAck.packetToBytes(), source)
        print("SYNACK sent to " + str(source))

        clients[source]["serverSeqNum"] += 1
        clients[source]["state"] = "SYNACK"
        return
    elif packet.hasSynFlag() == True and packet.hasAckFlag() == True and clients[source]["state"] == "SYNACK":
        print("ACK recieved so connection established with " + str(source))
        clients[source]["state"] = "CONNECTED"
        return
    elif clients[source]["state"] == "CONNECTED":
        print("Packet recieved from " + str(source) + ": ")
        print(packet)

while True:
    try:
        data, addr = serverSocket.recvfrom(4096)
        recievePacket(data, addr)
    except BlockingIOError:
        pass

    time.sleep(0.01)