# Author: Chukwuhalim Uzodike
# GitHub username: HalimUzodike
# Date: 03/09/2024
# Description: A simple server that plays Hangman with a client.
# References:
# [1] https://docs.python.org/3/library/socket.html
# [2] https://docs.python.org/3/library/socket.html#socket.socket.recv
# [3] https://docs.python.org/3/library/socket.html#socket.socket.sendall
# [4] https://docs.python.org/3/library/socket.html#socket.socket.bind
# [5] https://docs.python.org/3/library/socket.html#socket.socket.listen
# [6] https://docs.python.org/3/library/socket.html#socket.socket.accept
# [7] https://gaia.cs.umass.edu/kurose_ross/online_lectures.htm


from socket import *
from hangman_art import stages

HOST = 'localhost'
PORT = 8888


def play_hangman(conn):
    """Play a game of Hangman."""

    word = "python"
    guessed_letters = set()
    max_attempts = len(stages) - 1
    attempts = 0

    while True:
        display_word = "".join([letter if letter in guessed_letters else "_" for letter in word])       # Display the word with guessed letters
        conn.sendall(f"{stages[attempts]}\nWord: {display_word}\nAttempts: {attempts}/{max_attempts}\n".encode())       # Send game status to client

        if "_" not in display_word:
            conn.sendall("Congratulations! You guessed the word correctly.\n".encode())
            break

        if attempts >= max_attempts:
            conn.sendall(f"{stages[attempts]}\nGame over! The word was: {word}\n".encode())
            break

        conn.sendall("Enter a letter: ".encode())
        letter = conn.recv(1024).decode().strip().lower()

        if letter in guessed_letters:
            conn.sendall("You already guessed that letter. Try again.\n".encode())     # Reject repeated guesses
        elif letter in word:
            guessed_letters.add(letter)
            conn.sendall("Correct guess!\n".encode())    # Accept correct guesses
        else:
            attempts += 1
            conn.sendall(f"Wrong guess!\n".encode())    # Accept wrong guesses


with socket(AF_INET, SOCK_STREAM) as s:
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    print("Waiting for a connection...")
    print("Type /q to quit")
    print("Enter message to send. Please wait for input prompt before entering message...")

    conn, addr = s.accept()
    print(f"Connected by {addr}")

    connected = True
    game_active = False
    while connected:
        data = conn.recv(1024).decode().strip()     # Receive data from client

        if data == '/q':
            connected = False
            print("Client has requested shutdown. Shutting down!")
            break

        if data == "play hangman":
            print("Now playing Hangman!")
            game_active = True
            conn.sendall("Now playing Hangman!\n".encode())

        if game_active:
            play_hangman(conn)          # Play Hangman
            game_active = False
            continue

        if data and not game_active:
            print(f"Received: {data}")
            reply = input("Enter a reply: ")        # Get reply from server

            if reply == '/q':
                connected = False
                print("Shutting down!")             # Shutdown the server

            conn.sendall(reply.encode())

    conn.close()
