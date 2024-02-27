# waits for client to send message to recieve the message.
import socket
import pickle
import threading


def send_message(client):
    print("\nNow, Enter the message to send (Q = Exit Chat)\n")
    try:
        while True:
            msg_to_send = input()
            if msg_to_send == 'Q':
                client.sendall(pickle.dumps(msg_to_send))
                break
            data = {"name": name, "msg": msg_to_send}
            client.sendall(pickle.dumps(data))
    except Exception as e:
        print("An error occurred while sending a message!", e)

def receive_message(client):
    try:
        while True:
            data = client.recv(8192)
            if data:
                messages = pickle.loads(data)
                if messages == "No Space":
                    break
                print("\nReceived message: ")
                for msg in messages:                
                    if msg != name:
                        print('\t\t',msg,":", messages[msg])
            else:
                print("\nServer closed the connection.\n")
                break
    except Exception as e:
        print("An error occurred while receiving a message!", e)
        
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 5500))
name = input("\nEnter your username to start chat: ")
# Create and start the sending and receiving threads
receive_thread = threading.Thread(target=receive_message,args=(client,))
send_thread = threading.Thread(target=send_message,args=(client,))

send_thread.start()
receive_thread.start()

# Wait for both threads to finish (they won't in this case, unless an error occurs)
send_thread.join()
receive_thread.join()

client.close()
