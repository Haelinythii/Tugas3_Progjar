import socket, threading

def read_msg(clients, client_socket, client_address, client_username):
    while True:
        data = client_socket.recv(65535)
        if len(data) == 0:
            break
        
        command, args = data.decode("utf-8").split("|")
        msg = "<{}>: {}".format(client_username, args)
        
        if command == "bcast":
            send_broadcast(clients, msg, client_address)
            print(f"{client_username} kirim pesan")
        elif command == "addFriend":
            print(command)
            new_friend_socket = clients[args][0]
            req_friend(client_username, args, client_socket, new_friend_socket)
            print(client_friend)
        elif command == "acceptFriend":
            print(command)
            new_friend_socket = clients[args][0]
            add_friend(client_username, args, client_socket, new_friend_socket)
            print(client_friend)
        elif command == "friendRequestList":
            print(command)
            retval = ', '.join(client_friend_request[client_username])
            client_socket.send(bytes(f"friendRequestList||{retval}", "utf-8"))
        else:
            print(command)
            dest_client_socket = clients[command][0]
            send_msg(dest_client_socket, msg)
            print(f"{client_username} kirim pesan")
        print(data)
    
    client_socket.close()
    print("Connection closed", client_address)

def send_broadcast(clients, data, sender_client_address):
    for client_sock, client_addr, _ in clients.values():
        if not (sender_client_address[0] == client_addr[0] and sender_client_address[1] == client_addr[1]):
            send_msg(client_sock, data)

def send_msg(client_socket, data):
    client_socket.send(bytes(data, "utf-8"))

def add_friend(client_username, new_friend, client_socket, new_friend_socket):
    if new_friend not in client_friend[client_username] and check_client_exist(new_friend):

        if new_friend in client_friend_request[client_username]:
            client_friend_request[client_username].remove(new_friend)
        
        if client_username in client_friend_request[new_friend]:
            client_friend_request[new_friend].remove(client_username)
        
        client_friend[client_username].append(new_friend)
        client_friend[new_friend].append(client_username)

        client_socket.send(bytes(f"acceptedRequest||{new_friend}", "utf-8"))
        new_friend_socket.send(bytes(f"acceptedRequest||{client_username}", "utf-8"))

        

def req_friend(client_username, new_friend, client_socket, new_friend_socket):
    if client_username in client_friend_request[new_friend]:
        add_friend(client_username, new_friend, client_socket, new_friend_socket)
    elif new_friend not in client_friend_request[client_username] and check_client_exist(new_friend):
        #client_friend_request[client_username].append(new_friend)
        client_friend_request[new_friend].append(client_username)
        new_friend_socket.send(bytes(f"friendRequest||{client_username}", "utf-8"))

def check_client_exist(username):
    print(clients.keys())
    if username in clients.keys():
        print("True")
        return True
    print("False")
    return False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 7777))
server_socket.listen(5)
clients = {}

client_friend = {}

client_friend_request = {}

while True:
    client_socket, client_address = server_socket.accept()
    client_username = client_socket.recv(65535).decode("utf-8")
    print(client_username, " Joined")
    
    client_thread = threading.Thread(target=read_msg, args=(clients, client_socket, client_address, client_username))
    client_thread.start()

    clients[client_username] = (client_socket, client_address, client_thread)
    client_friend[client_username] = []
    client_friend_request[client_username] = []