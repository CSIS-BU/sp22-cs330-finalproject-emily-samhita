from socket import *

print('----- TCP Server is ready. -----')
print('----- TCP Server is connected. ----- \n')

serverPort = 12005 #port number
serverSocket = socket(AF_INET, SOCK_STREAM) #create socket

serverSocket.bind(('',serverPort)) #bind port number with socket
serverSocket.listen() #waits for TCP connection request

name = input('Enter Server\'s name: ')
serverSocket.listen(1) 

connection, addr = serverSocket.accept()

#receive a connection from the client 
client_nameID = connection.recv(1024)
client_nameID = client_nameID.decode()

#print that client has joined the chat
print(client_nameID + ' has joined the chat.')
print('Type [quit] to leave the chat room')
connection.send(name.encode())

while True:
    message = input('Me > ')

    #if user types quit, the program exits
    if message == 'quit':
        message = 'Good Night...'
        connection.send(message.encode())
        print("\n")
        break

    #server sends message
    connection.send(message.encode())
    
    #receive client message, capitalize it, and print
    message = connection.recv(1024)
    message = message.decode()
    capitalizedMessage = message.upper()
    print(client_nameID, '\'s message >', capitalizedMessage)
