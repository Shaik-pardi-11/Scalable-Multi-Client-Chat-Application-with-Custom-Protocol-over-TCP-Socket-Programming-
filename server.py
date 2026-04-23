import socket
import threading

clients = {}  # conn -> username

def broadcast(message, sender_conn=None):
    for conn in clients:
        if conn != sender_conn:
            try:
                conn.send(message.encode())
            except:
                pass

def handle_client(conn, addr):
    print(f"Connected: {addr}")
    
    username = "Unknown"
    
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            parts = data.split("|", 2)
            if len(parts) != 3:
                continue

            msg_type, length, content = parts

            if msg_type == "JOIN":
                username = content
                clients[conn] = username
                broadcast(f"MSG|{len(username)+10}|{username} joined", conn)

            elif msg_type == "MSG":
                full_msg = f"{username}: {content}"
                print(full_msg)
                broadcast(f"MSG|{len(full_msg)}|{full_msg}", conn)

            elif msg_type == "EXIT":
                break

        except:
            break

    print(f"Disconnected: {addr}")
    if conn in clients:
        left_user = clients[conn]
        del clients[conn]
        broadcast(f"MSG|{len(left_user)+10}|{left_user} left")

    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 5000))
server.listen()

print("Server running on port 5000...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()