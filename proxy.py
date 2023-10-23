# Eduardo Santín
# CCOM 4205
# Project 1 - Application Layer
from socket import *
import os
import io
import sys

# set debug mode
# switch to True to enable debug mode
debug = True





def sendTextData(socket, filename, fileExtension):

	print(filename)
	if fileExtension == "js":
		fileExtension = "javascript"

	# Send http response
	socket.send(("HTTP/1.0 200 OK\r\n").encode('utf-8'))

	# create content type message
	contentType = "Content-Type: text/" + fileExtension + "\r\n"

	# send content type
	socket.send((contentType).encode('utf-8'))

	# open file in read mode
	f = open(os.path.abspath(filename), "rb")

	# read file content and send it to the client
	# using with, it will close the file automatically
	with f:
		socket.sendall(f.read())
	


if len(sys.argv) <= 1:
	print ('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.

# assign proxy port number
serverPort = 12000

# assign proxy server address
serverAddr = sys.argv[1]

# bind to the port
tcpSerSock.bind((serverAddr, serverPort))

# start listening
tcpSerSock.listen(1)

# Fill in end.

while 1:

	# Start receiving data from the client
	print ('Ready to serve...\n\n')
	tcpCliSock, addr = tcpSerSock.accept()
	print ('Received a connection from:' ,addr)

	# utf-8 sometimes gives an unicode error when trying to decode
	# the message, so I'm using iso-8859-1 instead,
	# from what I've read this should be a fix to the problem
	message = tcpCliSock.recv(1024).decode('iso-8859-1')

	# if empty message, then close it and continue
	if not message:
		tcpCliSock.close()
		continue

	if debug:
		print ('This is the message received from the client:', message)

	# if message stars with CONNECT, then close it and continue
	if message.startswith("CONNECT"):
		tcpCliSock.close()
		continue

	# print ('Message end')

	# # Extract the filename and hostname from the given message
	# message = message.split()[1].partition("/")[2]
	# message = message.encode('utf-8')
	# print ("Message type", type(message))
	# print ("Message", message)
	
	filename = message.split()[1].partition("/")[2]
	filename = filename.split("/")
	print ("Filename", filename)
	hostname = filename[1]
	filename = "/".join(filename[1:])
	print ("Filename", filename)
	print ("Hostname", hostname)
	fileExist = "false"

	# if hostname is detectportal.firefox.com, then close it and continue
	if hostname == "detectportal.firefox.com":
		tcpCliSock.close()
		continue

	# File to use in cache
	filetouse = filename

	# Check if filename is a directory
	if filename[-1] == "/":
		filetouse += "index.html"

	try:
		with open(filetouse, "rb") as f:
			pass

		# if it passes the previous line, then the file exists
		fileExist = "true"

		
		# get file extension
		filename_extension = os.path.splitext(filetouse)[1][1:]
		

		sendTextData(tcpCliSock, filetouse, filename_extension)
		# Fill in end.

		print ('Read from cache')
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false":
			# Create a socket on the proxyserver
			c = socket(AF_INET, SOCK_STREAM)

			try:
				# Connect to the socket to port 80

				# Fill in start.

				c.connect((hostname, 80))

				# Fill in end.

				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				fileobj = c.makefile('rwb', 0)
				fileobj.write(("GET http://" + filename + " HTTP/1.0\n\n").encode('utf-8'))

				print('fileobj', fileobj)

				# Read the response into buffer

				# Fill in start.

				try:
					os.makedirs(os.path.dirname(filename))

				except:
					pass

				
				tmpFile = open("./" + filetouse,"wb")

				# check if the filename is an image or text
				filename_extension = os.path.splitext(filename)[1][1:]

				buffer = fileobj.readlines()
				# get content-length from header

				# concatenate the buffer items starting at index 13
				# this is to avoid the HTTP header
				for i in range(12, len(buffer)):
					tmpFile.write(buffer[i])
				
				tmpFile.close()

				# 

				
				if debug:
					print ("Buffer length", len(buffer))
					print ("Buffer type", type(buffer))
					# first buffer item
					print ("Buffer item index 0", buffer[0])

			
				print ("File created and cached \n sending data to client")

				# send the content message to the client
				
	

				sendTextData(tcpCliSock, filetouse, filename_extension)
				

				# Fill in end.

			except Exception as error:
				print ("Illegal request")

				if	debug:
					# print out the error message that python reports
					print ("Error: ", error)

					# print the line that caused the error, if possible
					print ("Line: ", error.__traceback__.tb_lineno)
					# print content of the line
					print ("Line content: ", error.__traceback__.tb_frame.f_code.co_name)

					# close the client socket and release the address
					c.close()
					tcpCliSock.close()
					tcpSerSock.close()

					# get session id and terminate the program
					os.system("curl -s -X GET http://localhost:12000/terminate")
				

				exit()

		else:
			# HTTP response message for file not found
			tcpCliSock.send(("HTTP/1.0 404 sendErrorErrorError\r\n".encode(encoding='utf-8')))
			# Fill in start.
			

			# Fill in end.

	# Close the client and the server sockets
	print ("Closing client socket\n\n")
	tcpCliSock.close()

tcpSerSock.close()
