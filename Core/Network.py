import socket
import threading


class Network:
    def __init__(self):
        self.HEADER = 64
        self.PORT = 5050
        self.IP = socket.gethostbyname(
            socket.gethostname())  # auto get ip address
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"


class Server(Network):

    def __init__(self):
        super().__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.ADDR)
        self.server.bind(self.ADDR)
        self.conn_clients = []
        self.messages = []

    def _handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        self.connected = True
        while self.connected:
            self.msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if self.msg_length:
                self.msg_length = int(self.msg_length)
                self.msg = conn.recv(self.msg_length).decode(self.FORMAT)
                if self.msg == self.DISCONNECT_MESSAGE:
                    self.connected = False
                self.messages.append((addr, self.msg))
                print(f"[{addr}] {self.msg}")
                conn.send("Msg received".encode(self.FORMAT))

        conn.close()

    def _start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.IP}")
        while True:
            conn, addr = self.server.accept()
            self.conn_clients.append(conn)
            thread = threading.Thread(
                target=self._handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        print("[STARTING] server is starting...")

    def start(self):
        thread = threading.Thread(target=self._start)
        thread.start()

    def get_conn_clients(self):
        return self.conn_clients

    def send(self, conn, msg):
        conn.send(msg.encode(self.FORMAT))

    def get_messages(self):
        return self.messages


class Client(Network):

    def __init__(self):
        super().__init__()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client.connect(self.ADDR)

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        print(self.client.recv(2048).decode(self.FORMAT))

    def disconnect(self):
        send(self.DISCONNECT_MESSAGE)

    def recv(self):
        msg = self.client.recv(2048).decode(self.FORMAT)
        return msg
