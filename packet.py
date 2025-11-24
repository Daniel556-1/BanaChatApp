import json

# For the "TCP" headers that we are going to make using UDP, we will be using a json. Although this might not
# be as space efficient as just a string and parsing through it, it is a lot more easier to manipulate
class Packet:

    def __init__(self, sequence = 0, ack = 0, flags = [], payload = {}):
        self.sequence = sequence
        self.ack = ack
        self.flags = flags
        self.payload = payload
    
    def packetToBytes(self):
        return json.dumps({
            "sequence": self.sequence,
            "ack": self.ack,
            "flags": self.flags,
            "payload": self.payload,
        }).encode("utf-8")
    
    def bytesToPacket(bytes):
        bytesJson = json.loads(bytes.decode("utf-8"))
        return Packet(
            sequence = bytesJson.get("sequence", 0),
            ack = bytesJson.get("ack", 0),
            flags = bytesJson.get("flags", []),
            payload = bytesJson.get("payload", {}),
        )
    
    def hasSynFlag(self):
        for i in self.flags:
            if i == "SYN":
                return True
        return False
    
    def hasAckFlag(self):
        for i in self.flags:
            if i == "ACK":
                return True
        return False
    
    def hasFinFlag(self):
        for i in self.flags:
            if i == "FIN":
                return True
        return False
