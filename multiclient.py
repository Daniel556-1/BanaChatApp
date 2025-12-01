import subprocess
import sys
import os

NUM_CLIENTS = 2

CLIENT_SCRIPT = os.path.join(os.path.dirname(__file__), "client.py")

def launch_client(index):
    subprocess.Popen([sys.executable, CLIENT_SCRIPT])

if __name__ == "__main__":
    for i in range(NUM_CLIENTS):
        launch_client(i)