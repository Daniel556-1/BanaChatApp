# This class is where we are going to use UDP and then use that to simulate the 3 way TCP handshake.
# The way this works is that every time a packet is going to send, we're gonna use the 3 way TCP handshake
# to verify. In this sense, we won't be using a concurrent connection, but rather use a brand new connection
# each time.

import socket
import random
import time
import uuid
from packet import Packet

chatrooms = {}
clients = {}

# UDP
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(("0.0.0.0", 6789))

def sendPacketWithRetransmit(packet, addr):
    clients[addr]["lastSentPacket"] = packet
    clients[addr]["awaitingAck"] = True
    clients[addr]["lastSentTime"] = time.time()
    clients[addr]["expectedAck"] = packet.sequence + 1
    serverSocket.sendto(packet.packetToBytes(), addr)

def recievePacket(payload, source):
    packet = Packet.bytesToPacket(payload)

    if source in clients:
        state = clients[source]["state"]
        serverSeqNum = clients[source]["serverSeqNum"]

    print(source)

    # SYNACK
    if packet.hasSynFlag() == True and packet.hasAckFlag() == False and (source not in clients or (source in clients and clients[source]["state"] not in ["SYNACK", "CONNECTED"] and clients[source]["awaitingAck"] == False)):
        print("SYN recieved from " + str(source))

        if source not in clients:
            clients[source] = {
                "state": "NIL",
                "serverSeqNum": random.randint(1, 999999999),
                "lastSentPacket": None,
                "awaitingAck": False,
                "lastSentTime": 0,
                "expectedAck": None,
                "retransmit": 0,
                "expectedClientSeq": None,
                "roomName": "",
            }

            state = clients[source]["state"]
            serverSeqNum = clients[source]["serverSeqNum"]
        
        synAck = Packet(serverSeqNum, packet.sequence + 1, ["SYN", "ACK"], {})
        sendPacketWithRetransmit(synAck, source)
        print("SYNACK sent to " + str(source))

        clients[source]["serverSeqNum"] += 1
        clients[source]["state"] = "SYNACK"
        return
    
    # WELCOME (4th handshake with the payload of everything)
    elif source in clients and packet.hasSynFlag() == True and packet.hasAckFlag() == True and clients[source]["state"] == "SYNACK":
        
        if source in clients and clients[source].get("awaitingAck") == True:
            if packet.ack == clients[source]["expectedAck"]:
                clients[source]["awaitingAck"] = False
                clients[source]["lastSentPacket"] = None
                clients[source]["expectedAck"] = None
                clients[source]["retransmit"] = 0
                print("Recieved ACK from " + str(source))
        
        print("ACK recieved so connection established with " + str(source))
        clients[source]["state"] = "WELCOME"

        uniqueUser = packet.user + str(uuid.uuid4())

        welcomePacket = Packet(
            serverSeqNum,
            packet.sequence + 1,
            flags = ["WELCOME"],
            payload = {
                "message": "Connection Established",
                "room": packet.room,
                "username": uniqueUser,
            },
            room = packet.room,
            user = uniqueUser,
        )

        sendPacketWithRetransmit(welcomePacket, source)
        print("Welcome packet sent to " + str(source))

        clients[source]["serverSeqNum"] += 1
        return
    
    # 5th handshake final ack for connection
    elif source in clients and clients[source]["state"] == "WELCOME":
        if source in clients and clients[source].get("awaitingAck") == True:
            if packet.ack == clients[source]["expectedAck"]:
                clients[source]["awaitingAck"] = False
                clients[source]["lastSentPacket"] = None
                clients[source]["expectedAck"] = None
                clients[source]["retransmit"] = 0
                print("Recieved final connection ACK from " + str(source))

                clients[source]["state"] = "CONNECTED"

                if packet.room in chatrooms:
                    chatrooms[packet.room].add(source)
                else:
                    chatrooms[packet.room] = {source}
                clients[source]["roomName"] = packet.room

                clients[source]["expectedClientSeq"] = packet.sequence + 1
                print("Client " + str(source) + " fully connected")
                return
    
    # Connected packet recieval
    elif source in clients and clients[source]["state"] == "CONNECTED":
        if source in clients and packet.hasAckFlag() and clients[source].get("awaitingAck") == True:
            if packet.ack == clients[source]["expectedAck"]:
                clients[source]["awaitingAck"] = False
                clients[source]["lastSentPacket"] = None
                clients[source]["expectedAck"] = None
                clients[source]["retransmit"] = 0
                print("Recieved ACK from " + str(source))

        if clients[source]["expectedClientSeq"] is not None:
            if packet.sequence != clients[source]["expectedClientSeq"]:
                print("Packet ignored from " + str(source) + " for bad seq num")
                return
            clients[source]["expectedClientSeq"] = packet.sequence + 1
        
        # Broadcast to everyone in the same room
        
        room = packet.room
        if room in chatrooms:
            for client_addr in chatrooms[room]:

                forward_packet = Packet(
                    clients[client_addr]["serverSeqNum"],
                    packet.sequence,                     
                    flags=packet.flags,
                    payload=packet.payload,
                    room=room,
                    user=packet.user
                )

                sendPacketWithRetransmit(forward_packet, client_addr)
                clients[client_addr]["serverSeqNum"] += 1
        
        return
    else:
        print("Packet ignored from " + str(source))
        return


while True:
    try:
        data, addr = serverSocket.recvfrom(4096)
        recievePacket(data, addr)
    except BlockingIOError:
        pass
    
    inactiveUser = set()
    for addr, info in clients.items():
        
        if info["retransmit"] > 10:
            inactiveUser.add(addr)
        if info.get("awaitingAck") and info.get("lastSentPacket") and time.time() - info["lastSentTime"] > 2:
            print("Retransmitting packet to " + str(addr))
            serverSocket.sendto(info["lastSentPacket"].packetToBytes(), addr)
            info["retransmit"] += 1
            info["lastSentTime"] = time.time()
        
        if time.time() - info["lastSentTime"] > 600:
            inactiveUser.add(addr)

    for i in inactiveUser:
        chatrooms[clients[i]["roomName"]].discard(i)
        clients.pop(i)

    time.sleep(0.01)