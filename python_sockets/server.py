import socket
import threading 

FORMAT = 'utf-8'
HEADER = 64
PORT = 5050
SERVER = "127.0.0.1"
#SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print("[NEW CONNECTION] {addr} connected.")
    connected = True 
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("Msg recived".encode(FORMAT))
    conn.close()

def start():
    #Allow server to start listening to connections
    server.listen()
    print(f"[LISTENING] on {ADDR}") 
    while True:
        #Addr is the ip:port of the inbound connection; conn a object by which to interact w/ said connection
        conn, addr = server.accept() 
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
