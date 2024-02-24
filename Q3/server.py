import socket 
import pickle
import threading

clients = []
messages ={}

def handle_client_chat(client_socket, client_address):
    while True:
        try:
            message = pickle.loads(client_socket.recv(8192))
            # split will give us a list of words
            name = message['name']
            data = message['msg']

            if name in messages:
                # will add the line number in to the list as a value  
                messages[name].append(data)
            else:
                # word is not present then we will add it with list of line number as a value.
                messages[name] = [data]

            for client in clients:
                if client != client_socket:
                    client.sendall(pickle.dumps(messages))
        except Exception as e:
            print(e)
            # location = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            break

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 5500)
    server_socket.bind(server_address)
    server_socket.listen(5)
    
    print("Server is listening for connections...")
    while True:
        print(len(clients))
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        if len(clients) > 4:
            client_socket.sendall(pickle.dumps("No Space"))
            client_socket.recv(8192)
            client_socket.close()

        client_thread = threading.Thread(target=handle_client_chat, args=(client_socket, client_address))
        client_thread.start()
  
        
main()