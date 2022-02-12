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


# The code for the client starts here:
import socket   # Socket implpementation
import time     # Time functions(sleep)
import datetime # getting the Timestamp 
import argparse # Input using arguments

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
# Sample input: python3 client.py -n 10 -i 0.1 -s 1024

# Begin with a display message
print('''
**************************************************************
*                       WELCOME!                             *
*                 This is the Client                         *
**************************************************************
''')

# Assign the values obtained from the ArgumentParser
totalMessages = args.total_messages
messageInterval = args.message_interval
packetSize = args.packet_size

# Since window size is same as packetSize, we can use the same value for window size
bufferSize = packetSize

messageFromClient = "This is a message from Client"
serverIP = '127.0.0.1'
serverPort = 20001
socketAddress = (serverIP, serverPort)
bytesToSend = str.encode(messageFromClient) # client message encoded
avgRTT = 0 # Initializing the average RTT
packetSuccessCount = 0 # Initializing the success count of packets

# Creation of UDP Socket on Client's Side for IPv4 family
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

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
print("\n")

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
        time.sleep(messageInterval-delay) # Sleep for the left
    
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
print("    ------------------------------------")
print("\n")

# TERMINATE the socket
UDPSocket.close()