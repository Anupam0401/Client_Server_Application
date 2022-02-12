# ***PROBLEM STATEMENT***

# Create your own UDP echo client and server application 
# to measure round trip time between client and server (similar to “ping” command) 

# The client should create a UDP socket and send echo packets to 
# server at a given interval, number of echo messages, and given 
# packet size (use command line arguments). On reception of the 
# packet, server should send the packet back to the client. The 
# client on reception of the packet should calculate and display the 
# round-trip time. To calculate the round-trip time, you can have 
# the timestamp in the packet or/and use some unique identifier 
# in the packet. You should also calculate and print the loss 
# percentage at the end.

# The code for the server starts here
import socket  # Socket Implementation
import time    # For time delay and sleep
import random  # For creating loss by the use of random number generation

# Start with a display message
print('''
**************************************************************
*                       WELCOME!                             *
*                 This is the server                         *
**************************************************************
''')

serverIP = '127.0.0.1'
serverPort = 20001
socketAddress = (serverIP, serverPort)
serverPublicIP = socket.gethostbyname(socket.gethostname())

bufferSize = 1024

ACKmessage = "Packet Acknowledged!"
encodedACKmessage = ACKmessage.encode()

# Creation of UDP Socket on Server's Side for IPv4 family
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the address
serverSocket.bind(socketAddress)

print(f"UDP Server is up and running on address {serverPublicIP} : {serverPort}")

serverHostname = socket.gethostname()
print(f"Server Hostname: {serverHostname}")

# Listen for incoming connections
while True:
    # Get client requests
    clientRequestData, clientAddress = serverSocket.recvfrom(bufferSize)
    print("\n")
    print(f"Message from the Client: {clientRequestData}")
    print(f"Client Address: {clientAddress}")

    decodedData = clientRequestData.decode()
    print(f"Decoded Data: {decodedData}")

    # If the decoded message required the adjustment of window size
    if decodedData.split()[0] == "ADJ":
        print("Adjusting Window Size...")
        bufferSize = int(decodedData.split(" ")[1])
        print()
        serverSocket.sendto(str.encode(f"Adjusted Window Size to {bufferSize}"), clientAddress)
        print(f"Adjusted Window size to {bufferSize}")
        print("\n")
        continue

    # If the decoded message requests Termination of Connection
    if decodedData == "TERMINATE":
        print("Terminating Connection...")
        serverSocket.sendto(str.encode("Connection Terminated"), clientAddress)
        print("\nConnection Terminated!\n")
        break


    # Introducing Packet Delay
    time.sleep(random.randint(1, 5000) / 1000)

    # Introducing Packet Loss with Loss Probability of 0.1
    if random.randint(1, 10) <= 1:
        print("Packet Loss Occurred!\n")
        continue

    # Sending reply to the client with an Acknowledgement message
    serverSocket.sendto(encodedACKmessage, clientAddress)
    print(f"ACK Message: {ACKmessage}")
    

# Close the socket with a message
print("\n\nClosing the Server Socket...")
serverSocket.close()
print("\nServer Socket Closed!")





