import socket 
import pickle
import threading

clients = []
messages ={}

def handle_client_chat(client_socket, client_address):
    try:
        while True:
            message = pickle.loads(client_socket.recv(8192))
            # Q means quiting the chat app
            if message == 'Q':
                break
            name = message['name']
            data = message['msg']

            if name in messages:
                # add the msg with the coresponding name   
                messages[name].append(data)
            else:
                # if name is not there we will create new key
                messages[name] = [data]

            for client in clients:
                if client != client_socket:
                    client.sendall(pickle.dumps(messages))
    except Exception as e:
        print(e)
        # location = clients.index(client_socket)
        clients.remove(client_socket)
        client_socket.close()
    finally:
        # once quit will remove the client socket from the array and also close it
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 5500)
    server_socket.bind(server_address)
    server_socket.listen(6)
    
    print("Server is listening for connections...")
    while True:
        print(len(clients))
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        # (Optional) Max 4 people allowed 
        if len(clients) > 4:
            client_socket.recv(8192)
            client_socket.sendall(pickle.dumps("No Space"))
            client_socket.close()
        
        # start a thread for the client joined
        client_thread = threading.Thread(target=handle_client_chat, args=(client_socket, client_address))
        client_thread.start()
    
if __name__ == "__main__":   
    main()