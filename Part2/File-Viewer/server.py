# ***PROBLEM STATEMENT***

# Add any two features to Echo Client/Server and demonstrate 
# them. In the report, you must describe the new features with their 
# benefit.

# This is on of the features that I have incorporated
# # Transfer of file in Echo client server

# The code for the server starts here
import socket
import os
import time
import random
import datetime

# Start with a display message
print('''
**************************************************************
*                       WELCOME!                             *
*                 This is the server                         *
**************************************************************
**************************************************************
----------------->    FILE VIEWER    <------------------------
**************************************************************
''')

serverIP = '127.0.0.1'
serverPort = 20001
socketAddress = (serverIP, serverPort)
serverPublicIP = socket.gethostbyname(socket.gethostname())

bufferSize = 1024

ACKmessage = "Packet Acknowledged!"
encodedACKmessage = ACKmessage.encode()

# Creation of UDP Socket on Client's Side for IPv4 family
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

    # If the decoded message requests the server to send a list of files available in the server
    if decodedData == "LIST":
        print("Requesting the list of files from the server...")
        # Get the list of files available in the server
        listOfFiles = [f for f in os.listdir('.') if os.path.isfile(f)] 

        # Remove the unnecessary or private files from the list
        listOfFiles.remove('server.py') # Remove the server.py file from the list
        listOfFiles.remove('client.py') # Remove the client.py file from the list

        print(f"Files in the Server: {listOfFiles}")
        # Send the list of files available in the server to the client
        serverSocket.sendto(str.encode(f"Files available in the Server: {listOfFiles}"), clientAddress)
        print("\n")
        continue

    

    # If the decoded message requests the server for file viewing
    if decodedData.split()[0] == "REQFILE":
        print("Sending File...")
        nameOfFile = decodedData.split()[1] # Get the name of the file requested by the client
        file = open(nameOfFile, "rb")  # Open the file in binary mode(r-read, b-binary) binary mode is useful for reading images and other files
        dataInFile = file.read() # Read the data from the file
        file.close() # Close the file
        serverSocket.sendto(dataInFile, clientAddress) # Send the data to the client
        print(f"File Sent: {nameOfFile}") # Print the name of the file sent
        print("\n")
        continue



    # Sending reply to the client with an Acknowledgement message
    serverSocket.sendto(encodedACKmessage, clientAddress)
    print(f"ACK Message: {ACKmessage}")
    

# Close the socket with a message
print("\n\nClosing the Server Socket...")
serverSocket.close()
print("\nServer Socket Closed!")





