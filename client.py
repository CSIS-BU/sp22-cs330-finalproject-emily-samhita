#!/usr/bin/env python

from socket import *

RECV_BUFFER_SIZE = 2048

def get_line(c, game_buf):
    ## helper function to deal with send/recv not always lining up correctly
    if(game_buf != b''):
        return game_buf.decode(), b'', None
    buf = b''
    while b'\0' not in buf:
        data = c.recv(RECV_BUFFER_SIZE)
        if not data: # socket closed
            return None
        buf += data
    line,sep,buf = buf.partition(b'\0')
    return line.decode(), buf, 'a'

def get_prompt(c, game_buf):
    prompt, game_buf, _ = get_line(c, game_buf)
    if(prompt == "DONE"):
        return 1
    print('Enter a ', prompt, ': ')
    return 0

def recv_story(c, game_buf):
    ## prints full story as received from server
    full_message = '\n'
    while True:
        message = get_line(c, game_buf)
        if(message is None or len(message[0]) <= 0):
            break
        full_message += message[0]
    print(full_message)
    return

def play_game(client):
    # user chooses a story, will repeat until valid answer is received
    
    game_buf =b''

    while True:
        titlePrompt, game_buf, _ = get_line(client, game_buf)
        print(titlePrompt)
        choice = input() +str('\0')
        client.send(choice.encode())
        resp, game_buf, _ = get_line(client, game_buf)
        if (resp != "INVALID"): 
            break
    
    ## answers all prompts
    while(get_prompt(client, game_buf) != 1): 
        answer = input() +str('\0')
        client.send(answer.encode())

    ## keeps send/recv ing even to prevent the sometimes not recving on the client side error
    client.send(str.encode('ack\0'))
        
    recv_story(client, game_buf)
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
