# ***PROBLEM STATEMENT***

# Add any two features to Echo Client/Server and demonstrate 
# them. In the report, you must describe the new features with their 
# benefit.

# This is one of the features that I have incorporated
# INTERACTIVE MESSAGING in Echo client server

# The code for the server starts here
import socket

# The pickle module implements binary protocols for serializing and de-serializing a Python object structure.
import pickle 
import random
import datetime

# Start with a display message
print('''
**************************************************************
*                       WELCOME!                             *
*                 This is the server                         *
**************************************************************
**************************************************************
-------------->    INTERACTIVE MESSAGING    <-----------------
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

    # If the decoded message requests the server to send a random message to the client when decodedData begins with MESSAGE
    if decodedData.split()[0] == "MESSAGE":
        # Recieve the message from the client 
        message = decodedData.split()[1]
        # store the current timestamp
        timestamp = datetime.datetime.now()
        print(f"\nMessage from the Client: {message}\nReceived at {timestamp}\n")
        print("\nSending Random Message...")
        # generate a random message comprising greeting words to form a message
        randomMessage = random.choice(["Hello", "Hi", "Hey", "Howdy", "Greetings", "Good Day", "Good Morning", "Good Evening", "Good Afternoon", "Good Night"])
        # send the random message to the client
        serverSocket.sendto(str.encode(f"Your Message has been recieved\n Here is a Message for you: {randomMessage}"), clientAddress)
        # update the timestamp
        timestamp = datetime.datetime.now()
        print(f"Random Message: {randomMessage}")
        print(f"\nMessage sent at {timestamp}")
        print("\n")
        continue
    

    # If the decoded message requests the server for age based on date of birth when the decoded message begins with DOB
    if decodedData.split()[0] == "DOB-EXPLORE":
        # Recieve the date of birth from the client
        dateOfBirth = decodedData.split()[1] #04-01-2002
        # store the current timestamp
        timestamp = datetime.datetime.now()
        print(f"\nDate of Birth: {dateOfBirth}\nReceived at {timestamp}\n")
        print("\nSending Age...")

        # calculate the age in years
        age = datetime.datetime.now().year - int(dateOfBirth.split("-")[2]) # [04,01,2002]
        # Print the age of the client
        print(f"\nAge of the Client: {age}\n")
        timestamp = datetime.datetime.now()
        # Generate a greeting message based on current time like Good Morning, Good Afternoon, Good Evening, Good Night
        greetingTime = timestamp.hour # get the current hour
        if greetingTime >= 0 and greetingTime < 12:
            greeting = "Good Morning"
        elif greetingTime >= 12 and greetingTime < 16:
            greeting = "Good Afternoon"
        elif greetingTime >= 16 and greetingTime < 20:
            greeting = "Good Evening"
        else:
            greeting = "Good Night"

        # Get astrological sign based on the date of birth
        dateOfBirth = dateOfBirth.split("-") # split the date of birth into day, month and year
        day = int(dateOfBirth[0])
        month = int(dateOfBirth[1])
        year = int(dateOfBirth[2])
        if month == 1 or month == 2: # January and February
            month = 12 
            year = year - 1 # decrement the year
        else:
            month = month - 1
        # Calculate the day of the week
        dayOfTheWeek = (day + (((13 * month) - 1) / 5) + year + (year / 4) + (6 * (year / 100)) + (year / 400)) % 7 
        # Get the astrological sign based on the day of the week
        if dayOfTheWeek == 0:
            astrologicalSign = "Capricorn"
        elif dayOfTheWeek == 1:
            astrologicalSign = "Aquarius"
        elif dayOfTheWeek == 2:
            astrologicalSign = "Pisces"
        elif dayOfTheWeek == 3:
            astrologicalSign = "Aries"
        elif dayOfTheWeek == 4:
            astrologicalSign = "Taurus"
        elif dayOfTheWeek == 5:
            astrologicalSign = "Gemini"
        else:
            astrologicalSign = "Cancer"

        # Find the personality based on the date of birth and the astrological sign
        if day >= 21:
            personality = "You are an Achiever"
        elif day >= 19:
            personality = "You are a Socializer"
        elif day >= 17:
            personality = "You are a Thinker"
        elif day >= 15:
            personality = "You are an Explorer"
        elif day >= 13:
            personality = "You are an Entertainer"
        elif day >= 11:
            personality = "You are an Analyst"
        elif day >= 9:
            personality = "You are a Leader"
        elif day >= 7:
            personality = "You are an Analyst"
        elif day >= 5:
            personality = "You are an Entertainer"
        elif day >= 3:
            personality = "You are a Thinker"
        else:
            personality = "You are a Socializer"
        # Send the age and personality to the client
        # create an array and all the value of age, greeting, astrological sign and personality
        clientInfo = [age, greeting, astrologicalSign, personality]
        # send the array to the client
        serverSocket.sendto(pickle.dumps(clientInfo), clientAddress) # searilize the array and send it to the client
        # serverSocket.sendto(str.encode(f"{greeting} client!\n\n Here are the informations about you which you might not have known:-\nYour Age is {age}\nYour Astrological Sign is {astrologicalSign}\n\n {personality}"), clientAddress)
        print(f"\nMessage sent at {timestamp}")
        print("\n")
        timestamp = datetime.datetime.now()
        print(f"\nGreeting: {greeting}\nAge: {age}\nAstrological Sign: {astrologicalSign}\nPersonality: {personality}\n")
        print(f"\nMessage sent at {timestamp}")
        print("\n")
        continue



    # Sending reply to the client with an Acknowledgement message
    serverSocket.sendto(encodedACKmessage, clientAddress)
    print(f"ACK Message: {ACKmessage}")
    

# Close the socket with a message
print("\n\nClosing the Server Socket...")
serverSocket.close()
print("\nServer Socket Closed!")