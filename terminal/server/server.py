from re import I
import threading
import time
import socket
import cv2
import struct
import imutils
import pickle

# TODO: Handles no space in contents whatsoever!

host = "127.0.0.1"
port = 5002
port_upload = 5003
port_stream = 5004

should_accept = True
should_accept_lock = threading.Lock()

ip_time = {}

class User:
    def __init__(self, username, password, number_of_removed_videos = 0):
        self.username = username
        self.password = password
        self.number_of_removed_videos = number_of_removed_videos

class Admin:
    def __init__(self, username, password, is_accepted = False, proxy_username = "", proxy_password = ""):
        self.username = username
        self.password = password
        self.is_accepted = is_accepted
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password

class Comment:
    def __init__(self, username, text):
        self.username = username
        self.text = text

class Video:
    def __init__(self, id, name, username, number_of_likes = 0, number_of_dislikes = 0, comments = [], is_tagged = False):
        self.id = id
        self.name = name
        self.username = username
        self.number_of_likes = number_of_likes
        self.number_of_dislikes = number_of_dislikes
        self.comments = comments
        self.is_tagged = is_tagged

class Ticket:
    def __init__(self, id, username, content, answer = "", status = "new"): # new, waiting, solved, closed
        self.id = id
        self.username = username
        self.content = content
        self.answer = answer
        self.status = status

all_users = []
all_admins = []
all_videos = []

all_user_admin_tickets = []
all_admin_manager_tickets = []

user_tokens = []
admin_tokens = []
manager_token = ""

def user_for_token(token):
    global user_tokens
    global all_users
    for token_dict in user_tokens:
        for key, value in token_dict.items():
            if key == token:
                for user in all_users:
                    if user.username == value:
                        return user
    return None

def admin_for_token(token, host, port):
    if not isProxy(host, port):
        return None
    global admin_tokens
    global all_admins
    for token_dict in admin_tokens:
        for key, value in token_dict.items():
            if key == token:
                for user in all_admins:
                    if user.username == value:
                        return user
    return None

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

def allVideos(data, host, port):
    token = data.split(" ")[2]
    user = user_for_token(token)
    if user == None:
        admin = admin_for_token(token, host, port)
        if admin == None:
            return "Error: not authorized"
    global all_videos
    response = ""
    for video in all_videos:
        response += "ID: " + video.id + " - Name: " + video.name + " - Username: " + video.username + " - Number of likes: " + str(video.number_of_likes) + " - Number of dislikes: " + str(video.number_of_dislikes) + " - Is tagged: " + str(video.is_tagged) + "\n"
    return response

def likeVideo(data):
    global all_videos
    token = data.split(" ")[2]
    video_id = data.split(" ")[3]
    user = user_for_token(token)
    if user == None:
        return "Error: not authorized"
    for video in all_videos:
        if video.id == video_id:
            video.number_of_likes += 1
            return "Success"
    return "Error: video not found"

def dislikeVideo(data):
    global all_videos
    token = data.split(" ")[2]
    video_id = data.split(" ")[3]
    user = user_for_token(token)
    if user == None:
        return "Error: not authorized"
    for video in all_videos:
        if video.id == video_id:
            video.number_of_dislikes += 1
            return "Success"
    return "Error: video not found"

def addComment(data):
    global all_videos
    token = data.split(" ")[2]
    video_id = data.split(" ")[3]
    text = ' '.join(data.split(" ")[4:])
    user = user_for_token(token)
    if user == None:
        return "Error: not authorized"
    for video in all_videos:
        if video.id == video_id:
            video.comments.append(Comment(user.username, text))
            return "Success"
    return "Error: video not found"

def showComments(data):
    global all_videos
    token = data.split(" ")[2]
    video_id = data.split(" ")[3]
    user = user_for_token(token)
    if user == None:
        return "Error: not authorized"
    for video in all_videos:
        if video.id == video_id:
            response = ""
            for comment in video.comments:
                response += "Username: " + comment.username + " - Text: " + comment.text + "\n"
            return response
    return "Error: video not found"

def tagVideo(data, host, port):
    global all_videos
    token = data.split(" ")[2]
    video_id = data.split(" ")[3]
    user = admin_for_token(token, host, port)
    if user == None:
        return "Error: not authorized"
    for video in all_videos:
        if video.id == video_id:
            video.is_tagged = True
            return "Success"
    return "Error: video not found"

def removeVideo(data, host, port):
    global all_videos
    token = data.split(" ")[2]
    video_id = data.split(" ")[3]
    user = admin_for_token(token, host, port)
    if user == None:
        return "Error: not authorized"
    for video in all_videos:
        if video.id == video_id:
            all_videos.remove(video) # TODO: Check if this works correctly
            for user in all_users:
                if video.username == user.username:
                    user.number_of_removed_videos += 1
            return "Success"
    return "Error: video not found"

def allAdmins(data):
    global manager_token
    global all_admins
    token = data.split(" ")[2]
    if token != manager_token:
        return "Error: not authorized"
    response = ""
    for user in all_admins:
        response += "Username: " + user.username + " - Password: " + user.password + " - Is Accepted: " + str(user.is_accepted) + "\n"
    return response
    
def authorizeAdmin(data):
    global manager_token
    global all_admins
    token = data.split(" ")[2]
    if token != manager_token:
        return "Error: not authorized"
    username = data.split(" ")[3]
    for user in all_admins:
        if user.username == username:
            user.is_accepted = True
            return "Success"
    return "Error: admin not found"

def setProxyAuth(data):
    global manager_token
    global all_admins
    token = data.split(" ")[2]
    if token != manager_token:
        return "Error: not authorized"
    username = data.split(" ")[3]
    proxy_username = data.split(" ")[4]
    proxy_password = data.split(" ")[5]
    for user in all_admins:
        if user.username == username:
            user.proxy_username = proxy_username
            user.proxy_password = proxy_password
            return "Success"
    return "Error: admin not found"

def isProxy(host, port):
    if host != "127.0.0.1":
        return False
    else:
        return True

def isProxyAuthCorrect(data, host, port):
    global all_admins
    if not isProxy(host, port):
        return "Error: not authorized"
    username = data.split(" ")[2]
    proxy_username = data.split(" ")[3]
    proxy_password = data.split(" ")[4]
    for user in all_admins:
        if user.username == username:
            if user.proxy_username != proxy_username or user.proxy_password != proxy_password:
                return "Error: proxy auth wrong"
            else:
                return "Success"
    return "Error: admin not found"

def sendUserAdminTicket(data):
    global all_user_admin_tickets
    token = data.split(" ")[2]
    content = ' '.join(data.split(" ")[3:])
    user = user_for_token(token)
    if user == None:
        return "Error: not authorized"
    all_user_admin_tickets.append(Ticket(len(all_user_admin_tickets), user.username, content))
    return "Success"

def sendAdminManagerTicket(data, host, port):
    global all_admin_manager_tickets
    token = data.split(" ")[2]
    content = ' '.join(data.split(" ")[3:])
    user = admin_for_token(token, host, port)
    if user == None:
        return "Error: not authorized"
    all_admin_manager_tickets.append(Ticket(len(all_admin_manager_tickets), user.username, content))
    return "Success"

def answerUserAdminTicket(data, host, port):
    global all_user_admin_tickets
    token = data.split(" ")[2]
    ticket_id = int(data.split(" ")[3])
    answer = ' '.join(data.split(" ")[4:])
    user = admin_for_token(token, host, port)
    if user == None:
        return "Error: not authorized"
    for ticket in all_user_admin_tickets:
        if ticket.id == ticket_id:
            if ticket.status == "closed":
                return "Error: ticket closed"
            ticket.answer = answer
            return "Success"
    return "Error: ticket ID not found"

def answerAdminManagerTicket(data):
    global all_admin_manager_tickets
    token = data.split(" ")[2]
    ticket_id = int(data.split(" ")[3])
    answer = ' '.join(data.split(" ")[4:])
    if token != manager_token:
        return "Error: not authorized"
    for ticket in all_admin_manager_tickets:
        if ticket.id == ticket_id:
            if ticket.status == "closed":
                return "Error: ticket closed"
            ticket.answer = answer
            return "Success"
    return "Error: ticket ID not found"

def seeUserAdminTickets(data, host, port):
    global all_user_admin_tickets
    token = data.split(" ")[2]
    user = user_for_token(token)
    if user == None:
        admin = admin_for_token(token, host, port)
        if admin == None:
            return "Error: not authorized"
    response = ""
    for ticket in all_user_admin_tickets:
        if user != None:
            if ticket.username == user.username:
                response += "ID: " + str(ticket.id) + " - Status: " + ticket.status + " - Content: '" + ticket.content + "' - Answer: '" + ticket.answer + "'\n"
        else:
            response += "ID: " + str(ticket.id) + " - Username: " + ticket.username + " - Status: " + ticket.status + " - Content: '" + ticket.content + "' - Answer: '" + ticket.answer + "'\n"
    return response

def seeAdminManagerTickets(data, host, port):
    global all_admin_manager_tickets
    token = data.split(" ")[2]
    admin = admin_for_token(token, host, port)
    if admin == None:
        if token != manager_token:
            return "Error: not authorized"
    response = ""
    for ticket in all_admin_manager_tickets:
        if admin != None:
            if ticket.username == admin.username:
                response += "ID: " + str(ticket.id) + " - Status: " + ticket.status + " - Content: '" + ticket.content + "' - Answer: '" + ticket.answer + "'\n"
        else:
            response += "ID: " + str(ticket.id) + " - Username: " + ticket.username + " - Status: " + ticket.status + " - Content: '" + ticket.content + "' - Answer: '" + ticket.answer + "'\n"
    return response

def markUserAdminTicket(data, host, port):
    global all_user_admin_tickets
    token = data.split(" ")[2]
    ticket_id = int(data.split(" ")[3])
    status = data.split(" ")[4]
    user = user_for_token(token)
    if user == None:
        admin = admin_for_token(token, host, port)
        if admin == None:
            return "Error: not authorized"
    for ticket in all_user_admin_tickets:
        if ticket.id == ticket_id:
            ticket.status = status
            return "Success"
    return "Error: ticket ID not found"

def markAdminManagerTicket(data, host, port):
    global all_admin_manager_tickets
    token = data.split(" ")[2]
    ticket_id = int(data.split(" ")[3])
    status = data.split(" ")[4]
    admin = admin_for_token(token, host, port)
    if admin == None:
        if manager_token != token:
            return "Error: not authorized"
    for ticket in all_admin_manager_tickets:
        if ticket.id == ticket_id:
            ticket.status = status
            return "Success"
    return "Error: ticket ID not found"

def createVideo(data):
    global all_videos
    token = data.split(" ")[2]
    name = ' '.join(data.split(" ")[3:])
    user = user_for_token(token)
    if user == None:
        return "Error: not authorized"
    if user.number_of_removed_videos >= 2:
        return "Error: strike"
    video_id = str(len(all_videos))
    all_videos.append(Video(video_id, name, user.username))
    return "Success"

def isStrike(data):
    global all_users
    token = data.split(" ")[2]
    user = user_for_token(token)
    if user == None:
        return "Error: not authorized"
    if user.number_of_removed_videos >= 2:
        return "Yes"
    return "No"

def removeStrike(data, host, port):
    global all_users
    token = data.split(" ")[2]
    username = data.split(" ")[3]
    admin = admin_for_token(token, host, port)
    if admin == None:
        return "Error: not authorized"
    for user in all_users:
        if user.username == username:
            user.number_of_removed_videos = 0
            return "Success"
    return "Error: user not found"

def allowRequests():
    global should_accept
    global should_accept_lock
    should_accept_lock.acquire()
    should_accept = True
    should_accept_lock.release()

def refuseRequests():
    global should_accept
    global should_accept_lock
    should_accept_lock.acquire()
    should_accept = False
    should_accept_lock.release()
    t = threading.Timer(2.0, allowRequests)
    t.start()
    return "Success"

def prepare_response(data, host, port):
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
    elif data.startswith("all videos"):
        return allVideos(data, host, port)
    elif data.startswith("like video"):
        return likeVideo(data)
    elif data.startswith("dislike video"):
        return dislikeVideo(data)
    elif data.startswith("add comment"):
        return addComment(data)
    elif data.startswith("show comments"):
        return showComments(data)
    elif data.startswith("tag video"):
        return tagVideo(data, host, port)
    elif data.startswith("remove video"):
        return removeVideo(data, host, port)
    elif data.startswith("all admins"):
        return allAdmins(data)
    elif data.startswith("authorize admin"):
        return authorizeAdmin(data)
    elif data.startswith("set proxy_auth"):
        return setProxyAuth(data)
    elif data.startswith("is proxy_auth_correct"):
        return isProxyAuthCorrect(data, host, port)
    elif data.startswith("send user_admin_ticket"):
        return sendUserAdminTicket(data)
    elif data.startswith("send admin_manager_ticket"):
        return sendAdminManagerTicket(data, host, port)
    elif data.startswith("answer user_admin_ticket"):
        return answerUserAdminTicket(data, host, port)
    elif data.startswith("answer admin_manager_ticket"):
        return answerAdminManagerTicket(data)
    elif data.startswith("see user_admin_tickets"):
        return seeUserAdminTickets(data, host, port)
    elif data.startswith("see admin_manager_tickets"):
        return seeAdminManagerTickets(data, host, port)
    elif data.startswith("mark user_admin_ticket"):
        return markUserAdminTicket(data, host, port)
    elif data.startswith("mark admin_manager_ticket"):
        return markAdminManagerTicket(data, host, port)
    elif data.startswith("create video"):
        return createVideo(data)
    elif data.startswith("is strike"):
        return isStrike(data)
    elif data.startswith("remove strike"):
        return removeStrike(data, host, port)
    elif data.startswith("refuse requests"):
        return refuseRequests()
    elif data.startswith("ping"):
        return "pong"
    return "Error: bad request"

# https://medium.com/nerd-for-tech/developing-a-live-video-streaming-application-using-socket-programming-with-python-6bc24e522f19
def handle_stream():
    global s_stream
    while True:
        connection, address = s_stream.accept()
        if not connection:
            continue
        file_name = connection.recv(1024).decode()
        connection.send("File name received".encode())
        try:
            video = cv2.VideoCapture(file_name)
        except:
            print("Error: file not found")
            return
        while video.isOpened():
            image, frame = video.read()
            dump = pickle.dumps(frame)
            message = struct.pack("Q", len(dump)) + dump
            try:
                connection.sendall(message)
            except:
                pass
            # cv2.imshow("Currently sending", frame)
            wait_key = cv2.waitKey(10)
            if wait_key == 13:
                connection.close()

def handle_upload_receive():
    global s_upload
    while True:
        connection, address = s_upload.accept()
        if not connection:
            continue
        file_name = connection.recv(1024).decode()
        connection.send("File name received".encode())
        try:
            file = open(file_name, "wb")
        except:
            print("Error: file not found")
            return
        while True:
            data = connection.recv(1024)
            if not data or len(data) < 1024:
                break
            file.write(data)
        file.flush()
        connection.send("File received".encode())
        file.close()
        connection.close()

def is_DDoS(source_host):
    global ip_time
    if not (source_host in ip_time):
        return False
    ip_time[source_host].sort()
    times = ip_time[source_host]
    if times == None or len(times) < 5:
        return False
    print(times[-1] - times[-2])
    if times[-1] - times[-2] < 100:
        print("DDoS!")
        return True
    return False

def accept_connection(connection, source_host, source_port):
    global should_accept
    global should_accept_lock
    global ip_time
    print("accept_connection() - Accepted connection from " + source_host + ":" + str(source_port))
    if not (source_host in ip_time):
        ip_time[source_host] = [int(round(time.time() * 1000))]
    else:
        ip_time[source_host].append(int(round(time.time() * 1000)))
    if is_DDoS(source_host):
        connection.send("Error: server is currently busy".encode())
        connection.close()
        return
    data = connection.recv(1024).decode()
    if data == "":
        return
    print("accept_connection() - Received data: '" + data + "'")
    should_accept_lock.acquire()
    local_should_accept = should_accept
    should_accept_lock.release()
    if not local_should_accept:
        connection.send("Error: server is currently busy".encode())
        connection.close()
        return
    response = prepare_response(data, source_host, source_port)
    if response != "":
        connection.sendall(response.encode())
    connection.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

# https://nikhilroxtomar.medium.com/file-transfer-using-tcp-socket-in-python3-idiot-developer-c5cf3899819c
s_upload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_upload.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_upload.bind((host, port_upload))
s_upload.listen(5)

# https://medium.com/nerd-for-tech/developing-a-live-video-streaming-application-using-socket-programming-with-python-6bc24e522f19
s_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_stream.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_stream.bind((host, port_stream))
s_stream.listen(5)

print("Welcome to server!")

threading.Thread(target=handle_upload_receive).start()
threading.Thread(target=handle_stream).start()

while True:
    connection, addr = s.accept()
    threading.Thread(target=accept_connection, args=(connection, addr[0], int(addr[1]))).start()