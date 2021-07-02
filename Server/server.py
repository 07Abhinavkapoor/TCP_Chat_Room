import socket
import threading
import json
import colors
import time
from pathlib import Path


class Server:
    def __init__(self):
        self.keywords = json.loads(Path("keywords.json").read_text())
        self.initialise_server()
        self.clients = []
        self.nicknames = []
        self.password = "12345"
        self.receive_and_accept()

    def initialise_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(("127.0.0.1", 48_531))
            print(colors.colorise("Server Initialised ........", colors.CYAN))
            self.server.listen()
            print(colors.colorise("Listening .......", colors.CYAN))
        except:
            self.initialise_server()

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message)
            except:
                nickname = self.clients.index(client)
                nickname = self.nicknames[nickname]
                self.close_connection(client, nickname)

    def handle(self, client, address, nickname):
        while True:
            message = client.recv(1024).decode("ascii")

            if len(message) == 0:
                self.close_connection(client, address, nickname)
                break

            self.broadcast(message.encode("ascii"))

    def receive_and_accept(self):
        while True:
            client, address = self.server.accept()
            client.send(self.keywords["nickname"].encode("ascii"))
            nickname = client.recv(1024).decode("ascii")
            nickname = self.validate_nickname(nickname, client)

            client.send(self.keywords["password"].encode("ascii"))
            if not self.verify(client):
                print(colors.colorise(
                    "Verification Failed: ", colors.RED) + nickname)
                self.close_connection(client, address, nickname)

            print(
                f"{address} is connnected as {colors.colorise(nickname, colors.GREEN)}")
            client.send(colors.colorise("Connected.....",
                        colors.GREEN).encode("ascii"))
            self.broadcast(
                f"{colors.colorise(nickname, colors.PURPLE)} joined the room....".encode("ascii"))
            self.clients.append(client)
            self.nicknames.append(nickname)

            thread = threading.Thread(
                target=self.handle, args=(client, address, nickname))
            thread.start()

    def verify(self, client):
        try:
            while True:
                password = client.recv(1024).decode("ascii")
                if(password == self.password):
                    break
                else:
                    client.send(colors.colorise(
                        "Invalid password.\nTry Again", colors.RED))

            client.send(self.keywords["green_signal"].encode("ascii"))
            time.sleep(0.3)
            return True
        except:
            return False

    def validate_nickname(self, nickname, client):
        while nickname in self.nicknames:
            client.send(
                colors.colorise("Nickname not available. \nChoose another nickname.", colors.RED).encode("ascii"))
            nickname = client.recv(1024).decode("ascii")

        client.send(self.keywords["green_signal"].encode("ascii"))
        time.sleep(0.3)
        return nickname

    def close_connection(self, client, address, nickname):
        self.clients.remove(client)
        self.nicknames.remove(nickname)
        self.broadcast(
            f"{colors.colorise(nickname, colors.RED)} left the room...".encode("ascii"))
        print(
            f"{address} i.e {colors.colorise(nickname, colors.RED)} is disconnected...")


if __name__ == "__main__":
    Server()
