# waits for client to send message to recieve the message.
import socket
import pickle

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5500))
name = input("\nEnter your username to start chat: ")


def receive_message():
    while True:
        try:
            msg_to_send = input("\nEnter the message to send: ")
            data = {"name":name, "msg":msg_to_send}
            client.sendall(pickle.dumps(data))
            message = pickle.loads(client.recv(8192))
            if message:
                print("Received message:", message)
            else:
                print("Server closed the connection.")
                break
        except Exception as e:
            print("An error occurred!", e)
            client.close()
            break

receive_message()


# Different threads for receiving and sending messages

# import socket
# import pickle
# import threading

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('127.0.0.1', 5500))
# name = input("\nEnter your username to start chat: ")

# def send_message():
#     while True:
#         try:
#             msg_to_send = input("\nEnter the message to send: ")
#             data = {"name": name, "msg": msg_to_send}
#             client.sendall(pickle.dumps(data))
#         except Exception as e:
#             print("An error occurred while sending a message!", e)
#             break

# def receive_message():
#     while True:
#         try:
#             message = pickle.loads(client.recv(8192))
#             if message:
#                 print("\nReceived message:", message)
#             else:
#                 print("Server closed the connection.")
#                 break
#         except Exception as e:
#             print("An error occurred while receiving a message!", e)
#             break

# # Create and start the sending and receiving threads
# send_thread = threading.Thread(target=send_message)
# receive_thread = threading.Thread(target=receive_message)

# send_thread.start()
# receive_thread.start()

# # Wait for both threads to finish (they won't in this case, unless an error occurs)
# send_thread.join()
# receive_thread.join()