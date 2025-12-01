import json

# For the "TCP" headers that we are going to make using UDP, we will be using a json. Although this might not
# be as space efficient as just a string and parsing through it, it is a lot more easier to manipulate
class Packet:

    def __init__(self, sequence = 0, ack = 0, flags = None, payload = None, room = "public", user = "anon"):
        self.sequence = sequence
        self.ack = ack
        self.flags = flags if flags is not None else []
        self.payload = payload if payload is not None else {}
        self.room = room
        self.user = user
    
    def packetToBytes(self):
        return json.dumps({
            "sequence": self.sequence,
            "ack": self.ack,
            "flags": self.flags,
            "payload": self.payload,
            "room": self.room,
            "user": self.user,
        }).encode("utf-8")
    
    def bytesToPacket(bytes):
        bytesJson = json.loads(bytes.decode("utf-8"))
        return Packet(
            sequence = bytesJson.get("sequence", 0),
            ack = bytesJson.get("ack", 0),
            flags = bytesJson.get("flags", []),
            payload = bytesJson.get("payload", {}),
            room = bytesJson.get("room", "public"),
            user = bytesJson.get("user", "anon"),
        )
    
    def hasSynFlag(self):
        return "SYN" in self.flags
    
    def hasAckFlag(self):
        return "ACK" in self.flags
    
    def hasFinFlag(self):
        return "FIN" in self.flags
    
    def hasWelcomeFlag(self):
        return "WELCOME" in self.flags
    
    def getUsername(self):
        return self.user

    def getRoom(self):
        return self.room
