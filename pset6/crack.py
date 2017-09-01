import sys
import cs50
import crypt
import itertools
import string

def main():
    if len(sys.argv) == 2 and len(sys.argv[1]) == 13:
        hash_ = sys.argv[1]
        salt = hash_[:2]
        print(brute_force(hash_,salt))
    else:
        print("Usage: python crack.py hash")
        return 1

def brute_force(h, s):
    chars = string.ascii_lowercase + string.ascii_uppercase
    for password_length in range (1, 5):
        for guess in itertools.product(chars, repeat = password_length):
            guess = "".join(guess)
            if crypt.crypt(guess, s) == h:
                return guess

if __name__ == "__main__":
    main()