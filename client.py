import socket, sys, threading

def read_msg(client_socket):
    while True:
        
        data = client_socket.recv(65535)

        if len(data) == 0:
            break
        print(data)
        
        command, args = data.split(b"||", 1)
        command = command.decode("utf-8")

        if command != "createFile":
            args = args.decode("utf-8")

        if command == "friendRequest":
            print(f"New friend request from {args}")
        elif command == "acceptedRequest":
            print(f"Friend request accepted! You are now friend with {args}")
        elif command == "friendRequestList":
            print(f"List of friend request: {args}")
        elif command == "friendExist":
            print(f"{args} is already in your friend list")
        elif command == "requestExist":
            print(f"You have sent {args} a friend request before, please wait for them to accept your friend request")
        elif command == "notFriend":
            print(f"You're not friend with {args} yet.")
        elif command == "createFile":
            file_size, filename, file_content = args.split(b"||")
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

client_socket.send(bytes(sys.argv[1], "utf-8"))

client_thread = threading.Thread(target=read_msg, args=(client_socket,))
client_thread.start()

while True:

    command = input("Masukkan command (ketikkan bcast untuk broadcast pesan):")

    if command == "sendFile":
        filename = input("Masukkan nama file:")
        dest = input("Masukkan tujuan pengiriman file:")

        file_content = b""
        file_size = 0

        with open(file="./" + filename, mode="rb") as file:
            file_content = file.read()
            file_size = len(file_content)
        
        client_socket.sendall(bytes(f"{command}||{file_size}||{dest}||{filename}||", "utf-8") + file_content)
    elif command == "friendRequestList":
        client_socket.send(bytes(f"{command}||a", "utf-8"))
    else:
        msg = input("Masukkan pesan anda: ")
        client_socket.send(bytes(f"{command}||{msg}", "utf-8"))

    if command == "exit":
        client_socket.close()
        break
