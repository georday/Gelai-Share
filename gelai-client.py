#Programmer: Elaine George + Dalton Glenn
#Date: 02/06/23
#Purpose: File Sharing Client to operate with gelai-server.py

from socket import *
import sys
import os

#Simple helper functions
def to_byte(inty, size, which = 0):
    if which == 0:
        return inty.to_bytes(size,'little')
    return inty.to_bytes(size,'big')

def file_to_byte(string):
    try:
        f = open("repo/"+ string)
        file = f.read()
        f.close()
        return file
    except:
        return -1

#Requires ip address and port
try:
    try:
        #server connection setup
        serverID = sys.argv[1]
        serverPort = int(sys.argv[2])
        clientSocket = socket(AF_INET,SOCK_STREAM)
        clientSocket.connect((serverID,serverPort))

        #find out the number of files in the servers/repo
        numfiles = int.from_bytes(clientSocket.recv(4),"little")

        #receive as many files as in the repo
        #iterate from zero through the number of files, getting the names of each
        x = 0
        listy = []
        while x < numfiles:
            fileNameLength = clientSocket.recv(4)
            fileName = clientSocket.recv(int.from_bytes(fileNameLength,"little")).decode()
            listy.append(fileName)
            print("["+ str(x) + "]" + " " + fileName)
            x = x + 1
    
        #Allows user to choose the file
        #sends that index
        file_index = int(input("Enter File Index: "))
        clientSocket.send(to_byte(file_index,4))
    
        fileName = listy[file_index]
        fileLength = clientSocket.recv(4)
        fileLengthi = int.from_bytes(fileLength,"little")
        lengthy = 0
        file = ""

        #Begin sending the file in chunks
        print("Transmission Initalized...")
        while(lengthy < fileLengthi):
            addr = clientSocket.recv(fileLengthi-lengthy)
            file = file + addr.decode()
            lengthy = lengthy + len(addr)
        
            #Print the file's progress bar
            a = int((lengthy/fileLengthi)*10)

            stra = int((lengthy/fileLengthi)*10)*"⬛"
            #progress bar
            if(len(stra)>0 and len(stra)<10 ):
                print(" "+str(a*10)+"% : "+ stra+ (10-len(stra))*"⬜")

        #creates repo directory if it doesn't exist
        if not os.path.isdir("repo"):
            os.makedirs("repo")
    
        #writes entire file
        f = open("repo/"+ fileName,"w")
        f.write(file)
        f.close()
        clientSocket.close()
        print("File Written...")
        print("Connection Closed")
    except KeyboardInterrupt:
        clientSocket.close()

except IndexError:
    print("Ip address and Port needed")
