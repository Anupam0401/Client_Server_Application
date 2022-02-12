# ***PROBLEM STATEMENT***

# Add any two features to Echo Client/Server and demonstrate 
# them. In the report, you must describe the new features with their 
# benefit.

# This is one of the features that I have incorporated
# INTERACTIVE MESSAGING in Echo client server


# The code for the client starts here:
import socket
import datetime
import pickle



# Begin with a display message
print('''
**************************************************************
*                       WELCOME!                             *
*                 This is the Client                         *
**************************************************************
-------------->    INTERACTIVE MESSAGING    <-----------------
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

# packetCount = 0 

print("You have entered the INTERACTIVE EXPLORATION Application based on UDP echo client server\n")
print("You can send a message to the server and know something interesting and new about yourself.\n")

# Get in the infinite loop until the user asks to leave
while True:
    print('''xxxxxxxxxxxxxxxxxxxxxxxxxx MENU xxxxxxxxxxxxxxxxxxxxxxxxxxxx

  # To send a message to the server: press 1
  # To know something really interesting yourself: press 2

  # To exit the INTERACTIVE EXPLORATION: Press 0
*************************************************************
    ''')
    choice = int(input("\n\nEnter your Choice here: "))
    if choice==0: # If the user wants to exit the application
        break

    
    elif choice==1:
        # Send the message to the server
        # print("Sending the message to the server")
        # Store the current timeStamp
        timeStamp = datetime.datetime.now()
        msg=input(("\nEnter a message to send to the server: "))
        msg = str.encode(f"MESSAGE {msg}") # message encoded
        UDPSocket.sendto(msg, socketAddress)
        print(f"\n\nMessage sent to the server at {timeStamp}")
        print("Waiting for the server to send the message back")

        # Receive the message from the server
        print("\nReceiving the message from the server\n\n")
        messageFromServer, serverAddress = UDPSocket.recvfrom(bufferSize)
        timeStamp = datetime.datetime.now()
        print(f"Message received from the server at {timeStamp}\n")
        print("Message from the server: " + str(messageFromServer.decode()))
        print("\n\n")

    elif choice==2:
        # Explore yourself
        # Input the date of birth from the user
        dateOfBirth = input("Enter your date of birth (format: DD-MM-YYYY): ") # 04-01-2002
        # Send the date of birth to the server by passing it with DOB tag
        msg = str.encode(f"DOB-EXPLORE {dateOfBirth}")
        UDPSocket.sendto(msg, socketAddress)
        print("\n\n")
        print("Your Date Of Birth has been sent to the server.\n")
        # Receive the array of data from the server
        print("Receiving the array of data from the server\n")
        # Recieve the array data from the server using the pickle method
        dataRecieved, serverAddress = UDPSocket.recvfrom(bufferSize)
        dataFromServer = pickle.loads(dataRecieved) # deserialize the data stream using the loads method
        # dataFromServer, serverAddress = UDPSocket.recvfrom(bufferSize)
        age = dataFromServer[0]
        greeting = dataFromServer[1]
        astrologicalSign = dataFromServer[2]
        personality = dataFromServer[3]
        print(f"\nThe message from the server is:\n")
        print(f"{greeting} client!\n\nHere are the informations about you which you might not have known:-\nYour Age is {age}\nYour Astrological Sign is {astrologicalSign}\n{personality}\n\n")


    else: # If the user has entered an invalid choice
        print("\nYou have entered an invalid input!\n")
        print("\nPlease enter a valid choice\nRedirecting to the main page...\n")
        continue

    
# Sending of messages completed.
print("The Interactive Messaging Service has completed successfully!\nHope you liked it!\n")

print("Ending the service...\n")
# Send termination message to the server
UDPSocket.sendto(str.encode("TERMINATE"), socketAddress)
serverResponse = UDPSocket.recvfrom(bufferSize)
print(f"Message from the server: Connection Terminated")

print("\n    ------------------------------------\n")

# TERMINATE the socket
UDPSocket.close()