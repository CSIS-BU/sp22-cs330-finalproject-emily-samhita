#!/usr/bin/env python

from socket import *
from _thread import *

RECV_BUFFER_SIZE = 2048

def get_line(c, buf):
    while b'\0' not in buf:
        data = c.recv(RECV_BUFFER_SIZE)
        if not data: # socket closed
            return None
        buf += data
    line,sep,buf = buf.partition(b'\0')
    return line.decode()

def choose_story(c):
    # ask client to choose a story
    askClient = ("Choose a story (1), (2), (3): \0")
    c.send(askClient.encode())
    choice1 = get_line(c, b'')
    return choice1

##    story_arr = ['test1', 'test2'] 
##    choice = randint(0, len(story_arr) - 1) # randomly chooses a story
##    return story_arr[choice]

def get_prompts(title):
    ## TODO
    print(title)
    return ['<NOUN>', '<VERB>', '<ADJ>']

def send_prompt(prompt, c):
    prompt += '\0'
    c.send(prompt.encode())
    print('sending ', prompt)
    return get_line(c, b'')

def make_story(responses):
    ## TODO
    print('making story')
    return(' '.join(responses))

def play_game(connection):
    ## pick story, send title
    title = choose_story(connection) +str('\0')
    connection.send(title.encode()) 
    
    prompt_arr = get_prompts(title) 
    
    resp_arr = [send_prompt(p, connection) for p in prompt_arr] 
    connection.send(str.encode('DONE\0'))
    print(resp_arr) 
    
    story = make_story(resp_arr) +str('\0')
    connection.sendall(story.encode())
    connection.close()
    return

def main():
    serverPort = 12007 #port number
    serverSocket = socket(AF_INET, SOCK_STREAM) #create socket
    try:
        serverSocket.bind(('',serverPort)) #bind port number with socket
    except error as e:
        print('error binding socket', str(e))

    print('----- TCP Server is ready. ----- ')

    serverSocket.listen() #waits for TCP connection request

    while True:
        try:
            connection, addr = serverSocket.accept()
            print('----- TCP Server accepted connection with ', addr[0], ':', str(addr[1]), ' -----\n')
            start_new_thread(play_game, (connection, ))
            print("~~ WELCOME TO MADLIBS ~~")
        except KeyboardInterrupt:
            serverSocket.close()


if __name__ == "__main__":
    main()
