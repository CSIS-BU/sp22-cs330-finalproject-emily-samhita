""" 
--------- OUTLINE ----------
1. client & server connection
2. SERVER FUNCTIONALITY
    - read files 
    - sends story in a string to client 
    - story is split into multiple arrays 
        - each sentence is spilt into an separate arrays
        - search array with <> delimiter to find where to insert word
        - take index of client input array and insert into index of story array
    - send client input asking adj,verb,noun
    - puts client input into array
    - takes each item from client input array and insert into each story array 
    - sends the finished story in a whole string
3. CLIENT FUNCTIONALITY
    - client input and send to server 

"""