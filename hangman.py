# Problem Set 2, hangman.py
# Name: 
# Collaborators: 
# Time spent: 

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"







# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
# wordlist = load_words()





# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

class HangmanGame:

  def __init__(self):
    #secret word, guessed letters, guess count, warning count
    self.wordlist = self.load_words() 

    self.secret_word = self.choose_word(self.wordlist)
    self.letters_guessed = []
    self.guesses_left = 6
    self.warnings_left = 3

  def load_words(self):
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

  def choose_word(self, wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)
  
  def is_word_guessed(self):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase //preconditiod
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for ch in set(self.secret_word): #for goes through all characters in the secret word
      if ch not in self.letters_guessed:# if char is not within letters guess list
        return False# return false
    #loop ends
    return True #returns true

  def get_guessed_word(self):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = []
    for ch in self.secret_word:
      if ch in self.letters_guessed:
        guessed_word.append(ch)
      else: 
        guessed_word.append('_ ')
    return ''.join(guessed_word)

  def get_available_letters(self):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = []
    for ch in string.ascii_lowercase:
      if ch not in self.letters_guessed:
        available_letters.append(ch)
    return ''.join(available_letters)
  
  def display_intro(self):
    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(self.secret_word)} letters long.')
    print(self.secret_word)

  def display_remaining(self, var, var_name):
    print(f'You have {var} {var_name} left.')

  def get_guess(self, accept_hint=False):
    res = input('Please guess a letter:')
    if accept_hint and res == '*':
      return res
    if res.lower().isalpha():
      return res
    return None

  def penalize_with_warning(self, warning_msg):
    if self.warnings_left:
      self.warnings_left -= 1
      print(
        f'{warning_msg} You have {self.warnings_left} warnings left:',
        self.get_guessed_word()
      )
    else:
      self.guesses_left -= 1
      print(
        f'{warning_msg} You have no warnings left so you lose one guess:',
        self.get_guessed_word()
      )
    return None

  def check_guess(self, guess):
    if guess in self.letters_guessed:
      warning_msg = "You've already guessed that letter."
      self.penalize_with_warning(warning_msg)
    elif guess in self.secret_word:
      self.letters_guessed.append(guess)
      print("Good guess:", self.get_guessed_word())
    else:
      print(
        'Oops! That letter is not in my word:',
        self.get_guessed_word()
      )
      self.letters_guessed.append(guess)
      if guess in 'aeiou':
        self.guesses_left -= 2
      else:
        self.guesses_left -= 1

    return None

  def get_score(self):
    return len(set(self.secret_word)) * self.guesses_left

  def display_loss(self): 
    print(f'Sorry, you ran out of guesses. The word was {self.secret_word}.')

  def hangman(self):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    self.display_intro()
    self.display_remaining(self.warnings_left, 'warnings')

    while self.guesses_left:
      print('-'*20)
      if self.is_word_guessed():
        print('Congratulations, you won!')
        print(f'Your total score for this game is: {self.get_score()}')
        break

      self.display_remaining(self.guesses_left, 'guesses')
      print(f'Available letters: {self.get_available_letters()}')
      guess = self.get_guess()
      if guess:
        self.check_guess(guess)
      else:
        warning_msg = "Oops! That is not a valid letter."
        self.penalize_with_warning(warning_msg)
    else:
      print('-'*20)
      self.display_loss()

  def match_with_gaps(self, my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
      corresponding letters of other_word, or the letter is the special symbol
      _ , and my_word and other_word are of the same length;
      False otherwise: 
    '''
    # remove spaces
    my_word = my_word.replace(' ', '')
    # compare lenghts
    if len(my_word) != len(other_word):
      return False
    # check each letter
    for i in range(len(my_word)):
      # skip unknown letters
      if my_word[i] == '_':
        continue
      if my_word[i] != other_word[i]:
        return False
    return True

  def show_possible_matches(self):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
        Keep in mind that in hangman when a letter is guessed, all the positions
        at which that letter occurs in the secret word are revealed.
        Therefore, the hidden letter(_ ) cannot be one of the letters in the word
        that has already been revealed.

    '''
    possible_matches = []
    for w in self.wordlist:
      if self.match_with_gaps(self.get_guessed_word(), w):
        possible_matches.append(w)
    print('Possible word matches are:')
    print(' '.join(possible_matches))

if __name__ == "__main__":
  # pass

  # To test part 2, comment out the pass line above and
  # uncomment the following two lines.
  
  # secret_word = choose_word(wordlist)
  # hangman(secret_word)

###############
  
  # To test part 3 re-comment out the above lines and 
  # uncomment the following two lines. 
  
  # secret_word = choose_word(wordlist)
  # hangman_with_hints(secret_word)
  game = HangmanGame()
  game.hangman()
