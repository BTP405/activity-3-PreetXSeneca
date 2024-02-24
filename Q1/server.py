import socket
import pickle

from file import save_file

def accept_file():

    # create a server socket to connect to the client and receive the files
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5500))
    server_socket.listen(1)

    print("Server is listening for connection...")

    while True:
        # accepts the connection and get the client socket & client address
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")

        try:
            # receive the file data
            data = client_socket.recv(1024)
            # pickle.loads is used to deserialize a binary string into a Python object
            file_data = pickle.loads(data)
            save_file(file_data)
            # send the confirmation message to the client
            client_socket.send(("File received successfully!").encode())

        # if any error in this process is captured.
        except Exception as e:
            print(f"Error: {e}")
            client_socket.send("Error occurred while receiving the file.".encode())

        # finally after all the process we close the client socket
        finally:
            client_socket.close()

if __name__ == "__main__":
    accept_file()
