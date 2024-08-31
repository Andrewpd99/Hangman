# hangman.py
import random
import requests

def fetch_random_words():
    try:
        response = requests.get('https://api.datamuse.com/words?sp=*')
        if response.status_code == 200:
            words = [word['word'] for word in response.json()]
            # Filter out words that are too short or too long for a better game experience
            filtered_words = [word for word in words if 4 <= len(word) <= 10]
            return filtered_words
        else:
            print("Failed to fetch words from the API. Using fallback list.")
            return ["fallback", "words", "only", "if", "api", "fails"]
    except requests.RequestException as e:
        print(f"An error occurred: {e}. Using fallback list.")
        return ["fallback", "words", "only", "if", "api", "fails"]

def get_random_word(words):
    return random.choice(words).upper()

def display_hangman(tries):
    stages = [
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           -
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / 
           -
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   
           -
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |   
           -
        """,
        """
           ------
           |    |
           |    O
           |    |
           |   
           -
        """,
        """
           ------
           |    |
           |    O
           |   
           |   
           -
        """,
        """
           ------
           |    |
           |    
           |   
           |   
           -
        """
    ]
    return stages[tries]

def play_hangman(word):
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6

    print("Let's play Hangman!")
    print(display_hangman(tries))
    print(word_completion)
    print("\n")

    while not guessed and tries > 0:
        guess = input("Please guess a letter or word: ").upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print(f"You already guessed the letter {guess}.")
            elif guess not in word:
                print(f"{guess} is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print(f"Good job! {guess} is in the word!")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print(f"You already guessed the word {guess}.")
            elif guess != word:
                print(f"{guess} is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Invalid input. Please guess a letter or word.")

        print(display_hangman(tries))
        print(word_completion)
        print("\n")

    if guessed:
        print(f"Congratulations! You guessed the word {word}!")
    else:
        print(f"Sorry, you ran out of tries. The word was {word}.")

def main():
    words = fetch_random_words()
    word = get_random_word(words)
    play_hangman(word)

if __name__ == "__main__":
    main()
