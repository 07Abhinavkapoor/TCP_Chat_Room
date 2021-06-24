import socket
import threading
import json
from pathlib import Path


class Server:
    def __init__(self):
        self.keywords = json.loads(Path("keywords.json").read_text())
        self.initialise_server()
        self.clients = []
        self.nicknames = []
        self.receive_and_accept()

    def initialise_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 48_531))
        print("Server Initialised ........")
        self.server.listen()
        print("Listening .......")

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client, address, nickname):
        while True:
            message = client.recv(1024).decode("ascii")

            if len(message) == 0:
                self.close_connection(client)
                print(f"{address} i.e {nickname} is disconnected...")
                break

            self.broadcast(message)

    def receive_and_accept(self):
        while True:
            client, address = self.server.accept()

            client.send(self.keywords["nickname"].encode("ascii"))
            nickname = client.recv(1024).decode("ascii")
            nickname = self.validate_nickname(nickname, client)

            print(f"{address} is connnected as {nickname}")
            self.clients.append(client)
            self.nicknames.append(nickname)

            thread = threading.Thread(
                target=self.handle, args=(client, address, nickname))
            thread.start()

    def validate_nickname(self, nickname, client):
        while nickname in self.nicknames:
            client.send(
                "Nickname not available. \nChoose another nickname:".encode("ascii"))
            nickname = client.recv(1024).decode("ascii")

        return nickname

    def close_connection(self, client):
        self.clients.remove(client)
        self.broadcast(f"{client} left the room...".encode("ascii"))


if __name__ == "__main__":
    Server()
