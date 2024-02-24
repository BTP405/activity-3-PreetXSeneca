import os

def get_file():
    file_path = input("\bEnter file path (e.g. ./test1.txt): ")
    with open(file_path, "rb") as file:
        file_data = file.read()
        filename = file_path.split("/")[-1]
    return  filename,file_data

def save_file(fileData):
    # will create a directory or folder to save the received files in it.
    save_directory = 'files_dir'
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)\
    # from file_data object we will get the file name ad create a file of that name in save directory 
    filename = os.path.join(save_directory, fileData['filename'])

    # will write the content in the file
    with open(filename, 'wb') as file:
        file.write(fileData['data'])
    print(f"File saved to {filename}")
