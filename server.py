import socket

HOST = 'localhost'
PORT = 8888


def play_hangman(conn):
    word = "python"
    guessed_letters = set()
    max_attempts = 6
    attempts = 0

    while True:
        display_word = "".join([letter if letter in guessed_letters else "_" for letter in word])
        conn.sendall(f"Word: {display_word}\n".encode())

        if "_" not in display_word:
            conn.sendall("Congratulations! You guessed the word correctly.\n".encode())
            break

        if attempts >= max_attempts:
            conn.sendall(f"Game over! The word was: {word}\n".encode())
            break

        conn.sendall("Enter a letter: ".encode())
        letter = conn.recv(1024).decode().strip().lower()

        if letter in guessed_letters:
            conn.sendall("You already guessed that letter. Try again.\n".encode())
        elif letter in word:
            guessed_letters.add(letter)
            conn.sendall("Correct guess!\n".encode())
        else:
            attempts += 1
            conn.sendall(f"Wrong guess! Attempts left: {max_attempts - attempts}\n".encode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                print(f"Received: {data}")

                if data.lower() == "play hangman":
                    play_hangman(conn)
                elif data.lower() == "/q":
                    break
                else:
                    reply = input("Enter a reply: ")
                    conn.sendall(reply.encode())
