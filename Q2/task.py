import dill  # extention of the pickle library (used for serializing and deserializing functions)

class Task:
    def __init__(self, func, args):
        self.func = func
        self.args = args
    
    def runTask(self):
        return self.func(*self.args)

def task_worker(task_data , client_socket):
    try:
        task = dill.loads(task_data)
        result = task.runTask()
        client_socket.sendall(dill.dumps(result))
    except Exception as e:
        print("Exception occured: ", e)
        client_socket.close()

        