#Distributed Task Queue with Pickling:

#Create a distributed task queue system where tasks are sent from a client to multiple worker nodes for processing using sockets. 
#Tasks can be any Python function that can be pickled. Implement both the client and worker nodes. 
#The client sends tasks (pickled Python functions and their arguments) to available worker nodes, and each worker node executes the task and returns the result to the client.

#Requirements:
#Implement a protocol for serializing and deserializing tasks using pickling.
#Handle task distribution, execution, and result retrieval in both the client and worker nodes.
#Ensure fault tolerance and scalability by handling connection errors, timeouts, and dynamic addition/removal of worker nodes.
import socket
import pickle
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
        task = pickle.loads(data)
        result = task.execute()
        client_socket.sendall(pickle.dumps(result))
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

# Client function to send tasks to available worker nodes
def send_task(host, port, task):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.send(pickle.dumps(task))
        result = pickle.loads(client_socket.recv(4096))
        client_socket.close()
        return result
    except Exception as e:
        print(f"Error communicating with worker node: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    worker_thread = threading.Thread(target=worker, args=("localhost", 5000))
    worker_thread.start()

    # Example task
    def add(x, y):
        return x + y

    task = Task(add, (4, 5))
    result = send_task("localhost", 5000, task)
    print("Result:", result)
