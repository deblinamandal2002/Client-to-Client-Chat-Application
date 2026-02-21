import threading
import socket
alias = input("Enter your alias: ")  # prompt user for alias
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket object
client.connect(('127.0.0.1', 59000))  # connect to server


# Function to receive messages from server
def receive_messages():  # function to receive messages from server
    while True:
        try:
            message = client.recv(1024).decode('utf-8')  # receive message from server and decode
            if message == 'alias?':  # if server requests alias because it is a new connection
                client.send(alias.encode('utf-8'))  # send alias to server by encoding it to bytes
            else:
                print(message)  # print received message to console
        except:  # if error occurs, close connection and exit 
            print("An error occurred. Closing connection.") # error message for debugging
            client.close()
            break

def client_send():  # function to send messages to server
    while True:
        message = f'{alias}: {input("")}'  # format message with alias.. here alias is used to identify sender
        client.send(message.encode('utf-8'))  # send message to server by encoding it to bytes as sockets transmit bytes
# Start thread to receive messages from server
receive_thread = threading.Thread(target=receive_messages)  # create thread for receiving messages
receive_thread.start()  # start receive thread

# Start thread to send messages to server
# This allows user to input messages while still receiving messages from server
send_thread = threading.Thread(target=client_send)  # create thread for sending messages
send_thread.start()  # start send thread       