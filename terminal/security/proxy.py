import socket
import threading

host = "127.0.0.1"
port = 6001

authorized_pairs = []

def send_to_server(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.connect(("127.0.0.1", 5002))
    s.sendall(message.encode())
    response_from_proxy = s.recv(1024).decode()
    s.close()
    return response_from_proxy

def authorizeProxy(data):
    username = data.split(" ")[2]
    proxy_username = data.split(" ")[3]
    proxy_password = data.split(" ")[4]
    result = send_to_server("is proxy_auth_correct " + username + " " + proxy_username + " " + proxy_password)
    return result.startswith("Success")

def accept_connection(connection, source_host, source_port):
    global authorized_pairs
    print("accept_connection() - Accepted connection from " + source_host + ":" + str(source_port))
    data = connection.recv(1024).decode()
    if data == "":
        return
    print("accept_connection() - Received data: '" + data + "'")
    if data.startswith("authorize proxy") and authorizeProxy(data):
        authorized_pairs.append((source_host, source_port))
        connection.send("Success".encode())
    else:
        if (source_host, source_port) in authorized_pairs:
            connection.sendall(send_to_server(data))
        else:
            connection.send("Error: not authorized")
    connection.close()



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)

while True:
    connection, addr = s.accept()
    threading.Thread(target=accept_connection, args=(connection, addr[0], int(addr[1]))).start()