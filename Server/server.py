import socket
import threading


class Server:
    def __init__(self):
        self.initialise_server()
        self.clients = []
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

    def handle(self, client, address):
        while True:
            message = client.recv(1024)

            if len(message) == 0:
                self.close_connection(client)
                print(f"{address} is disconnected...")
                break

            self.broadcast(message)

    def receive_and_accept(self):
        while True:
            client, address = self.server.accept()
            print(f"{address} is connnected")
            self.clients.append(client)
            thread = threading.Thread(
                target=self.handle, args=(client, address))
            thread.start()

    def close_connection(self, client):
        self.clients.remove(client)
        self.broadcast(f"{client} left the room...".encode("ascii"))


if __name__ == "__main__":
    Server()
