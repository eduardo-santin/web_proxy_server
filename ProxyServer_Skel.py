from socket import *
import os
import sys

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
	print ('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print ('Received a connection from:' ,addr)
	message = tcpCliSock.recv(1024)
	print ('This is the message received from the client:', message)


	print ('Message end')

	# Extract the filename and hostname from the given message
	print (message.split()[1])
	filename = message.split()[1].partition("/")[2]
	filename = filename.split("/")
	print ("Filename", filename)
	hostname = filename[1]
	filename = "/".join(filename[1:])
	print ("Filename", filename)
	print ("Hostname", hostname)
	fileExist = "false"

	# File to use in cache
	filetouse = filename

	# Check if filename is a directory
	if filename[-1] == "/":
		filetouse += "index.html"

	try:
		# Check wether the file exist in the cache
		f = open(filetouse, "r")
		outputdata = f.readlines()
		fileExist = "true"
		# ProxyServer finds a cache hit and generates a response message
		tcpCliSock.send("HTTP/1.0 200 OK\r\n")

		# You might want to play with this part.  It is not always html in the cache
		tcpCliSock.send("Content-Type:text/html\r\n")

		# Fill in start.

		# Fill in end.

		print ('Read from cache')
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false":
			# Create a socket on the proxyserver
			c = 'something'

			try:
				# Connect to the socket to port 80

				# Fill in start.

				# Fill in end.

				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				fileobj = c.makefile('r', 0)
				fileobj.write("GET "+"http://" + filename + " HTTP/1.0\nHost: "+hostname+ "\n\n")
				# Read the response into buffer

				# Fill in start.

				# Fill in end.

				# Create a new file in the cache for the requested file.
				# Create the directory structure if necessary.
				# Also send the response in the buffer to client socket and the corresponding file in the cache
				if not os.path.exists(filename):
					os.makedirs(os.path.dirname(filename))
					
				tmpFile = open("./" + filetouse,"wb")
				# Fill in start.

				# Fill in end.

			except:
				print ("Illegal request")
		else:
			# HTTP response message for file not found
			tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n")
			# Fill in start.

			# Fill in end.

	# Close the client and the server sockets
	tcpCliSock.close()

tcpSerSock.close()
