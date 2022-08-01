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
        print("all videos")
        print("like video")
        print("dislike video")
        print("add comment")
        print("show comments")
        print("see user_admin_tickets")
        print("send user_admin_ticket")
        print("mark user_admin_ticket")
        print("logout")
        selection = input("Your selection: ")
        if selection == "all videos":
            allVideos()
        elif selection == "like video":
            likeVideo()
        elif selection == "dislike video":
            dislikeVideo()
        elif selection == "add comment":
            addComment()
        elif selection == "show comments":
            showComments()
        elif selection == "see user_admin_tickets":
            seeUserAdminTickets()
        elif selection == "send user_admin_ticket":
            sendUserAdminTicket()
        elif selection == "mark user_admin_ticket":
            markUserAdminTicket()
        elif selection == "logout":
            if logoutUser():
                break

def adminPanel():
    while True:
        print("Welcome to admin panel!")
        print("all videos")
        print("tag video")
        print("remove video")
        print("see user_admin_tickets")
        print("answer user_admin_ticket")
        print("see admin_manager_tickets")
        print("send admin_manager_ticket")
        print("mark user_admin_ticket")
        print("mark admin_manager_ticket")
        print("logout")
        selection = input("Your selection: ")
        if selection == "all videos":
            allVideos()
        elif selection == "tag videos":
            tagVideo()
        elif selection == "remove videos":
            removeVideo()
        elif selection == "see user_admin_tickets":
            seeUserAdminTickets()
        elif selection == "answer user_admin_ticket":
            answerUserAdminTicket()
        elif selection == "see admin_manager_tickets":
            seeAdminManagerTickets()
        elif selection == "send admin_manager_ticket":
            sendAdminManagerTicket()
        elif selection == "mark user_admin_ticket":
            markUserAdminTicket()
        elif selection == "mark admin_manager_ticket":
            markAdminManagerTicket()
        elif selection == "logout":
            if logoutAdmin():
                break

def managerPanel():
    while True:
        print("Welcome to manager panel!")
        print("all admins")
        print("authorize admin")
        print("see admin_manager_tickets")
        print("answer admin_manager_ticket")
        print("mark admin_manager_ticket")
        print("logout")
        selection = input("Your selection: ")
        if selection == "all admins":
            allAdmins()
        elif selection == "authorize admin":
            authorizeAdmin()
        elif selection == "see admin_manager_tickets":
            seeAdminManagerTickets()
        elif selection == "answer admin_manager_tickets":
            answerAdminManagerTicket()
        elif selection == "mark admin_manager_ticket":
            markAdminManagerTicket()
        elif selection == "logout":
            if logoutManager():
                break

def markUserAdminTicket():
    global token
    ticketID = input("Ticket ID: ")
    status = input("Status (from 'new', 'waiting', 'solved' and 'closed': ")
    message = "mark user_admin_ticket " + token + " " + ticketID + " " + status
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Marked!")

def markAdminManagerTicket():
    global token
    ticketID = input("Ticket ID: ")
    status = input("Status (from 'new', 'waiting', 'solved' and 'closed': ")
    message = "mark admin_manager_ticket " + token + " " + ticketID + " " + status
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Marked!")

def seeUserAdminTickets():
    global token
    message = "see user_admin_tickets " + token
    response_from_proxy = send_to_server(message)
    print(response_from_proxy)

def seeAdminManagerTickets():
    global token
    message = "see admin_manager_tickets " + token
    response_from_proxy = send_to_server(message)
    print(response_from_proxy)

def sendUserAdminTicket():
    global token
    content = input("Content: ")
    message = "send user_admin_ticket " + token + " " + content
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Sent!")

def sendAdminManagerTicket():
    global token
    content = input("Content: ")
    message = "send admin_manager_ticket " + token + " " + content
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Sent!")

def answerUserAdminTicket():
    global token
    ticketID = input("Ticket ID: ")
    answer = input("Answer: ")
    message = "answer user_admin_ticket " + token + " " + ticketID + " " + answer
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Sent!")

def answerAdminManagerTicket():
    global token
    ticketID = input("Ticket ID: ")
    answer = input("Answer: ")
    message = "answer admin_manager_ticket " + token + " " + ticketID + " " + answer
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Sent!")

def allAdmins():
    global token
    message = "all admins " + token
    response_from_proxy = send_to_server(message)
    print(response_from_proxy)

def authorizeAdmin():
    global token
    admin_username = input("Admin username: ")
    message = "authorize admin " + token + " " + admin_username
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Authorized!")

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

def allVideos():
    global token
    message = "all videos " + token
    response_from_proxy = send_to_server(message)
    print(response_from_proxy)

def likeVideo():
    global token
    video_id = input("Video ID: ")
    message = "like video " + token + " " + video_id
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Liked!")

def dislikeVideo():
    global token
    video_id = input("Video ID: ")
    message = "dislike video " + token + " " + video_id
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Disliked!")

def addComment():
    global token
    video_id = input("Video ID: ")
    text = input("Comment text: ")
    message = "add comment " + token + " " + video_id + " " + text
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Added comment!")

def showComments():
    global token
    video_id = input("Video ID: ")
    message = "show comments " + token + " " + video_id
    response_from_proxy = send_to_server(message)
    print(response_from_proxy)

def tagVideo():
    global token
    video_id = input("Video ID: ")
    message = "tag video " + token + " " + video_id
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Tagged!")

def removeVideo():
    global token
    video_id = input("Video ID: ")
    message = "remove video " + token + " " + video_id
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Removed!")

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