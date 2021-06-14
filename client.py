import socket, sys, threading, os

def read_msg(client_socket):
    while True:
        try:
            data = client_socket.recv(65535)
        except:
            break
        #print(data)

        #if len(data) == 0:
        #    break
        # print(data)
        
        command, args = data.split(b"||", 1)
        command = command.decode("utf-8")

        if command != "createFile":
            args = args.decode("utf-8")

        if command == "friendRequest":
            print(f"New friend request from {args}")
        elif command == "acceptedRequest":
            print(f"Friend request accepted! You are now friend with {args}")
        elif command == "friendList":
            friends, friendRequests  = args.split('||', 1)
            print(f"List of friend: {friends}")
            print(f"List of incoming friend request: {friendRequests}")
        elif command == "friendExist":
            print(f"{args} is already in your friend list")
        elif command == "requestExist":
            print(f"You have sent {args} a friend request before, please wait for them to accept your friend request")
        elif command == "notFriend":
            print(f"You're not friend with {args} yet or the user does not exist.")
        elif command == "notExist":
            print(f"That user does not exist.")
        elif command == "createFile":
            # print(args)
            file_size, filename, file_content = args.split(b"||", 2)
            file_size = int(file_size.decode("utf-8"))
            filename = filename.decode("utf-8")
            with open(file="./" + filename, mode="wb") as file:
                file.write(file_content)
                file_size -= len(file_content)

                while file_size > 0:
                    received_data = client_socket.recv(65535)
                    file.write(received_data)
                    file_size -= len(received_data)

            print("File created!")
        else:
            print(f"{args}")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(("127.0.0.1", 7777))

username = sys.argv[1]

client_socket.send(bytes(username, "utf-8"))

client_thread = threading.Thread(target=read_msg, args=(client_socket,))
client_thread.start()

def is_dest_self_username(dest):
    if dest == username:
        print("Can't send anything to yourself!")
        return True
    return False

while True:

    command = input("\nCommand yang tersedia:\nbcast untuk broadcast pesan ke semua teman\naddFriend untuk mengirim request pertemanan\nacceptFriend untuk menerima request pertemanan yang masuk\nfriendList untuk melihat list dari request pertemanan\nsendFile untuk mengirim file ke seorang teman\nsendMessage untuk mengirim pesan ke seorang teman\nMasukkan command: ")

    if command == "sendFile":
        filename = input("Masukkan nama file: ")

        if not os.path.exists("./" + filename):
            print("File tidak ada.")
            continue

        dest = input("Masukkan tujuan pengiriman file: ")

        if is_dest_self_username(dest):
            continue

        file_content = b""
        file_size = 0

        with open(file="./" + filename, mode="rb") as file:
            file_content = file.read()
            file_size = len(file_content)
        
        client_socket.sendall(bytes(f"{command}||{dest}||{file_size}||{filename}||", "utf-8") + file_content)
    elif command == "exit":
        client_socket.close()
        break
    else:
        if command == "friendList":
            dest = "friendList"
            args = "a"
        elif command == "addFriend" or command == "acceptFriend":
            dest = input("Masukkan nama teman anda: ")
            if is_dest_self_username(dest):
                continue
            args = "friend"
        elif command == "sendMessage":
            dest = input("Masukkan tujuan pengiriman pesan: ")
            if is_dest_self_username(dest):
                continue
            args = input("Masukkan pesan anda: ")
        elif command == "bcast":
            dest = "bcast"
            args = input("Masukkan pesan anda: ")
        else:
            print("Command tidak tersedia.")
            continue
            
        client_socket.send(bytes(f"{command}||{dest}||{args}", "utf-8"))