# Client-Server-Chat-Game
## Hangman Client-Server Game


This project is a simple implementation of the classic Hangman game using a client-server architecture. The server hosts the game, and the client connects to the server to play the game.

## Files

- `server.py`: This file contains the server-side code for the Hangman game. It listens for incoming connections, manages the game state, and communicates with the client.
- `client.py`: This file contains the client-side code for the Hangman game. It connects to the server, sends user input, and displays the game progress.
- `hangman_art.py`: This file contains the ASCII art for the different stages of the hangman figure.

## How to Run

1. Start the server by running `python server.py` in a terminal window.
2. In another terminal window, start the client by running `python client.py`.
3. Follow the prompts in the client terminal to play the game. Type `play hangman` to start a new game.
4. Guess letters to uncover the hidden word. If you guess incorrectly, the hangman figure will be drawn progressively. You have a limited number of attempts to guess the word correctly.
5. To quit the game, type `/q` in either the server or client terminal.

## Requirements

- Python 3.x

## Author

- Halim Uzodike

## References

- Python Socket Programming Documentation
- Kurose Ross Online Lectures