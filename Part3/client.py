# ***PROBLEM STATEMENT***

# Revise echo client and server to be protocol independent 
# (support both IPv4 and IPv6).


# The code for the client starts here:
import socket
import sys
import time
import datetime
import argparse

# # Input the required parameters using the normal input method
# totalMessages = int(input("Enter the total number of packets: "))
# messageInterval = float(input("Enter the Interval size: "))
# packetSize = int(input("Enter the Packet size: "))

# Input the required parameters using the argparse method
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--total-number-of-packets", help="Enter the total number of packets", type=int, dest="total_messages")
parser.add_argument("-i", "--interval", help="Enter the Interval size", type=float, dest="message_interval")
parser.add_argument("-s", "--size", help="Enter the Packet size", type=int, dest="packet_size")
args = parser.parse_args()

# Begin with a display message
print('''
**************************************************************
*                       WELCOME!                             *
*                 This is the Client                         *
**************************************************************
## This is same as the UDP Echo Client server created in PART 1.1
## The differnce is that this is protocol independent    #########
## (support both IPv4 and IPv6).                         #########
## Just enter the Server host corrosponding to the server ########
## When running on local machine, the hosts are:         #########
## For IPv4: localhost; For IPv6: ip6-localhost          #########
''')

# Assign the values obtained from the ArgumentParser
totalMessages = args.total_messages
messageInterval = args.message_interval
packetSize = args.packet_size

# Since window size is same as packetSize, we can use the same value for window size
bufferSize = packetSize

serverHost = input("Enter the Server Host Name: ")

messageFromClient = "This is a message from Client"
# serverIP = '127.0.0.1'
serverPort = 20001
bytesToSend = str.encode(messageFromClient) # client message encoded
avgRTT = 0 # Initializing the average RTT
packetSuccessCount = 0 # Initializing the success count of packets

socketAddrInfo = socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_DGRAM)
firstInfo = socketAddrInfo[0] #First tuple

# Creation of UDP Socket on Client's Side for the protocol family that is taken from the user
UDPSocket = socket.socket(family=firstInfo[0], type=firstInfo[1])

socketAddress = (serverHost, serverPort)

# Timeout setting to interval
UDPSocket.settimeout(messageInterval)

# Callibrating the buffer size
# To adjust the window size, we send the message to the server with ADJ denoting Adjustment
msg = str.encode(f"ADJ {packetSize}")
print("\n")
# Sending the message to the server
UDPSocket.sendto(msg, socketAddress)

# Receiving the ACK from the server
recievedACK = UDPSocket.recvfrom(bufferSize) 

print(recievedACK[0].decode())
print("\n\n")

packetCount = 0 # defined for calculating RTT and loss percentage

while(totalMessages > 0):
    packetCount += 1
    totalMessages -= 1
    print("\n                   ***\n")
    print(f"Sending packet number {packetCount} of {packetSize} bytes...")
    sendTimestamp = datetime.datetime.now().timestamp() # Time at which the packet is sent

    # Sending the packet to the server
    UDPSocket.sendto(bytesToSend, socketAddress)

    try:
        # Receiving the ACK from the server
        recievedACK = UDPSocket.recvfrom(bufferSize) 
    except socket.timeout:
        # Server timeout leads to packet loss
        print("\nPACKET LOST!!\n")
        continue

    recievingTimestamp = datetime.datetime.now().timestamp() # Time at which the packet is recieved
    
    print(f"Message from the server: {recievedACK}")
    print("\n\n")
    print(f"Packet number {packetCount} recieved successfully")
    packetSuccessCount += 1
    print(f"Round Trip Time for packet {packetCount} is {recievingTimestamp-sendTimestamp}")
    print("\n")

    # Calculating the average RTT
    avgRTT += recievingTimestamp-sendTimestamp

    # Until the current interval is not over, the process is paused by making it sleep for the left time
    delay = recievingTimestamp-sendTimestamp
    if(delay < messageInterval):
        time.sleep(messageInterval-delay)
    
# Sending of messages completed.
print("Process of Sending Packets has completed!\n")
# Send termination message to the server
UDPSocket.sendto(str.encode("TERMINATE"), socketAddress)
serverResponse = UDPSocket.recvfrom(bufferSize)
print(f"Message from the server: {serverResponse}")
print("\n\n")

# Calculating the Average RTT
avgRTT = avgRTT/packetSuccessCount
print(f"Average Round Trip Time is {avgRTT}")

# Calculating the loss percentage
lossPercentage = (1 - (packetSuccessCount/packetCount))*100
print(f"Loss Percentage is {lossPercentage}%")
print("The program is complete and is Protocol Independent\n")
print("    ------------------------------------")
print("\n")

# TERMINATE the socket
UDPSocket.close()