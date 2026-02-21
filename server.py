#'Chat Room Connection  - Client to chat server'
import threading
import socket
host = '127.0.0.1' #host address
port = 59000 #port number
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket object
server.bind((host, port)) #bind host and port
server.listen() #listen for connections
clients = [] #list of clients because multiple clients can connect and chat
aliases = [] #list of aliases for clients to identify them in chat room 

# Function to broadcast messages to all clients in the chat room

def broadcast(message): #function to send message to all clients
    for client in clients:
        client.send(message)  # loop through clients and send message to each client because it's a chat room   

# Function to handle individual client connection.

def handle_client(client): #function to handle individual client connection.
    # This is done in a separate thread for each client so that multiple clients can be handled simultaneously 
    while True:
        try:
            message = client.recv(1024) #receive message from client 
            broadcast(message) #broadcast message to all clients
        except: #if error occurs, remove client and alias from lists
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index] # retrieve alias of disconnected client
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break  



# Main function to receive clients and start threads for each client    


def receive(): #function to receive clients and start threads for each client
    while True:
        print('Server is running and listening for connections...') # for server status and debugging 
        client, address = server.accept() #accept connection from client
        print(f'Connection established with {str(address)}') #print connection address for debugging
        client.send('alias?'.encode('utf-8')) #ask client for alias
        alias = client.recv(1024).decode('utf-8') #receive alias from client
        aliases.append(alias) #add alias to list and client to clients list
        clients.append(client)
        print(f'Alias of the client is {alias}') #print alias for debugging 
        broadcast(f'{alias} has joined the chat room!'.encode('utf-8')) #broadcast that client has joined
        client.send('You are now connected to the chat room!'.encode('utf-8')) #send confirmation message to client . encode is to
        # convert string to bytes for transmission over network
        thread = threading.Thread(target=handle_client, args=(client,)) #start thread to. In 
        #order to handle multiple clients simultaneously  args is for passing arguments to target function
        thread.start() #start thread

if __name__ == "__main__": #main function to start server
    receive() #call receive function to start server        