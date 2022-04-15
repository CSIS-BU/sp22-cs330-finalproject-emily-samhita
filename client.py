#!/usr/bin/env python

from socket import *
from sys import *

RECV_BUFFER_SIZE = 2048

def get_prompt(c):
    prompt = c.recv(RECV_BUFFER_SIZE)
    if(prompt.decode() == "DONE"):
        return 1
    print('Enter a ', prompt.decode(), ': ')
    return 0

def recv_story(c):
    print('receiving story:\n')
    full_message = bytearray()
    while True:
        message = c.recv(RECV_BUFFER_SIZE)
        if(len(message) <= 0):
            break
        full_message += message
    stdout.buffer.write(full_message)
    stdout.flush()

def play_game(client):
    title = client.recv(RECV_BUFFER_SIZE)
    print('Playing story: ', title.decode(), '\n')
    while(get_prompt(client) != 1):
        answer = input()
        client.send(answer.encode())
    recv_story(client)
    return

def main():
    serverName = 'localhost'  #IP address
    serverPort = 12006  # destination port number 
    clientSocket = socket(AF_INET, SOCK_STREAM)  #creates socket

    print('----- TCP Client is ready. -----')
    clientSocket.connect((serverName, serverPort))

    print("----- TCP Client is Connected. -----\n")
    play_game(clientSocket)
    
    print("\nThanks for playing!\n")
    clientSocket.close()

if __name__ == "__main__":
    main()
