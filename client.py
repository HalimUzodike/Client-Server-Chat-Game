# Author: Chukwuhalim Uzodike
# GitHub username: HalimUzodike
# Date: 03/09/2024
# Description: A simple client that plays Hangman with a server.
# References:
# [1] https://docs.python.org/3/library/socket.html
# [2] https://docs.python.org/3/library/socket.html#socket.socket.recv
# [3] https://docs.python.org/3/library/socket.html#socket.socket.sendall
# [4] https://docs.python.org/3/library/socket.html#socket.socket.bind
# [5] https://docs.python.org/3/library/socket.html#socket.socket.listen
# [6] https://docs.python.org/3/library/socket.html#socket.socket.accept
# [7] https://gaia.cs.umass.edu/kurose_ross/online_lectures.htm


from socket import *

HOST = 'localhost'
PORT = 8888


def receive_messages(s):
    """Receive messages from the server."""

    data = ""
    while True:
        chunk = s.recv(1024).decode()
        data += chunk
        if len(chunk) < 1024:
            break
    return data


with socket(AF_INET, SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")
    print("Type /q to quit")
    print("Enter message to send. Please wait for input prompt before entering message...")
    print("Note: Type 'play hangman' to start a game of Hangman")

    connected = True
    while connected:
        game_active = False
        message = input("Enter Input: ")

        if message == "":
            print("Please enter a message.")
            continue

        if message == '/q':
            connected = False
            print("Shutting down!")

        if message == "play hangman":
            s.sendall(message.encode())
            game_active = True

        if game_active:
            while True:
                data = receive_messages(s)
                print(data)

                if "Congratulations!" in data or "Game over!" in data:
                    break

                if "Enter a letter:" in data:
                    guess = input().strip().lower()
                    s.sendall(guess.encode())
            continue

        if not game_active:
            s.sendall(message.encode())
            data = receive_messages(s)

        if data == '/q':
            connected = False
            print("Server has requested shutdown. Shutting down!")
            break

        if data and not game_active:
            print(f"Received: {data}")

    s.close()
