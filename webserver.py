# Eduardo Santín
# CCOM 4205
# Project 1 - Application Layer
from socket import *
import os
import sys

# set debug mode
# switch to True to enable debug mode
debug = True

# create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# assign port number
# going with 8080 because 80 is used by the system on my machine
# and is giving me a permission error
serverPort = 8080

# assign server address
serverAddr = "localhost"

# bind to the port  
tcpSerSock.bind((serverAddr, serverPort))

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


        f = open(filename, "r")

        # collect the html file from the file system
        outputdata = f.readlines()
        print ("Outputdata", outputdata)

        # send one HTTP header line into socket
        connectionSocket.send(("HTTP/1.1 200 OK\r\n").encode('utf-8'))

        # send the charset for the content to be utf-8
        connectionSocket.send(("Content-Type: text/html; charset=utf-8\r\n").encode('utf-8'))
        
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            if debug:
                print ("Outputdata[" + str(i) + "]", outputdata[i])
            connectionSocket.send((outputdata[i]).encode('utf-8'))

        # finish formatting the message to send to the client
        # and close the connection socket
        connectionSocket.send(("\r\n").encode('utf-8'))
        connectionSocket.close()

    except IOError:
        #Send response message for file not found
        connectionSocket.send(("HTTP/1.1 404 Not Found\r\n").encode('utf-8'))
        #Close client socket
        connectionSocket.close()
