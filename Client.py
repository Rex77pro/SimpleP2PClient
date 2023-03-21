from socket import *
import requests

# Calling REST Api - sending data
api_URL = "https://p2psharingapi20230321122351.azurewebsites.net/api/FileEndpoints"
response = requests.get(api_URL)
data = response.json()
print(data)

chooseFile = input("Please Write File Name: ")

response = requests.get(api_URL + '/' + chooseFile)
serverPeerData = response.json()
print(serverPeerData)
peerData = serverPeerData[0]

fileName = peerData["fileName"]

serverName = peerData["ip"]
serverPort = peerData["port"]
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Sending data
dataToSend = peerData["fileName"] + ";"
serverPeerData = clientSocket.send(dataToSend.encode())

# Receive Data from Server Peer
file = open('c:/temp/' + fileName, 'wb')
file_data = clientSocket.recv(1024)
while file_data:
    print("Receiving...")
    file.write(file_data)
    file_data = clientSocket.recv(1024)
file.close()

# Hent filer fra API, og lav om til json -> Din fil indeholder filNavn, ip og host ->
# Brug ip og Host til at connect til Server -> send fil navn til Server ->




