# This class is where we are going to use UDP and then use that to simulate the 3 way TCP handshake.
# The way this works is that every time a packet is going to send, we're gonna use the 3 way TCP handshake
# to verify. In this sense, we won't be using a concurrent connection, but rather use a brand new connection
# each time.

import threading
import socket
from packet import Packet

