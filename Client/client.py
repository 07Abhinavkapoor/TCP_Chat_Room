import socket
import threading


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 48_531))
        self.start()

    def receive(self):
        while True:
            message = self.client.recv(1024).decode("ascii")
            if len(message) == 0:
                self.client.close()
                break
            print(message)

    def send(self):
        while True:
            message = input()
            self.client.send(message.encode("ascii"))

    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        send_thread = threading.Thread(target=self.send)
        receive_thread.start()
        send_thread.start()


if __name__ == "__main__":
    Client()
