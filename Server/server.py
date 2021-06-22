import socket


class Server:
    def __init__(self):
        self.initialise_server()
        self.receive_and_accept()

    def initialise_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 48_531))
        print("Server Initialised ........")
        self.server.listen()
        print("Listening .......")

    def receive_and_accept(self):
        while True:
            client, address = self.server.accept()
            print(f"{address} is connnected")
            client.send("Thanks for connecting".encode("ascii"))
            client.close()


if __name__ == "__main__":
    Server()
