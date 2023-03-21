from socket import *
import requests

# Calling REST Api - sending data
# Get files from API and convert to json
api_URL = "https://p2psharingapi20230321122351.azurewebsites.net/api/FileEndpoints"
response = requests.get(api_URL)
data = response.json()
print(data)

chooseFile = input("Please Write File Name: ")

# Extract fileName, ip & host
response = requests.get(api_URL + '/' + chooseFile)
serverPeerData = response.json()
print(serverPeerData)
peerData = serverPeerData[0]

# Write filename
fileName = peerData["fileName"]

# Connect to Peer Server
serverName = peerData["ip"]
serverPort = peerData["port"]
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Sending data
dataToSend = peerData["fileName"] + ";"
serverPeerData = clientSocket.send(dataToSend.encode())

# Receive Data from Server Peer
# Set filePath to put file gotten
file = open('c:/temp/' + fileName, 'wb')
file_data = clientSocket.recv(1024)
while file_data:
    print("Receiving...")
    file.write(file_data)
    file_data = clientSocket.recv(1024)
file.close()
