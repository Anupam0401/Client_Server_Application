# ***PROBLEM STATEMENT***

# Revise echo client and server to be protocol independent 
# (support both IPv4 and IPv6).


# The code for the server starts here
import socket
import time
import random
from datetime import datetime

# Start with a display message
print('''
**************************************************************
*                       WELCOME!                             *
*                 This is the server                         *
**************************************************************
## This is same as the UDP Echo Client server created in PART 1.1
## The differnce is that this is protocol independent    #########
## (support both IPv4 and IPv6).                         #########
## Just enter the Server host according to your choice   #########
## When running on local machine, the hosts are:         #########
## For IPv4: localhost; For IPv6: ip6-localhost          #########
''')

# serverIP = '127.0.0.1'
serverPort = 20001
serverPublicIP = socket.gethostbyname(socket.gethostname())

bufferSize = 1024

# Taking the server Host from the user which depicts whether the protocol is IPv4 or IPv6
serverHost = input("Enter the Server Host: ")


ACKmessage = "Packet Acknowledged!"
encodedACKmessage = ACKmessage.encode()

# We need to make the echo client server protocol independent
# So, instead of creating the socket for a fixed family
# We will create the socket based on the Server Host Name entered by the used
# And then bind to the correct family based on the client's request

# For doing this, we use the getaddrinfo() function which return a list of tuples that contain information about the socket
# The synatx for it is: socket.getaddrinfo(host, port, family, type)
socketAddrInfo = socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_DGRAM)

# We take the first tuple from the list of tuples in socketAddrInfo
firstInfo = socketAddrInfo[0] #First tuple

# The first tuple obtained from the list of tuples in socketAddrInfo contains the following information
# (family, type, proto, canonname, sockaddr)
# So, we can use the first tuple to create the UDPsocket

# Creation of UDP Socket on Client's Side based on the family obtained from the socketAddrInfo
serverSocket = socket.socket(family=firstInfo[0], type=firstInfo[1])
socketAddress = (serverHost, serverPort)

# Bind the socket to the address
serverSocket.bind(socketAddress)

print(f"UDP Server is up and running on address {serverPublicIP} : {serverPort}")


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