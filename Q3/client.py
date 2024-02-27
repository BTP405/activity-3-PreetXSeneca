# waits for client to send message to recieve the message.
import socket
import pickle
import threading

thread_finished = False


def send_message(client):
    global thread_finished
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
    # finally:
    #     thread_finished = True
    #     if not thread_finished:
    #         client.close()


def receive_message(client):
    global thread_finished
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
    # finally:
    #     thread_finished = True
    #     if not thread_finished:
    #         client.close()
        
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





# def receive_message():
#     while True:
#         try:
#             msg_to_send = input("\nEnter the message to send: ")
#             data = {"name":name, "msg":msg_to_send}
#             client.sendall(pickle.dumps(data))
#             message = pickle.loads(client.recv(8192))
#             if message:
#                 if message == "No Space":
#                     client.close()
#                     break
#                 print("Received message:", message)
#             else:
#                 print("Server closed the connection.")
#                 break
#         except Exception as e:
#             print("An error occurred!", e)
#             client.close()
#             break

# receive_message()

