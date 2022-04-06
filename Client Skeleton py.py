from socket import *

print('----- TCP Client is ready. -----')

serverName = 'localhost'  #IP address
serverPort = 12005  # destination port number 

clientSocket = socket(AF_INET, SOCK_STREAM)  #creates socket

clientSocket.connect((serverName, serverPort))

print("----- TCP Client is Connected. -----\n")
name = input('Enter Client\'s name: ') #user input their name

#sends client's name ID to the server 
clientSocket.send(name.encode())

#receives server's name ID to know they joined the chat
server_nameID = clientSocket.recv(1024)
server_nameID = server_nameID.decode()
print('{} has joined the chat.'.format(server_nameID))
print('Type [quit] to exit.')

while True:
    message = clientSocket.recv(1024)
    message = message.decode()

    #print out the server's message
    print(server_nameID, "\'s message > ", message)

    #input client message
    message = input('Me >>  ')
    
    #if user types quit, program exits
    if message == "quit":
        message = "Leaving the Chat room"
        clientSocket.send(message.encode())
        print("\n")
        break
    
    clientSocket.send(message.encode())
