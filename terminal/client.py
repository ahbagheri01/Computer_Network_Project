import socket

token = ""
current_role = "" # user - admin - manager

def send_to_server(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.connect(("127.0.0.1", 5002))
    s.sendall(message.encode())
    response_from_proxy = s.recv(1024).decode()
    s.close()
    return response_from_proxy

def userPanel():
    while True:
        print("Welcome to user panel!")
        print("Logout")
        selection = input("Your selection: ")
        if selection == "logout":
            if logoutUser():
                break

def adminPanel():
    while True:
        print("Welcome to admin panel!")
        print("Logout")
        selection = input("Your selection: ")
        if selection == "logout":
            if logoutAdmin():
                break

def managerPanel():
    while True:
        print("Welcome to manager panel!")
        print("Logout")
        selection = input("Your selection: ")
        if selection == "logout":
            if logoutManager():
                break

def logoutUser():
    global token
    global current_role
    message = "logout user " + token
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
        return False
    else:
        token = ""
        current_role = ""
        return True

def logoutAdmin():
    global token
    global current_role
    message = "logout admin " + token
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
        return False
    else:
        token = ""
        current_role = ""
        return True

def logoutManager():
    global token
    global current_role
    message = "logout manager " + token
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
        return False
    else:
        token = ""
        current_role = ""
        return True

def loginUser():
    global token
    global current_role
    username = input("Username: ")
    password = input("Password: ")
    message = "login user " + username + " " + password
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        token = response_from_proxy
        print("Logged In!")
        current_role = "user"
        userPanel()

def registerUser():
    global token
    username = input("Username: ")
    password = input("Password: ")
    message = "register user " + username + " " + password
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Registered!")

def loginAdmin():
    global token
    global current_role
    username = input("Username: ")
    password = input("Password: ")
    message = "login admin " + username + " " + password
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        token = response_from_proxy
        print("Logged In!")
        current_role = "admin"
        adminPanel()

def registerAdmin():
    global token
    username = input("Username: ")
    password = input("Password: ")
    message = "register admin " + username + " " + password
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Registered!")

def loginManager():
    global token
    global current_role
    username = input("Username: ")
    password = input("Password: ")
    message = "login manager " + username + " " + password
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        token = response_from_proxy
        print("Logged In!")
        current_role = "manager"
        managerPanel()

def welcomeMenu():
    while True:
        print("Welcome to the video sharing system!")
        print("login user")
        print("register user")
        print("login admin")
        print("register admin")
        print("login manager")
        print("exit")
        selection = input("Your selection: ")
        if selection == "login user":
            loginUser()
        elif selection == "register user":
            registerUser()
        elif selection == "login admin":
            loginAdmin()
        elif selection == "register admin":
            registerAdmin()
        if selection == "login manager":
            loginManager()
        elif selection == "exit":
            break
        else:
            print("Error: wrong command")


welcomeMenu()