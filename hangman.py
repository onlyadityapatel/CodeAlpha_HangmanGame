import random


def play_hangman():
    word_list = ["python", "code", "alpha", "hangman", "script"]
    secret_word = random.choice(word_list)
    max_incorrect_guesses = 6
    incorrect_guesses_count = 0
    guessed_letters = []

    print("=" * 45)
    print("           WELCOME TO HANGMAN GAME           ")
    print("=" * 45)
    print(f"The word has {len(secret_word)} letters.")
    print(f"You have {max_incorrect_guesses} incorrect guesses allowed.\n")

    while incorrect_guesses_count < max_incorrect_guesses:
        displayed_word = []
        for letter in secret_word:
            if letter in guessed_letters:
                displayed_word.append(letter)
            else:
                displayed_word.append("_")

        print("Word to guess: " + " ".join(displayed_word))

        if "_" not in displayed_word:
            print("\n Congratulations! You won! You guessed the word:", secret_word)
            print("=" * 45)
            return

        remaining_guesses = max_incorrect_guesses - incorrect_guesses_count
        print(f"Remaining incorrect guesses: {remaining_guesses}")
        print("Already guessed letters: " + (", ".join(guessed_letters) if guessed_letters else "None"))

        guess = input("Enter a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("\n Invalid input! Please enter a single letter.\n")
            continue

        if guess in guessed_letters:
            print(f"\n You have already guessed '{guess}'. Try another letter.\n")
            continue

        guessed_letters.append(guess)

        if guess in secret_word:
            print(f"\n Good guess! '{guess}' is in the word.\n")
        else:
            incorrect_guesses_count += 1
            print(f"\n Incorrect guess! '{guess}' is not in the word.\n")

    print("=" * 45)
    print(" Game Over! You have exceeded the maximum incorrect guesses.")
    print(f"The secret word was: '{secret_word}'")
    print("=" * 45)


if __name__ == "__main__":
    play_hangman()
