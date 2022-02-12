# ***PROBLEM STATEMENT***

# Add any two features to Echo Client/Server and demonstrate 
# them. In the report, you must describe the new features with their 
# benefit.

# This is on of the features that I have incorporated
# Transfer of file in Echo client server


# The code for the client starts here:
import socket



# Begin with a display message
print('''
**************************************************************
*                       WELCOME!                             *
*                 This is the Client                         *
**************************************************************
----------------->    FILE VIEWER    <------------------------
**************************************************************
''')


# Initialize the buffer size to 1024
bufferSize = 1024

messageFromClient = "This is a message from Client"
serverIP = '127.0.0.1'
serverPort = 20001
socketAddress = (serverIP, serverPort)
bytesToSend = str.encode(messageFromClient) # client message encoded

# Creation of UDP Socket on Client's Side for IPv4 family
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Timeout setting to interval
UDPSocket.settimeout(1024)

print("You have entered the File Viewer Application based on UDP echo client server\n")

# Get in the infinite loop until the user asks to leave
while True:
    print('''xxxxxxxxxxxxxxxxxxxxxxxxxx MENU xxxxxxxxxxxxxxxxxxxxxxxxxxxx

  # To request a file from the server: press 1
  # To see the list of files available on the server: press 2

  # To exit the File Viewer Application: Press 0
*************************************************************
    ''')
    choice = int(input("\n\nEnter your Choice here: "))
    if choice==0: # If the user wants to exit the application
        break

    elif choice==1:
        # Requesting a file from the server
        fileName = input("Enter the full file name: ")
        msg = str.encode(f"REQFILE {fileName}")
        UDPSocket.sendto(msg, socketAddress)
        print("\n\n")
        # Receiving the ACK from the server
        recievedACK = UDPSocket.recvfrom(bufferSize)
        print(recievedACK[0].decode())
        print("\n\n")
        continue

    elif choice==2:
        # Requesting the list of files from the server
        msg = str.encode(f"LIST")
        UDPSocket.sendto(msg, socketAddress)
        print("\n\n")
        # Receiving the ACK from the server
        recievedACK = UDPSocket.recvfrom(bufferSize)
        print(recievedACK[0].decode())
        print("\n\n")
        continue

    else: # If the user has entered an invalid choice
        print("\nYou have entered an invalid input!\n")
        print("\nPlease enter a valid choice\nRedirecting to the main page...\n")
        continue

    
# Sending of messages completed.
print("The file viewer was successfully completed\nHope you liked it!")

# Send termination message to the server
UDPSocket.sendto(str.encode("TERMINATE"), socketAddress)
serverResponse = UDPSocket.recvfrom(bufferSize)
print(f"Message from the server: {serverResponse}")

print("\n    ------------------------------------\n")

# TERMINATE the socket
UDPSocket.close()