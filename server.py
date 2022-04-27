#!/usr/bin/env python

from socket import *
from _thread import *
import re
from pathlib import Path

RECV_BUFFER_SIZE = 2048

def get_line(c):
    buf = b''
    ## helper function to deal with send/recv not always lining up correctly
    while b'\0' not in buf:
        data = c.recv(RECV_BUFFER_SIZE)
        if not data: # socket closed
            return None
        buf += data
    line,sep,buf = buf.partition(b'\0')
    return line.decode()

def choose_story(c):
    # ask client to choose a story
    while True:
        askClient = ("Enter a number to choose a story:\n1) Amusement Park\n2) Bakery\n3) Birthday\n4) Coffee\n5) Bucky the Dog \0")
        c.send(askClient.encode())
        choice = get_line(c)
        if(choice in ['1', '2', '3', '4', '5']):
            c.send(str.encode('VALID\0'))
            break
        else:
            c.send(str.encode('INVALID\0'))
    return choice

def get_prompts(title):
    title = title.strip()[:-1]
    stories = {'1': 'amusement_park.txt', '2': 'bakery.txt', '3': 'bd_story.txt', '4': 'Coffee.txt', '5': 'Dog.txt'}
    # extract prompts from story
    data_folder = Path("./stories")
    file_to_open = data_folder / stories[title]
    f = open(file_to_open)
    fileContent = f.read()

    # gets prompts by searching <string> pattern in story & adding it to the list
    keyword = re.compile('<.*?>',re.IGNORECASE)
    prompts = keyword.findall(fileContent)

    ## returning prompt list and full file content so we don't have to open it again
    return (prompts,fileContent)

def send_prompt(prompt, c):
    prompt += '\0'
    c.send(prompt.encode())
    return get_line(c)

def make_story(responses,match,fileContent):

    # replaced prompts with responses from user into the story
    for i in range(len(match)):
        fileContent = fileContent.replace(match[i],responses[i],1)

    return(fileContent)

def play_game(connection):
    ## pick story, send title
    print("~~ WELCOME TO MADLIBS ~~")
    title = choose_story(connection) +str('\0')
    
    prompt_arr,fileContent = get_prompts(title) 
    
    resp_arr = [send_prompt(p, connection) for p in prompt_arr] 
    connection.send(str.encode('DONE\0'))

    ## keeps send/recv ing even to prevent the sometimes not recving on the client side error
    get_line(connection)
    
    story = make_story(resp_arr,prompt_arr,fileContent) +str('\0')
    connection.sendall(story.encode())
    connection.close()
    return

def main():
    serverPort = 12164 #port number
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
            ## multiple user capabilities
            start_new_thread(play_game, (connection, ))
        except KeyboardInterrupt:
            serverSocket.close()


if __name__ == "__main__":
    main()
