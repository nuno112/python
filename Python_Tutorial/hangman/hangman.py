from random import randrange
from data import *
from helpers import *


if __name__ == "__main__":
    name = input("Insert your name: ")
    print("\nHello, " + name + "!\n")
    word = wordList[randrange(0, len(wordList))]
    guessedWord = list("*" * len(word))
    attempts = []
    while numOfAttempts > 0:
        print("\nTry to guess the word: " + "".join(guessedWord))
        attempt = input("Attempt letter: ")
        if len(attempt) != 1:
            print("\nPlease insert one letter only.")
        else:
            if attempt not in attempts:
                attempts.append(attempt)
                for i, letter in enumerate(word):
                    if letter == attempt:
                        guessedWord[i] = attempt
                if "".join(guessedWord) == word:
                    score = numOfAttempts
                    print("\nYou won!! The word was: " + "".join(guessedWord) +
                          ". You scored " + str(score) + " points.")
                    updateScoreFile(name, score)
                    break
                else:
                    numOfAttempts -= 1
                    print("\nYou have " + str(numOfAttempts) +
                          " attempts remaining.")
            else:
                print("\nYou already tried that letter!")
