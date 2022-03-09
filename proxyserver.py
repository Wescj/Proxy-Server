#---------------------
#Note: For some reason the cached file does not send properly to localhost:8888
#      However the cached file is indeed saved but was just not sent
#
#Written by: Wesley Judy and Andrew Song
#---------------------

from socket import *
import sys
temp = "localhost"
if len(sys.argv) <= 1:
    # print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    # sys.exit(2)
    pass
else:
    temp = sys.argv[1]


# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((temp, 8888))
tcpSerSock.listen(100)

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(1024).decode()
    print(message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[-1]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename.replace("/","\\")
    print("searching for file ", filetouse)
    # print(filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        print("found in cache")
        # ProxyServer finds a cache hit and generates a response message\
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
            # print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            print("not found in cache")
            # socket create
            c = socket(AF_INET, SOCK_STREAM)   
            hostn = filename.replace("www.","",1)
            print("Trying to find file")
            print(hostn)
            # try:
                # Connect to the socket to port 80
            print("hostn:",hostn)
            tempHost = ""
            if ":" in hostn:
                c.connect(("localhost".encode(),6789))
                print("connect to localhost?\n")
                tempHost = "localhost"
            else:
                c.connect((hostn.encode(), 80))
                print ('Socket connected to port 80 of the host\n')
                tempHost = hostn
            print("Past connecting socket")
            # Create a temporary file on this socket and ask port 80 for the file requested by the client
            # fileobj = c.makefile('rwb', None)
            # print(fileobj.readline())
            if "localhost" in hostn:
                hostArr = hostn.split("/")
                print(hostArr)
                tempGET = "GET /" + "/".join(hostArr[1:]) +" HTTP/1.1\r\nHost:" + hostArr[0] + "\r\n\r\n"
            else:
                tempGET = "GET / HTTP/1.1\r\nHost:" + tempHost + "\r\n\r\n"
            # tempGET = "GET /helloworld.html HTTP/1.1\r\nHost:" + "localhost:6789" + "\r\n\r\n"
            print("TEMPGET: ", tempGET)
            c.sendall(tempGET.encode())
            
            message = c.recv(10000)
            #--------------------
            #Apparently this part of the code is required when running it locally
            #However, it seems to work fine when it runs on google collab
            #--------------------
            # if "localhost" in hostn:
            #     while 1:
            #         temptemp = c.recv(10000)
            #         message += str(temptemp)
            #         if temptemp == "":
            #             break
            # else:
            #     message = c.recv(10000)
            # print("filename:",filename)
            # tmpFile = open("testing.html","wb")
            # print("buffer:",buff)
            # for line in buff:
            #     print("Writing line:",line)
            #     tmpFile.write(line)
            # getreq = "GET "+"http://" + filename + " HTTP/1.0\r\n"
            # print("getreq:",getreq)
            # tmpFile.write(getreq)
            # print("asafsafas")
            # Read the response into buffer
            
            # Create a new file in the cache for the requested file.
            filename = filename.replace("/","\\")
            tmpFile = open("./" + filename,"wb")
            print("Message", message)
            for line in str(message):
                tmpFile.write(line.encode())
                tcpCliSock.send(line.encode())
            tmpFile.close()
            # except Exception as e:
            #     print(e)
            #     print("Illegal request")
        else:
            # HTTP response message for file not found
            print("NOT FOUND")
            tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n".encode())
            tcpCliSock.send("\r\n".encode())
    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()
