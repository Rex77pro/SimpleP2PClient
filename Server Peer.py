from socket import *
from threading import *
import requests
from os import listdir
from os.path import isfile, join

folderPath = "C:/Temp/"
# send data to client
def handleClient(connectionSocket, addr):
    print(addr)
    # Uses connection make a socket connection and recieve
    # decode() function decodes data
    Unprocessedrequest = connectionSocket.recv(1024).decode()
    print(addr[0])
    print(Unprocessedrequest)
    request = process(Unprocessedrequest)
    
    if validate(request):
        request = request.split(";")
        request = request[0]
        print("here1")
        file = open(folderPath + request, "rb")
        print("here2")
        file_data = file.read(1024)
        print("here3")
        while file_data:
            print ("sending...")
            connectionSocket.send(file_data)
            file_data = file.read(1024)
        file.close()
        print("Done Sending")
        connectionSocket.close()
        print("Connection stopped")

def process(request):
    request = request.strip()
    return request

def validate(request):
    if ";" in request:
        return True
    else: False

# Port that client needs
serverPort = 12000

onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
print(onlyfiles)
api_url = "https://p2psharingapi20230321122351.azurewebsites.net/api/FileEndpoints"
for file in onlyfiles:
    fileAndPeerInformation = {"ip": "10.200.130.76", "port": serverPort, "fileName": file}
    response = requests.post(api_url, json=fileAndPeerInformation)
    print(response.json())

# AF_INET: IPv4
# SOCK_STREAM: stream of content
serverSocket = socket(AF_INET,SOCK_STREAM)
# "": IP address, blank = all ip can access in my server
# serverPort: port of my server
serverSocket.bind(("",serverPort))
# waiting for client
serverSocket.listen(1)

print("The Server Peer is ready to receive")

while True:
    # Wait for connected client
    connectionSocket, addr = serverSocket.accept()
    Thread(target=handleClient, args=(connectionSocket, addr)).start()