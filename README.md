# Hangman Game (Python)

A Hangman game built with Python featuring both console and local web interface versions.

## Features & Requirements
- **Word List:** Uses a predefined list of 5 words (`"python"`, `"code"`, `"alpha"`, `"hangman"`, `"script"`).
- **Guess Limit:** Maximum of 6 incorrect guesses allowed.
- **Game Logic:**
  - Displays revealed letters and hidden letters with underscores (`_`).
  - Tracks and displays remaining incorrect guesses and already guessed letters.
  - Validates user input (letters only, single character, rejects repeated guesses).
  - Clear victory and game over messages.

## How to Run

### 1. Console Version
Run directly in your terminal:
```bash
python3 hangman.py
```

### 2. Local Web Version
Run the local web server:
```bash
python3 server.py
```
Then open `http://localhost:8000` in your web browser.
