import http.server
import json
import os
import random
import sys
from urllib.parse import urlparse

PORT = 8000
WORDS = ["python", "code", "alpha", "hangman", "script"]
MAX_INCORRECT = 6


class HangmanGame:

    def __init__(self):
        self.reset()

    def reset(self):
        self.secret_word = random.choice(WORDS)
        self.max_incorrect = MAX_INCORRECT
        self.incorrect_guesses = 0
        self.guessed_letters = []
        self.status = "playing"
        self.message = "Game started! Guess a letter."

    def guess(self, letter):
        if self.status != "playing":
            return self.get_state()

        letter = letter.lower().strip()
        if not letter or len(letter) != 1 or not letter.isalpha():
            self.message = "Please enter a valid single alphabetical letter."
            return self.get_state()

        if letter in self.guessed_letters:
            self.message = f"You already guessed '{letter}'."
            return self.get_state()

        self.guessed_letters.append(letter)

        if letter in self.secret_word:
            self.message = f"Good guess! '{letter}' is in the word."
            if all(ch in self.guessed_letters for ch in self.secret_word):
                self.status = "won"
                self.message = f"🎉 Congratulations! You guessed '{self.secret_word}'!"
        else:
            self.incorrect_guesses += 1
            self.message = f"Miss! '{letter}' is not in the word."
            if self.incorrect_guesses >= self.max_incorrect:
                self.status = "lost"
                self.message = f"💀 Game Over! The secret word was '{self.secret_word}'."

        return self.get_state()

    def get_state(self):
        word_display = [
            ch if (ch in self.guessed_letters or self.status != "playing") else "_"
            for ch in self.secret_word
        ]
        return {
            "word_display": word_display,
            "secret_word_length": len(self.secret_word),
            "incorrect_guesses": self.incorrect_guesses,
            "max_incorrect": self.max_incorrect,
            "remaining_guesses": max(0, self.max_incorrect - self.incorrect_guesses),
            "guessed_letters": self.guessed_letters,
            "correct_letters": [ch for ch in self.guessed_letters if ch in self.secret_word],
            "wrong_letters": [ch for ch in self.guessed_letters if ch not in self.secret_word],
            "status": self.status,
            "message": self.message,
            "secret_word": self.secret_word if self.status != "playing" else None,
        }


game = HangmanGame()


class HangmanRequestHandler(http.server.SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        sys.stdout.write(f"[HTTP] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game.get_state()).encode("utf-8"))
            return

        if parsed.path == "/" or parsed.path == "/index.html":
            file_path = os.path.join(os.path.dirname(__file__), "index.html")
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/new-game":
            game.reset()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game.get_state()).encode("utf-8"))
            return

        if parsed.path == "/api/guess":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                data = json.loads(body)
                letter = data.get("letter", "")
            except Exception:
                letter = ""

            state = game.guess(letter)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(state).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


def run(port=PORT):
    server_address = ("", port)
    httpd = http.server.ThreadingHTTPServer(server_address, HangmanRequestHandler)
    print(f"Hangman Web Game running at http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run(port)
