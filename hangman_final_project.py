import os
from time import sleep
from colorama import Fore
from termcolor import colored

def print_hangman():
    """
    this function print the open screen for hangman game
    :return: None
    """

    print(Fore.BLUE + "Welcome to the game Hangman")
    sleep(2) # to create pause between prints for visual better looking

    print(Fore.BLUE + """ 
      _    _                                         
     | |  | |                                        
     | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
     |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
     | |  | | (_| | | | | (_| | | | | | | (_| | | | |
     |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                          __/ |                      
                         |___/
                                                        """)
    sleep(2) # to create pause between prints for visual better looking

    print(Fore.GREEN + "6")

def check_valid_input(letter_guessed, old_letters_guessed):
    """
    this function check if the input from the user is valid
    :param letter_guessed: letter guessed by the player
    :param old_letters_guessed: letters that the player has guesses already
    :type letter_guessed: str
    :type old_letters_guessed: list
    :return: if the input is valid - True else - False
    :rtype: bool
    """

    return_value = False

    if (len(letter_guessed) == 1) and (letter_guessed.isalpha()) and not(letter_guessed.lower() in old_letters_guessed):

        return_value = True

    return return_value

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    this function update the list of the guessed letters
    :param letter_guessed: new guess from the player
    :param old_letters_guessed: guessed letters
    :type letter_guessed: str
    :type old_letters_guessed: str
    :return: if the guess is valid - True, else - False
    :rtype: bool
    """

    is_valid_input = check_valid_input(letter_guessed=letter_guessed, old_letters_guessed=old_letters_guessed)
    if is_valid_input:
        old_letters_guessed.insert(-1, letter_guessed.lower())

    else:
        if len(old_letters_guessed) == 0:
            print(Fore.RED + "X")
        else:
            print(Fore.RED + "X", "\n", Fore.CYAN + " -> ".join(sorted(old_letters_guessed)))


    return is_valid_input

def show_hidden_word(secret_word, old_letters_guessed):
    """
    this function return string exactly like "secret_word" - beside - every char in "secret_word"
    that not exist in "old_letters_guessed" will be replaced with "_"
    :param secret_word: the word that needed to be guised by the player
    :param old_letters_guessed: chars that already been guised by the player
    :type secret_word: str
    :type old_letters_guessed: list
    :return: return string exactly like "secret_word" - beside - every char in "secret_word" that not exist in "old_letters_guessed" will be replaced with "_"
    :rtype: str
    """

    return_value = ""
    for i in range(len(secret_word)):
        if secret_word[i] in old_letters_guessed:
            return_value += secret_word[i]
        else:
            return_value += "_"
        if i != (len(secret_word) - 1):
            return_value += " "

    return return_value

def check_win(secret_word, old_letters_guessed):
    """
    this function check if the player won - guessed all the letters in "secret_word"
    :param secret_word: the word that needed to be guised by the player
    :param old_letters_guessed: chars that already been guised by the player
    :type secret_word: str
    :type old_letters_guessed: list
    :return: if the player guessed all the letters in "secret_word" - True, else - False
    :rtype: bool
    """

    return_value = True
    for i in range(len(secret_word)):
        if secret_word[i] not in old_letters_guessed:
            return_value = False

    return return_value

def choose_word(file_path, index):
    """
    this funcion recieve text file path and a index and return
     what is the word in "index" place at the file
    :param file_path: text file path
    :param index: index for returned word
    :type file_path: str
    :type index: int
    :return: the word in "index" place at the file
    :rtype: int
    """

    file = open(file_path, 'r')
    file_content = file.read()
    file_content_list = file_content.split(" ")

    new_index = (index % len(file_content_list)) - 1
    chosen_word = file_content_list[new_index]

    return chosen_word

def hangman(secret_word):
    """
    this function recieve "secret word" and manage the game hangman around it
    :param secret_word: secret word  -the player need to guess
    :type secret_word: str
    :return: None (return use to end the game in case of win / lose)
    """

    # player maximum amount of guesses
    MAX_TRIES = 6
    # hangman possibles states along the game
    HANGMAN_PHOTOS = {1: """
    x-------x
""",
                      2: """
    x-------x
    |
    |
    |
    |
    |
""",
                      3: """
    x-------x
    |       |
    |       0
    |
    |
    |
""",
                      4: """
    x-------x
    |       |
    |       0
    |       |
    |
    |
""",
                      5: r"""
    x-------x
    |       |
    |       0
    |      /|\
    |
    |
""",
                      6: r"""
    x-------x
    |       |
    |       0
    |      /|\
    |      /
    |
""",
                      7: r"""
    x-------x
    |       |
    |       0
    |      /|\
    |      / \
    |
"""}
    # amount of guesses that been taken by the player
    num_of_tries = 0
    old_letters_guessed = []
    # The number of the image that will be printed to the player, with each failure the value increase by 1 until reach 7 include (final state)
    hangmam_number = 1
    # print to the player the initial state of the hangman
    print(Fore.RED + HANGMAN_PHOTOS[hangmam_number])
    # print to the player the initial state of the secret word
    print(Fore.GREEN + show_hidden_word(secret_word=secret_word, old_letters_guessed=old_letters_guessed))

    # run the loop - if player win/lose break order will be activated
    while True:

        # ask the player for guess
        player_guess = input(Fore.YELLOW + "Guess a letter: ")
        # check if the guess is valid, if yes - update the list of letters guessed by the player if not ask for guess again
        while not try_update_letter_guessed(letter_guessed=player_guess, old_letters_guessed=old_letters_guessed):
            player_guess = input(Fore.YELLOW + "Guess a letter: ")

        if player_guess.lower() not in secret_word:
            # print sad smile
            print(Fore.RED + ":(")
            # update hangman current state
            hangmam_number += 1
            # print to the player the current state of the hangman
            print(Fore.RED + HANGMAN_PHOTOS[hangmam_number])
            # update num of tries by +1
            num_of_tries += 1
            # if the player lose
            if num_of_tries == 6:
                # show the player the status of the secret word when he loses
                print(Fore.GREEN + show_hidden_word(secret_word=secret_word, old_letters_guessed=old_letters_guessed))
                # print LOSE
                print(Fore.MAGENTA + "LOSE")
                return

        # show the player the status of the secret word
        print(Fore.GREEN + show_hidden_word(secret_word=secret_word, old_letters_guessed=old_letters_guessed))

        # check win - if the player won - print WIN and return no value
        if check_win(secret_word=secret_word, old_letters_guessed=old_letters_guessed):
            print(Fore.MAGENTA + "WIN")
            return

def main():

    # printing opening screen
    print_hangman()
    # waiting for 4 seconds before clear the screen
    sleep(4)
    # clear opening screen
    os.system('cls')

    # keep asking for path until path is right
    while True:
        file_path = input("Enter file path: ")
        if os.path.isfile(file_path):
            break

    # keep asking for word location until give value is non-negative int type
    while True:
        index = input("Enter index: ")
        if index.isdigit():
            if (int(index) == float(index)) and (int(index) > 0):
                index = int(index)
                break

    # clear inputs requests
    os.system('cls')
    # print Let’s start!

    print(Fore.YELLOW + "Let’s start!")
    # waiting for 4 seconds before clear the screen
    sleep(4)
    # clear the screen
    os.system('cls')

    # getting the chosen word to guess
    secret_word = choose_word(file_path=file_path, index=index)
    # start the game
    hangman(secret_word)

    # waiting for 10 seconds before clear the screen to let the player see the result
    sleep(10)

    # clear the screen for game end
    os.system('cls')


if __name__ == '__main__':
    main()