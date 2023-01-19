import socket
import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 12345))
server_socket.listen(5)

def broadcast(message, server_socket):
    for sock in clients:
        sock.send(message.encode())

clients = []
clients_name = {}
while True:
    rlist, wlist, xlist = select.select([server_socket] + clients, [], [])
    for socket in rlist:
        if socket is server_socket:
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)
            username = client_socket.recv(1024).decode()
            clients_name[client_socket] = username
            message = f"{username} has joined the chat room"
            broadcast(message, server_socket)
        else:
            try:
                data = socket.recv(1024)
                if not data:
                    clients.remove(socket)
                    disconnected_user = clients_name[socket]
                    message = f"{disconnected_user} has disconnected"
                    broadcast(message, server_socket)
                else:
                    username = clients_name[socket]
                    message = f"{username}: {data.decode()}"
                    broadcast(message, server_socket)
            except:
                clients.remove(socket)
                disconnected_user = clients_name[socket]
                message = f"{disconnected_user} has disconnected"
                broadcast(message, server_socket)