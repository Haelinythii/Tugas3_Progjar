import socket, sys, threading

def read_msg(client_socket):
    while True:
        data = client_socket.recv(65535)
        if len(data) == 0:
            break
        print(data)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(("127.0.0.1", 7777))

client_socket.send(bytes(sys.argv[1], "utf-8"))

client_thread = threading.Thread(target=read_msg, args=(client_socket,))
client_thread.start()

while True:

    dest = input("Masukkan username tujuan (ketikkan bcast untuk broadcast pesan):")
    msg = input("Masukkan pesan anda: ")
    client_socket.send(bytes(f"{dest}|{msg}", "utf-8"))
    if msg == "exit":
        client_socket.close()
        break