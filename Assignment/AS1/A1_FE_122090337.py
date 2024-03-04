from random import randint
from random import shuffle


# Display introduction about the game
def intro_game():
    print('Welcome to the sliding puzzle game! ')
    print('————————————————————————————————————————————————————————————————————————————————————————————————')
    print('Introduction:')
    print('On the square-framed game board, there are 8 or 15 '
          'number tiles, and an empty space where one of adjacent tiles can slide to.\nThe objective of the game '
          'is to re-arrange the tiles into a sequential order by their numbers (left to right, top to bottom) '
          '\n  by repeatedly making sliding moves (left, right, up or down). ')
    print('————————————————————————————————————————————————————————————————————————————————————————————————')
    print('How to play this game?')
    print('First, you need to define four letters on the keyboard used for left, right, up and down movement.')
    print('  Please enter four different letters in one line, and separate them with whitespaces.')
    print('Second, you can choose the game board size: ')
    print('  (1) 8-number puzzle')
    print('      It has a 3*3 square-framed board consisting of 8 square tiles, numbered 1 to 8, '
          'initially placed in random order,')
    print('  (2) 15-number puzzle ')
    print('      It has a 4*4 square-framed board consisting of 15 square tiles, numbered 1 to 15, '
          'initially placed in random order.')
    print('Third, repeatedly enter the defined letters to move the number tiles until you solve the puzzle.')
    print('————————————————————————————————————————————————————————————————————————————————————————————————')
    print('Now let’s start the game. Have fun!')


# Prompt users to enter 4 letters used for the left, right, up and down moves, and return the list of 4 letters
def define_move_letters():
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    # Check if users enter the correct number of letters, and return True if correct
    def check_number(letter_list):
        if len(letter_list) == 4:
            return True  # Return True if 4 items are entered
        else:
            print('The number of the letters is incorrect. Please enter FOUR letters.')
            return False

    # Check if users enter letters, instead of numbers, punctuation mark, etc., and return True if correct
    def check_letter(letter_list):
        for singleElement in letter_list:
            if singleElement.lower() not in alphabet:  # lower() is used to ensure case-insensitive
                print('The type of the input is incorrect. Please enter four LETTERS (a-z).')
                return False
        return True  # Return True if entered items are all letters

    # Check if users enter different letters, and return True if correct
    def check_repetition(letter_list):
        check_list = list()
        for eachLetter in letter_list:
            if eachLetter not in check_list:
                check_list.append(eachLetter)
        if len(check_list) == len(letter_list):
            return True  # Return True if 4 letters are all different
        else:
            print('There are repetitive letters. Please enter four DIFFERENT letters.')
            return False

    # Let users enter repeatedly until they enter the completely correct letters
    while True:
        input_letters = input('Enter the four letters used for left, right, up and down move > ')

        while input_letters.find(' ') != -1:
            input_letters = input_letters.replace(' ', '')  # Remove all whitespaces in the input

        input_letters_list = list()
        for singleLetter in input_letters:
            input_letters_list.append(singleLetter.lower())

        if check_number(input_letters_list) \
                and check_letter(input_letters_list) \
                and check_repetition(input_letters_list):
            return input_letters_list  # Return a list containing 4 correct letters


# Prompt users for selection of 8 puzzle, 15 puzzle or ending the game
def setting_puzzle():
    while True:
        setting_code = input('Enter “1” for 8-puzzle, “2” for 15-puzzle or “q” to end the game > ')

        while setting_code.find(' ') != -1:
            setting_code = setting_code.replace(' ', '')  # Remove all whitespaces in the input

        if setting_code == '1':
            return 3  # Return the 'size' of the puzzle, which is the side length of the game board
        elif setting_code == '2':
            return 4
        elif setting_code == 'q' or setting_code == 'Q':
            exit()  # Terminate the program
        else:
            print('The code is invalid. Please enter again.')


# Create a new, random and solvable puzzle game
def create_puzzle(size):  # size refers to the side length of the game board

    # check if the generated puzzle is solvable
    def check_puzzle_solvable(given_puzzle, empty_row_order, puzzle_size):
        global check_num
        check_puzzle = list()
        for num in given_puzzle:  # given_puzzle is a list containing all elements on the game board
            check_puzzle.append(num)  # check_puzzle is a list same as puzzle, used for solvable check
        count = 0  # It refers to the total number of pairs of reverse order numbers

        # The solvable check is based on the Reverse Order Number Theory in linear algebra
        # In a list [a, b, c], a > b, we call (a, b) a pair of reverse order numbers, short for RON
        while True:
            try:
                check_num = check_puzzle[0]
            except IndexError:
                # When board side length is 3, number of pairs of RON is even, the puzzle is solvable
                if puzzle_size == 3:
                    if count != 0 and count % 2 == 0:
                        return True  # Return True if the puzzle pass the check
                    else:
                        return False
                # When board side length is 4,
                # number of pairs of RON and difference between row order of empty tile and last tile are both even/odd,
                # then the puzzle is solvable
                elif puzzle_size == 4:
                    if count != 0 \
                            and count % 2 == 0 \
                            and (3 - empty_row_order) % 2 == 0:
                        return True
                    elif count != 0 \
                            and count % 2 == 1 \
                            and (3 - empty_row_order) % 2 == 1:
                        return True
                    else:
                        return False

            for num in check_puzzle:
                if check_num > num:
                    count += 1
            check_puzzle.remove(check_num)  # Remove the checked number

    # A function to generate random puzzles, and return the solvable puzzle after checking
    def determine_puzzle(puzzle_size):
        global determined_puzzle
        while True:
            random_puzzle = list()
            # Randomly determine the location of empty tile, record it as list index
            trial_empty_location = randint(0, puzzle_size * puzzle_size - 1)  # Location 0~8 or 0~15
            trial_empty_row = trial_empty_location // puzzle_size  # Row order 0~2 or 0~3

            for num in range(1, puzzle_size * puzzle_size):
                random_puzzle.append(num)  # Create an ordered(solved) puzzle
            shuffle(random_puzzle)  # Generate a random ordered puzzle

            if check_puzzle_solvable(random_puzzle, trial_empty_row, puzzle_size):
                if puzzle_size == 3:
                    determined_puzzle = [[], [], []]
                elif puzzle_size == 4:
                    determined_puzzle = [[], [], [], []]
                    for i in range(puzzle_size * puzzle_size - 1):
                        if random_puzzle[i] < 10:
                            random_puzzle[i] = '0' + str(random_puzzle[i])
                random_puzzle.insert(trial_empty_location, ' ')  # Insert the empty tile to the puzzle list

                # Put the solvable puzzle list into a nested list and insert the empty tile
                puzzle_index = 0
                for row in range(0, puzzle_size):
                    for column in range(0, puzzle_size):
                        determined_puzzle[row].append(str(random_puzzle[puzzle_index]))
                        puzzle_index += 1

                return determined_puzzle  # Return the nested list

    # Create a solvable puzzle as a nested list
    return determine_puzzle(size)


# Display the updated puzzle on the screen
def refresh_screen(puzzle, size):
    for row in range(0, size):
        print(end='\n')
        print('\t', end='')
        for column in range(0, size):
            print(puzzle[row][column].rjust(3), end='')
    print(end='\n')


# Let users move the empty location, and return the changed puzzle
def prompt_move(puzzle, size, move_letters):
    global stepCount, empty_column

    # Define the letters for move using move_letters from create_puzzle(...) function
    left = move_letters[0]
    right = move_letters[1]
    up = move_letters[2]
    down = move_letters[3]

    # Variables to indicate if the movement of each direction is valid
    check_left_move = True
    check_right_move = True
    check_up_move = True
    check_down_move = True

    # Locate the location of empty tile (row, column)
    empty_row = 0
    while True:
        empty_column = 0
        break_flag = False

        while empty_column <= size - 1:
            if puzzle[empty_row][empty_column] == ' ':
                break_flag = True
                break
            else:
                empty_column += 1

        if break_flag is False:
            empty_row += 1
        if break_flag is True:
            break

    # Update the validation of moving to each direction based on the location of empty tile
    if empty_column == size - 1:
        check_left_move = False
    if empty_column == 0:
        check_right_move = False
    if empty_row == size - 1:
        check_up_move = False
    if empty_row == 0:
        check_down_move = False

    # Generate the instruction of movement input
    input_instruction = '\nEnter your move ('
    if check_left_move:
        input_instruction += 'left-' + left + ', '
    if check_right_move:
        input_instruction += 'right-' + right + ', '
    if check_up_move and check_down_move:
        input_instruction += 'up-' + up + ', down-' + down
    elif check_up_move:
        input_instruction += 'up-' + up
    elif check_down_move:
        input_instruction += 'down-' + down
    input_instruction += ') > '

    # Move the tiles to empty space
    while True:
        move = input(input_instruction).lower()
        if move == left and check_left_move:
            puzzle[empty_row][empty_column] = puzzle[empty_row][empty_column + 1]
            puzzle[empty_row][empty_column + 1] = ' '
            stepCount += 1
            break
        if move == right and check_right_move:
            puzzle[empty_row][empty_column] = puzzle[empty_row][empty_column - 1]
            puzzle[empty_row][empty_column - 1] = ' '
            stepCount += 1
            break
        if move == up and check_up_move:
            puzzle[empty_row][empty_column] = puzzle[empty_row + 1][empty_column]
            puzzle[empty_row + 1][empty_column] = ' '
            stepCount += 1
            break
        if move == down and check_down_move:
            puzzle[empty_row][empty_column] = puzzle[empty_row - 1][empty_column]
            puzzle[empty_row - 1][empty_column] = ' '
            stepCount += 1
            break
        else:
            print('The input is invalid. Please enter again.')

    return puzzle  # Return the updated puzzle nested list


# Check if the puzzle is solved, and return True if the puzzle is solved
def game_is_over(puzzle, size):
    if size == 3:
        solved_puzzle = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', ' ']]
        if puzzle == solved_puzzle:
            return True
    if size == 4:
        solved_puzzle = [['01', '02', '03', '04'], ['05', '06', '07', '08'],
                         ['09', '10', '11', '12'], ['13', '14', '15', ' ']]
        if puzzle == solved_puzzle:
            return True


# Inform users that the game is over, and display the steps they use.
def display_game_over():
    print('\nCongratulations! You solved the puzzle in', stepCount, 'moves!')
    print('————————————————————————————————————————————————————————————————————————————————————————————————')
    print('You can try another puzzle, or end the game.')


''' Executive Process '''
intro_game()
game_move_letters = define_move_letters()

# The while loop below is used for repeatedly start games if users want
while True:
    stepCount = 0
    game_puzzle_size = setting_puzzle()
    game_puzzle = create_puzzle(game_puzzle_size)
    refresh_screen(game_puzzle, game_puzzle_size)

    # The while loop below is used for repeatedly prompt users to move the tiles until solving the puzzle
    while not game_is_over(game_puzzle, game_puzzle_size):
        game_puzzle = prompt_move(game_puzzle, game_puzzle_size, game_move_letters)
        refresh_screen(game_puzzle, game_puzzle_size)
    display_game_over()
