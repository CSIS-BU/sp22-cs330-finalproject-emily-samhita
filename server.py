#!/usr/bin/env python

from socket import *
from _thread import *
import re
from pathlib import Path

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
    while True:
        askClient = ("Enter a number to choose a story:\n1) Amusement Park\n2) Bakery\n3) Birthday \0")
        c.send(askClient.encode())
        choice = get_line(c, b'')
        if(choice in ['1', '2', '3']):
            c.send(str.encode('VALID\0'))
            break
        else:
            c.send(str.encode('INVALID\0'))
    return choice

def get_prompts(title):
    title = title.strip()[:-1]
    stories = {'1': 'amusement_park.txt', '2': 'bakery.txt', '3': 'bd_story.txt'}
    # extract prompts from story
    data_folder = Path("./stories")
    file_to_open = data_folder / stories[title]

    f = open(file_to_open)
    fileContent = f.read()
    # extract prompts from story
    # file1 = open("test_story.txt") ## CHANGE THIS to open correct file from the stories folder 
    # fileContent = file1.read()
    # file1.close()

    # gets prompts by searching <string> pattern in story & adding it to the list
    keyword = re.compile('<.*?>',re.IGNORECASE)
    prompts = keyword.findall(fileContent)

    return (prompts,fileContent)

def send_prompt(prompt, c):
    prompt += '\0'
    c.send(prompt.encode())
    return get_line(c, b'')

def make_story(responses,match,fileContent):

    # replaced prompts with responses from user into the story
    for i in range(len(match)):
        fileContent = fileContent.replace(match[i],responses[i],1)

    return(fileContent)

def play_game(connection):
    ## pick story, send title
    title = choose_story(connection) +str('\0')
    
    prompt_arr,fileContent = get_prompts(title) 
    
    resp_arr = [send_prompt(p, connection) for p in prompt_arr] 
    connection.send(str.encode('DONE\0'))
    
    story = make_story(resp_arr,prompt_arr,fileContent) +str('\0')
    connection.sendall(story.encode())
    connection.close()
    return

def main():
    serverPort = 12154 #port number
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
