"""
TODO:
- Implement game
- Impelemente a leadercore (in a csv)
- Implement statistics
- Implement list of letters already chosen


"""
from datetime import datetime
from random import randint
import pandas as pd

df_players = pd.read_csv('players.csv')

def get_time():
    now = datetime.now()
    t = now.strftime("%H:%M:%S")
    (h, m, s) = t.split(':')
    result = (int(h) * 3600 + int(m) * 60 + int(s)) / (60 * 60)
    if 5 <= result < 12:
        maen = 'morning'
    elif 12 <= result < 18:
        maen = 'afternoon'
    elif 18 <= result < 22:
        maen = 'evening'
    else:
        maen = 'night'

    return maen

def get_name(maen, name, first_time):
    if first_time:
        name = input("""\nHello! Good {}! Welcome to the Hangman® game by Edoardo Nervo.\n
Please write your name: """.format(maen))
        print("Hello {}! Nice to meet you!".format(name))
    else:
        change_name = True
        while change_name:
            choice = input("Hello again! Are you always {}? [Y/n]:".format(name))
            if choice == 'Y':
                print("Hello again {}! Missed you!".format(name))
                change_name = False
            elif choice == 'n':
                new_name = input('Okay then! What is your name?: ')
                dupl_name = True
                while dupl_name:
                    if new_name == name:
                        new_name = input("Oh no! This name has been already taken!\n"
                                         "Please choose another one: ")
                        if new_name != name:
                            name = new_name
                            dupl_name = False
                    else:
                        name = new_name
                        dupl_name = False
                change_name = False
                print("Hello {}! Nice to meet you!".format(name))
            else:
                print('Please, select one of following options: [Y/n]!!')
    return name


def get_word():
    with open("hangman_words.txt") as f:
        lines = f.readlines()
    lines = [line.strip('\n') for line in lines]
    rng_index = randint(0, len(lines) - 1)
    word = lines[rng_index]
    return word


def partial_word(guessed_indexes, word):
    """Display partial world"""
    for i in range(len(word)):
        if i in guessed_indexes:
            print(word[i], end=' ')
        else:
            print(' ', end=' ')
    print("")
    for i in range(len(word)):
        print('_ ', end='')
    print("\n\n")


def find_all(s, ch):
    """Return a list of all indexes for a char in string"""
    return [i for i, ltr in enumerate(s) if ltr == ch]


def find_word(pics, word):
    """Try to find word"""
    # Initialization
    guessed_indexes = []  # List of correctly guessed letter index
    # Guessing starts
    print("\nThe word has been chosen!"
          "Try to guess it!\n")
    errors = 0  # Counter of wrong guess (errors)
    guessing = True  # Loop of player trying to find the word

    while guessing:
        print(pics.iloc[errors].values[0], end='\n\n')
        partial_word(guessed_indexes, word)
        good_Letter = True  # Loop on validity of the letter
        while good_Letter:
            guessed_letter = input('Choose a letter: ')
            if len(guessed_letter) == 1 and \
                    guessed_letter.isalpha() and (
                    guessed_letter not in [word[i] for i in guessed_indexes]):
                good_Letter = False
            elif guessed_letter in [word[i] for i in guessed_indexes]:
                print('You have already chosen letter {}, try again!\n'.format(guessed_letter))
            elif len(guessed_letter) > 1 and guessed_letter.isalpha():
                print('You have chosen more than one letter, retry:\n')
            elif len(guessed_letter) == 1 and (not guessed_letter.isalpha()):
                print('{} is not a letter from english alphabet'.format(guessed_letter))
            else:
                print('You have chosen multiple letters and they are not even letters')

        if guessed_letter in word:  # TODO: Check for doubles
            print("Correct! Letter '{}' is in the word!".format(guessed_letter))
            guessed_indexes.extend(find_all(word, guessed_letter))  # TODO: could cause problems
        else:
            print('Oh no! Letter "{}" is not in the word'.format(guessed_letter))
            errors += 1

        # Interrupt cycle if word is found or errors >=6
        if len(guessed_indexes) == len(word):
            # Word is found
            print('Congratulations, {} is the correct word!!'.format(word))
            guessing = False

        if errors > 5:
            print('Oh no! You lose! Correct word is "{}"'.format(word))
            guessing = False


def main():
    first_time = True  # Booleans that indicates first loop
    game = True  # Loop game
    name = None  # Name initialization
    maen = get_time()  # Get local time
    pics = pd.read_csv('hangman_pics.csv', index_col=0)  # Pics of state of hangman

    while game:
        name = get_name(maen, name, first_time)  # Get name of the player
        first_time = False
        word = get_word()  # Word to be guessed
        print('Correct word is "{}"'.format(word))
        find_word(pics, word)  # Finding the word

        cont = input('\nAnother game?: [Y/n] ')
        print("")
        if cont == 'n':
            game = False
            print('Bye {}! See you soon!'.format(name))


if __name__ == '__main__':
    main()
