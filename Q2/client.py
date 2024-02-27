import socket
import dill # extention of the pickle library (used for serializing and deserializing functions)
from task import Task

# Client function to send tasks to available worker nodes
def send_task(host, port, tasks):
    try:
        result =[]
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        for task in tasks:
            client_socket.send(dill.dumps(task))
            result.append(dill.loads(client_socket.recv(4096)))
        return result
    except Exception as e:
        print("Error occured while sending the task: ",e)
        return None
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Example task
    def add(x, y):
        return x + y
    
    def scale(x, y ):
        cal = []
        for i in range(0, x*y):
            cal.append(x*i)
        return cal

    task1 = Task(scale, (4, 5))
    task2 = Task(add, (34, 100))
    result = send_task("localhost", 5000, [task2,task1])
    print("Results: ", result)

