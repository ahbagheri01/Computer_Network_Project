import threading
import time
import socket

host = "127.0.0.1"
port = 5002

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Admin:
    def __init__(self, username, password, is_accepted = False):
        self.username = username
        self.password = password
        self.is_accepted = is_accepted

class Video:
    def __init__(self, id, name, username, is_tagged = False):
        self.id = id
        self.name = name
        self.username = username
        self.is_tagged = is_tagged

all_users = []
all_admins = []
all_videos = []

user_tokens = []
admin_tokens = []
manager_token = ""

def loginUser(data):
    global all_users
    global user_tokens
    username = data.split(" ")[2]
    password = data.split(" ")[3]
    for user in all_users:
        if user.username == username and user.password == password:
            token = str(time.time()) + "-" + username
            user_tokens.append({token: user.username})
            return token
    return "Error: wrong details"

def registerUser(data):
    global all_users
    username = data.split(" ")[2]
    password = data.split(" ")[3]
    for user in all_users:
        if user.username == username:
            return "Error: user already exists"
    all_users.append(User(username, password))
    return "Success"

def loginAdmin(data):
    global all_admins
    global admin_tokens
    username = data.split(" ")[2]
    password = data.split(" ")[3]
    for user in all_admins:
        if user.username == username and user.password == password:
            if user.is_accepted:
                token = str(time.time()) + "-" + username
                admin_tokens.append({token: user.username})
                return token
            else:
                return "Error: manager has not accepted this admin"
    return "Error: wrong details"

def registerAdmin(data):
    global all_admins
    username = data.split(" ")[2]
    password = data.split(" ")[3]
    for user in all_admins:
        if user.username == username:
            return "Error: admin already exists"
    all_admins.append(Admin(username, password))
    return "Success"

def loginManager(data):
    global manager_token
    username = data.split(" ")[2]
    password = data.split(" ")[3]
    if username == "manager" and password == "supreme_manager#2022":
        manager_token = str(time.time()) + "-" + username
        return manager_token
    return "Error: wrong details"

def logoutUser(data):
    global user_tokens
    token = data.split(" ")[2]
    for token_dict in user_tokens:
        for key, value in token_dict.items():
            if key == token:
                user_tokens.remove(token_dict)
                return "Success"
    return "Error: invalid token"

def logoutAdmin(data):
    global admin_tokens
    token = data.split(" ")[2]
    for token_dict in admin_tokens:
        for key, value in token_dict.items():
            if key == token:
                admin_tokens.remove(token_dict)
                return "Success"
    return "Error: invalid token"

def logoutManager(data):
    global manager_token
    token = data.split(" ")[2]
    if token == manager_token:
        manager_token = ""
        return "Success"
    return "Error: invalid token"

def prepare_response(data):
    if data.startswith("login user"):
        return loginUser(data)
    elif data.startswith("register user"):
        return registerUser(data)
    elif data.startswith("login admin"):
        return loginAdmin(data)
    elif data.startswith("register admin"):
        return registerAdmin(data)
    elif data.startswith("login manager"):
        return loginManager(data)
    elif data.startswith("logout user"):
        return logoutUser(data)
    elif data.startswith("logout admin"):
        return logoutAdmin(data)
    elif data.startswith("logout manager"):
        return logoutManager(data)
    return "Error: bad request"




def accept_connection(connection, source_host, source_port):
    print("accept_connection() - Accepted connection from " + source_host + ":" + str(source_port))
    data = connection.recv(1024).decode()
    if data == "":
        return
    print("accept_connection() - Received data: '" + data + "'")
    response = prepare_response(data)
    if response != "":
        connection.sendall(response.encode())
    connection.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
print("main() - Server is listening")
while True:
    connection, addr = s.accept()
    threading.Thread(target=accept_connection, args=(connection, addr[0], int(addr[1]))).start()