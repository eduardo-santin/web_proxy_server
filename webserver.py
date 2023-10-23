# Eduardo Santín
# CCOM 4205
# Project 1 - Application Layer
from socket import *
import os
import sys

# set debug mode
# switch to True to enable debug mode
debug = True


# text_types =['html', 'css', 'js']

def sendTextData(socket, filename, fileExtension):
	if fileExtension == "js":
		fileExtension = "javascript"

	# Send http response
	socket.send(("HTTP/1.1 200 OK\r\n").encode('utf-8'))

	# create content type message
	contentType = "Content-Type: text/" + fileExtension + "; charset=utf-8\r\n"

	# send content type
	socket.send((contentType).encode('utf-8'))

	# open file in read mode
	f = open(os.path.join("./", filename), "rb")

	# read file content and send it to the client
	# using with, it will close the file automatically
	with f:
		socket.sendall(f.read())
	


# create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# assign port number
# going with 8080 because 80 is used by the system on my machine
# and is giving me a permission error
serverPort = 80

# assign server address
serverAddr = "localhost"

# bind to the port  
try:
    tcpSerSock.bind((serverAddr, serverPort))
except OSError:
    print("Address already in use")
    tcpSerSock.bind((serverAddr, 8080))
    print("Using port 8080")

# start listening for connections from clients(browser)
tcpSerSock.listen(1)

while 1:
    
    try:
    # start receiving data from the client
        print("Ready to serve...")
        connectionSocket, addr = tcpSerSock.accept()
        print("Received a connection from:", addr)

        # get the message from the client
        message = connectionSocket.recv(1024).decode('utf-8')
        if debug:
            print ("Message", message)

        filename = message.split()[1].partition("/")[2]
        print ("Filename", filename)

        fileExtension = filename.split(".")[1]

        sendTextData(connectionSocket, filename, fileExtension)
        connectionSocket.close()
        print("Connection closed")
     


    except IOError:
        #Send response message for file not found
        connectionSocket.send(("HTTP/1.1 404 Not Found\r\n").encode('utf-8'))
        #Close client socket
        connectionSocket.close()
        print("Connection closed, file not found")
