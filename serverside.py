import socket
import threading
import csv
import random

# Setting up server details
serverAddress = ('192.168.0.100', 138)  # Listen on all available network interfaces
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Address family and socket type
serverSocket.bind(serverAddress)
serverSocket.listen(1)  # Listen for one connection

# Function to handle each client 
def handleClient(clientSocket):
    data = clientSocket.recv(1024).decode() # Converting binary data to string max of 1024 bytes
    print("Received data from client:", data)

    # Opening csv file in append mode
    with open("catering.csv","a", newline='') as csvFile: 
        csvWriter = csv.writer(csvFile)
        # Appending data to file
        csvWriter.writerow([data])

print("Listening...")

# Loop making program stay active after recieving a request
while True:
    clientSocket, clientAddress = serverSocket.accept() # Accept connection and obtain reference
    print("Connected to:", clientAddress)

    # Creating a new thread to handle each client that sends data
    clientThread = threading.Thread(target = handleClient, args=(clientSocket,))
    clientThread.start() # Run the thread above