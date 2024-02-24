import socket
import pickle

from file import get_file


def send_file():
    
    # First will try to open the file by given path 
    try:
        filename, file_data=get_file()
        # if file found then will read the data
        data = {"filename": filename, "data": file_data}

    # if file not found will print the error and send nothing to server
    except Exception as e: # or we can use except FileNotFoundError:
        print(e)
        return
    
    try:
        # Here, pickle.dumps is used to serialize an object into a bytes object. 
        # It returns a binary string representing the object, which can be stored or transmitted.
        pickled_data = pickle.dumps(data)

        # if any error occures while pickling
    except pickle.PickleError as e:
        print(f"Pickle error: {e}")
        return
    
    # now once the file is pickled we create a socket and send it to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('127.0.0.1', 5500))
        client_socket.sendall(pickled_data)

        # will receive the response from server that file got saved or got any error
        response = client_socket.recv(1024).decode()
        print(response)

        # any error while in this socket process is handled
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    send_file()
