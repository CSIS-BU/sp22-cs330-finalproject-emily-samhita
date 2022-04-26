#!/usr/bin/env python

from socket import *

RECV_BUFFER_SIZE = 2048

def get_line(c, buf):
    ## helper function to deal with send/recv not always lining up correctly
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
    ## prints full story as received from server
    full_message = '\n'
    while True:
        message = get_line(c, b'')
        if(message == None or len(message) <= 0):
            break
        full_message += message
    print(full_message)

def play_game(client):
    # user chooses a story, will repeat until valid answer is received
    while True:
        titlePrompt = get_line(client, b'')
        print(titlePrompt)
        choice = input() +str('\0')
        client.send(choice.encode())
        if (get_line(client, b'') != "INVALID"): 
            break
    
    ## answers all prompts
    while(get_prompt(client) != 1): 
        answer = input() +str('\0')
        client.send(answer.encode())
        
    recv_story(client)
    return

def main():
    serverName = 'localhost'  #IP address
    serverPort = 12164  # destination port number 
    clientSocket = socket(AF_INET, SOCK_STREAM)  #creates socket

    print('----- TCP Client is ready. -----')
    clientSocket.connect((serverName, serverPort))

    print("----- TCP Client is Connected. -----\n")
    play_game(clientSocket)
    
    print("\nThanks for playing!\n")
    clientSocket.close()

if __name__ == "__main__":
    main()
