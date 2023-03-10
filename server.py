import socket
import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 12345))
server_socket.listen(5)

def broadcast(message, server_socket):
    for sock in clients:
        sock.send(message.encode())

def remove_user(socket):
    # Getting the disconnected client's name
    disconnected_user = clients_name[socket]
    # Removing the client
    clients.remove(socket)
    del clients_name[socket]
    # Generating the message and broadcasting it
    message = f"{disconnected_user} has disconnected"
    broadcast(message, server_socket)

clients = []
clients_name = {}
while True:
    rlist, wlist, xlist = select.select([server_socket] + clients, [], [])
    for socket in rlist:
        if socket is server_socket:
            client_socket, addr = server_socket.accept()
            username = client_socket.recv(1024).decode()
            print(f"Received username: {username}")  # Debug statement
            if username in clients_name.values():
                client_socket.send("Error: username already taken.".encode())
                client_socket.close()
            else:
                clients.append(client_socket)
                clients_name[client_socket] = username
                message = f"{username} has joined the chat room"
                broadcast(message, server_socket)
        else:
            try:
                data = socket.recv(1024)

                if not data:
                    remove_user(socket)
                
                username = clients_name[socket]
                message = f"{username}: {data.decode()}"
                broadcast(message, server_socket)
                
            except ConnectionResetError:
                remove_user(socket)