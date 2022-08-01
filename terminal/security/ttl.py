import socket
import time

def send_to_server(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.connect(("127.0.0.1", 5002))
    s.sendall(message.encode())
    response_from_proxy = s.recv(1024).decode()
    s.close()
    return response_from_proxy



# ping the server every 5 seconds
while True:
    # get current time
    start_time = int(round(time.time() * 1000))
    send_to_server("ping")
    current_time = int(round(time.time() * 1000))
    if current_time - start_time >= 20:
        print("Server has high load")
        send_to_server("refuse requests")
    time.sleep(5)
    
    