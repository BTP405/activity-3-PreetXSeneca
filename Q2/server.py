
import socket
import dill
import threading


# Define the task class
class Task:
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def execute(self):
        return self.func(*self.args)

# Worker function to handle incoming tasks
def handle_task(client_socket):
    try:
        data = client_socket.recv(4096)
        task = dill.loads(data)
        result = task.execute()
        client_socket.sendall(dill.dumps(result))
    except Exception as e:
        print(f"Error processing task: {e}")
    finally:
        client_socket.close()


# Worker node function
def worker(host, port):
    worker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker_socket.bind((host, port))
    worker_socket.listen(5)
    print(f"Worker node listening on {host}:{port}")

    while True:
        client_socket, _ = worker_socket.accept()
        threading.Thread(target=handle_task, args=(client_socket,)).start()
        # handle_task(client_socket)

if __name__ == "__main__":
    worker("localhost", 5000)
