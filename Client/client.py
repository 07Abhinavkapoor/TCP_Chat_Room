import socket
import threading
import json
import colors
import random
from pathlib import Path


class Client:
    def __init__(self):
        self.keywords = json.loads(Path("keywords.json").read_text())
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 48_531))
        self.color = random.randint(0, 4)
        self.start()

    def get_nickname(self):
        print("Enter your nickname: ")
        self.nickname = input("> ")

    def receive(self):

        while True:
            try:
                message = self.client.recv(1024).decode("ascii")
                if len(message) == 0:
                    self.client.close()
                    break
                elif message == self.keywords["nickname"]:
                    self.set_up_profile()
                elif message == self.keywords["password"]:
                    self.validate()
                else:
                    print(message)
            except:
                break

    def validate(self):
        print("Enter password to enter the room...")
        self.client.send(input().encode("ascii"))
        message = self.client.recv(1024).decode("ascii")

        if len(message) == 0:
            self.client.close()
        elif message == self.keywords["green_signal"]:
            self.event.set()
        else:
            print(message)
            self.validate()

    def set_up_profile(self):
        self.get_nickname()
        self.client.send(self.nickname.encode("ascii"))
        message = self.client.recv(1024).decode("ascii")

        if len(message) == 0:
            self.client.close()
        elif message == self.keywords["green_signal"]:
            self.nickname = colors.colorise(self.nickname, self.color)
        else:
            print(message)
            self.set_up_profile()

    def send(self):
        self.event.wait()

        while True:
            text = input()
            if text == "":
                continue

            message = f"{self.nickname} - {text}"
            self.client.send(message.encode("ascii"))

    def start(self):
        self.event = threading.Event()

        send_thread = threading.Thread(target=self.send, daemon=True)
        send_thread.start()
        self.receive()


if __name__ == "__main__":
    Client()
