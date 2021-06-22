import socket


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 48_531))
        self.start()

    def start(self):
        while True:
            message = self.client.recv(1024).decode("ascii")
            if len(message) == 0:
                self.client.close()
                break
            print(message)


if __name__ == "__main__":
    Client()
