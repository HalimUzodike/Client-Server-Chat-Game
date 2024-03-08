import socket

HOST = 'localhost'
PORT = 8888

def receive_messages(s):
    data = ""
    while True:
        chunk = s.recv(1024).decode()
        data += chunk
        if len(chunk) < 1024:
            break
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    while True:
        message = input("Enter a message (or '/q' to quit): ")
        s.sendall(message.encode())

        if message.lower() == "/q":
            break

        if message.lower() == "play hangman":
            while True:
                data = receive_messages(s)
                print(data)

                if "Congratulations!" in data or "Game over!" in data:
                    break

                guess = input().strip().lower()
                s.sendall(guess.encode())
        else:
            data = receive_messages(s)
            print(f"Received: {data}")