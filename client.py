#!/usr/bin/env python

from pydoc import cli
from socket import *
from sys import *

RECV_BUFFER_SIZE = 2048

def get_line(c, buf):
    while b'\0' not in buf:
        data = c.recv(RECV_BUFFER_SIZE)
        if not data: # socket closed
            return None
        buf += data
    line,sep,buf = buf.partition(b'\0')
    return line.decode()

def get_prompt(c):
    prompt = get_line(c, b'')
    if(prompt == "DONE"):
        return 1
    print('Enter a ', prompt, ': ')
    return 0

def recv_story(c):
    print('receiving story:\n')
    full_message = ''
    while True:
        message = get_line(c, b'')
        if(message == None or len(message) <= 0):
            break
        full_message += message
    stdout.buffer.write(full_message.encode())
    stdout.flush()

def play_game(client):
    # user chooses a story
    while True:
        titlePrompt = get_line(client, b'')
        print(titlePrompt)
        choice = input() +str('\0')
        client.send(choice.encode())
        if (get_line(client, b'') != "INVALID"): 
            break
    
    while(get_prompt(client) != 1): 
        answer = input() +str('\0')
        client.send(answer.encode())
        
    recv_story(client)
    return

def main():
    serverName = 'localhost'  #IP address
    serverPort = 12151  # destination port number 
    clientSocket = socket(AF_INET, SOCK_STREAM)  #creates socket

    print('----- TCP Client is ready. -----')
    clientSocket.connect((serverName, serverPort))

    print("----- TCP Client is Connected. -----\n")
    play_game(clientSocket)
    
    print("\nThanks for playing!\n")
    clientSocket.close()

if __name__ == "__main__":
    main()
