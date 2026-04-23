import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break

            parts = data.split("|", 2)
            if len(parts) == 3:
                _, _, content = parts
                print(content)

        except:
            break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5000))

username = input("Enter username: ")
client.send(f"JOIN|{len(username)}|{username}".encode())

# Start receiving thread
threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

while True:
    msg = input()
    if msg.lower() == "exit":
        client.send("EXIT|0|".encode())
        break
    client.send(f"MSG|{len(msg)}|{msg}".encode())

client.close()