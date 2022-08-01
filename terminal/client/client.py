import socket
import cv2
import struct
import imutils
import pickle

token = ""
current_role = "" # user - admin - manager

# https://nikhilroxtomar.medium.com/file-transfer-using-tcp-socket-in-python3-idiot-developer-c5cf3899819c
def upload_file_to_server(file_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.connect(("127.0.0.1", 5003))
    f = open(file_name, "rb")
    s.send(file_name.encode())
    s.recv(1024)
    data = f.read()
    s.sendall(data)
    s.recv(1024)
    f.close()
    s.close()

# https://medium.com/nerd-for-tech/developing-a-live-video-streaming-application-using-socket-programming-with-python-6bc24e522f19
def stream_file_from_server(file_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.connect(("127.0.0.1", 5004))
    s.send(file_name.encode())
    s.recv(1024)
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        should_break = False
        while payload_size > len(data):
            received_packet = s.recv(4096)
            if not received_packet:
                should_break = True
                break
            else:
                data += received_packet
        if should_break:
            break
        size = data[:payload_size]
        data = data[payload_size:]
        messageSize = struct.unpack("Q", size)[0]
        while messageSize > len(data):
            received_packet = s.recv(4096)
            data += received_packet
        raw_frame = data[:messageSize]
        data = data[messageSize:]
        frame = pickle.loads(raw_frame)
        cv2.imshow("Video", frame)
        key = cv2.waitKey(10)
        if key == 13:
            break
    s.close()

def send_to_server(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.connect(("127.0.0.1", 5002))
    s.sendall(message.encode())
    response_from_proxy = s.recv(1024).decode()
    s.close()
    return response_from_proxy

def uploadVideo():
    pass # TODO: upload video

def createVideo():
    global token
    name = input("Name: ")
    message = "create video " + token + " " + name
    response_from_proxy = send_to_server(message)
    if response_from_proxy.startswith("Error"):
        print(response_from_proxy)
    else:
        print("Created video!")

def userPanel():
    while True:
        print("Welcome to user panel!")
        print("all videos")
        print("create video")
        print("upload video")
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
        elif selection == "create video":
            createVideo()
        elif selection == "upload video":
            uploadVideo()
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
        print("upload test file")
        print("stream test file")
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
        elif selection == "login manager":
            loginManager()
        elif selection == "upload test file":
            upload_file_to_server("1.mp4")
        elif selection == "stream test file":
            stream_file_from_server("1.mp4")
        elif selection == "exit":
            break
        else:
            print("Error: wrong command")


welcomeMenu()