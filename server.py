#!/usr/bin/env python

from socket import *
from _thread import *
from random import randint

RECV_BUFFER_SIZE = 2048

def choose_story(c):
    ## TODO
    story_arr = ['test1', 'test2']
    choice = randint(0, len(story_arr) - 1)
    return story_arr[choice]

def get_prompts(title):
    ## TODO
    print(title)
    return ['<NOUN>', '<VERB>', '<ADJ>']

def send_prompt(prompt, c):
    c.send(prompt.encode())
    print('sending ', prompt)
    return c.recv(RECV_BUFFER_SIZE).decode()

def make_story(responses):
    ## TODO
    print('making story')
    return(' '.join(responses))

def play_game(connection):
    ## pick story, send title
    title = choose_story(connection)
    connection.send(title.encode())
    prompt_arr = get_prompts(title)
    resp_arr = [send_prompt(p, connection) for p in prompt_arr]
    connection.send(str.encode('DONE'))
    print(resp_arr)
    story = make_story(resp_arr)
    connection.sendall(story.encode())
    connection.close()
    return

def main():
    serverPort = 12006 #port number
    serverSocket = socket(AF_INET, SOCK_STREAM) #create socket
    try:
        serverSocket.bind(('',serverPort)) #bind port number with socket
    except error as e:
        print('error binding socket', str(e))

    print('----- TCP Server is ready. ----- \n')

    serverSocket.listen() #waits for TCP connection request

    while True:
        try:
            connection, addr = serverSocket.accept()
            print('----- TCP Server accepted connection with ', addr[0], ':', str(addr[1]), ' -----')
            start_new_thread(play_game, (connection, ))
        except KeyboardInterrupt:
            serverSocket.close()


if __name__ == "__main__":
    main()
