
import socket
import dill
# Define the task class
class Task:
    def __init__(self, func, args):
        self.func = func
        self.args = args

# Client function to send tasks to available worker nodes
def send_task(host, port, task):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.send(dill.dumps(task))
        result = dill.loads(client_socket.recv(4096))
        client_socket.close()
        return result
    except Exception as e:
        print(f"Error communicating with worker node: {e}")
        return None

if __name__ == "__main__":
    # Example task
    def add(x, y):
        return x + y
    
    def scale(x, y ):
       
        cal = []
        for i in range(0, x*y):
            cal.append(x*i)
        return cal


    task1 = Task(scale, (4, 10))
    task2 = Task(add, (34, 100))
    result1 = send_task("localhost", 5000, task1)
    result2 = send_task("localhost", 5000, task2)
    print("\n\nscale:", result1)
    print("\n\nadd:", result2)
