# Banana Chat App
Welcome to Team Banana's chat app! In this readme, you will learn about a basic overview of the code and how to run it.

## High level overview
This chat app mainly consists of 2 parts. The client and the server. The goal of this chat application is to use UDP to create a TCP-like protcol. In doing so, we are able to fully control retransmission, handshakes, and more. The main difference between our TCP and the real TCP is that our TCP is built off of UDP and has packet headers that include chat application specific fields. We also use a 5-way handshake instead of a 3-way handshake as there are some things that must happen every time a connection is established and it makes sense to place them in the handshake.

## How to run
Please open up two terminals that have python in the PATH and run these commands (keep in mind to fill in the blanks these are not actual python commands until you find the file path):
```python
pathToPython pathTo[client.py]
```
OR this for multiple clients
```python
pathToPython pathTo[multiclient.py]
```

Then on the other terminal run this to start the server:
```python
pathToPython pathTo[server.py]
```

## Client.py

This is the main client python script. It includes the clienside TCP logic, home page, and the chat page.

### multiclient.py

This is a python script that opens multiple of the client. The amount can be customized in the script.

## Packet.py

This is just a helper class for the client and the server to have the same packet objects.

## Server.py

This is the server that handles the server-side TCP logic and server-side chat logic. It handles retransmission and other TCP features.
