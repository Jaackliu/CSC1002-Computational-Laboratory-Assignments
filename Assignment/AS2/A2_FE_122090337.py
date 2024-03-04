import turtle
turtle.tracer(0)  # disable the animation

# set up the screen and the initial status bar
g_screen = turtle.Screen()
g_screen.setup(635, 670)
g_screen.bgcolor('white')
g_screen.title('Connect 4')

# set up the display of the placeholder outline
outline = turtle.Turtle()
outline.hideturtle()
outline.penup()

# set up the display of tokens
token = turtle.Turtle()
token.hideturtle()
token.penup()

# set up the display of connected tokens outline
win_token = turtle.Turtle()
win_token.hideturtle()
win_token.penup()

# create a nested list to store the board and tokens for result check
g_board = list()
for i in range(8):
    g_board.append([0, 0, 0, 0, 0, 0, 0, 0])

# set up the info of the first player, use integer 1 and 2 to indicate identification
round_player = 1


# to display the initial column trackers
def display_initial():
    # set up the turtle
    column_tracker = turtle.Turtle()
    column_tracker.hideturtle()
    column_tracker.penup()

    # set up starting position
    column_initial_x = -295
    column_initial_y = -300

    # draw the column trackers
    for blockNumber in range(8):
        column_tracker.goto(column_initial_x, column_initial_y)
        column_tracker.pendown()
        column_tracker.begin_fill()
        column_tracker.fd(60)
        column_tracker.lt(90)
        column_tracker.fd(20)
        column_tracker.lt(90)
        column_tracker.fd(60)
        column_tracker.lt(90)
        column_tracker.fd(20)
        column_tracker.lt(90)
        column_tracker.end_fill()
        column_tracker.penup()
        column_initial_x += 75


# to track the movement of mouse
def mouse_tracker(event):
    global round_column
    mouse_position = event.x

    # transfer x position to column number (0-7)
    round_column = column_detector(mouse_position)

    # display placeholder outline based on mouse position
    outline_display(round_player, round_column)


# to transfer x position of mouse to column number (0-7)
def column_detector(pos_x):
    position_code = None
    if 25 <= pos_x <= 88:
        position_code = 0
    elif 100 <= pos_x <= 163:
        position_code = 1
    elif 175 <= pos_x <= 238:
        position_code = 2
    elif 250 <= pos_x <= 313:
        position_code = 3
    elif 325 <= pos_x <= 388:
        position_code = 4
    elif 400 <= pos_x <= 463:
        position_code = 5
    elif 475 <= pos_x <= 538:
        position_code = 6
    elif 550 <= pos_x <= 613:
        position_code = 7
    return position_code


# to detect the row number (0-7) of the new token by checking the game board
def row_detector(r_column):
    if r_column is not None:

        check_row = 0
        # check each row from bottom to top in the given column, find the lowest one
        while check_row <= 7:
            if g_board[check_row][r_column] == 0:
                break
            else:
                check_row += 1  # check the next row

        return check_row


# to display the placeholder outline
def outline_display(player, column):
    if column is not None:
        outline.reset()  # clear the former outline
        outline.hideturtle()
        outline.penup()
        outline_x = -295 + 75 * column
        outline.goto(outline_x, -300)
        outline.pendown()
        # the outline color depends on the player
        if player == 1:
            outline.pencolor('blue')
        elif player == 2:
            outline.pencolor('purple')
        outline.pensize(5)
        outline.fd(60)
        outline.lt(90)
        outline.fd(20)
        outline.lt(90)
        outline.fd(60)
        outline.lt(90)
        outline.fd(20)
        outline.penup()
    else:
        outline.reset()  # clear the outline when the mouse moves away
        outline.hideturtle()
        outline.penup()


# to execute the game process of token drop, including display and win/tied check
def drop_token(x, y):
    # two 'if's to ensure the validation of row and column
    if round_column is not None:
        round_row = row_detector(round_column)

        if round_row <= 7 and g_board[round_row][round_column] == 0:
            # display the newly dropped token
            token_display(round_player, round_row, round_column)
            # record the new token in the board for win/tied checking
            g_board[round_row][round_column] = round_player
            # get the result of win/tied check
            game_code = result_check(round_player, round_row, round_column)

            # no win/tied: continue and transfer to the other player
            if game_code is None:
                player_transfer(round_column)
            # tied: inform the users
            elif game_code == 'tied':
                new_game_prompt(round_player, True)
            # win: inform the users
            else:
                win_display(game_code, round_row, round_column)
                new_game_prompt(round_player, False)
    return x, y


# to display the newly dropped token
def token_display(player, row, column):
    # calculate the location based on row and column number
    token_x = -295 + 15 * column + 60 * column + 30
    token_y = -295 + 15 * row + 60 * row + 30

    # draw the new tokens
    token.goto(token_x, token_y)
    token.pendown()
    # the color of the token depends on the player, blue for 1, purple for 2
    if player == 1:
        token.pencolor('blue')
        token.fillcolor('blue')
    elif player == 2:
        token.pencolor('purple')
        token.fillcolor('purple')
    token.begin_fill()
    token.circle(30)
    token.end_fill()
    token.penup()


# to transfer the chance of pacing token to the other player
def player_transfer(r_column):
    global round_player
    # ensure the transfer happens after valid operation
    if r_column is not None:
        if round_player == 1:
            round_player = 2
            g_screen.title('Connect 4 - Player 2 Turn')
            outline_display(round_player, r_column)
        elif round_player == 2:
            round_player = 1
            g_screen.title('Connect 4 - Player 1 Turn')
            outline_display(round_player, r_column)


# to check if the game ends up with win/tied result
def result_check(r_player, r_row, r_column):
    # 'count' are for counting the same-color tokens in each direction
    global left_count
    global right_count
    global up_count
    global down_count
    global up_left_count
    global up_right_count
    global down_left_count
    global down_right_count
    left_count = 0
    right_count = 0
    up_count = 0
    down_count = 0
    up_left_count = 0
    up_right_count = 0
    down_left_count = 0
    down_right_count = 0

    # count the same-color tokens below
    row = r_row
    while 0 <= row <= 7:
        if g_board[row][r_column] == r_player:
            down_count += 1
            row -= 1
        else:
            break

    # count the same-color tokens above
    row = r_row
    while 0 <= row <= 7:
        if g_board[row][r_column] == r_player:
            up_count += 1
            row += 1
        else:
            break

    # check if four or more tokens are connected vertically
    # the newly placed token itself is also counted, so minus 1 for eliminating it
    if up_count + down_count - 1 >= 4:
        return 'win_vertical'

    # count the same-color tokens on the left
    column = r_column
    while 0 <= column <= 7:
        if g_board[r_row][column] == r_player:
            left_count += 1
            column -= 1
        else:
            break

    # count the same-color tokens on the right
    column = r_column
    while 0 <= column <= 7:
        if g_board[r_row][column] == r_player:
            right_count += 1
            column += 1
        else:
            break

    # check if four or more tokens are connected horizontally
    if left_count + right_count - 1 >= 4:
        return 'win_horizontal'

    # count the same-color tokens on the diagonal down left
    row = r_row
    column = r_column
    while 0 <= row <= 7 and 0 <= column <= 7:
        if g_board[row][column] == r_player:
            down_left_count += 1
            row -= 1
            column -= 1
        else:
            break

    # count the same-color tokens on the diagonal upper right
    row = r_row
    column = r_column
    while 0 <= row <= 7 and 0 <= column <= 7:
        if g_board[row][column] == r_player:
            up_right_count += 1
            row += 1
            column += 1
        else:
            break

    # check if four or more token are connected diagonally upper right
    if down_left_count + up_right_count - 1 >= 4:
        return 'win_diagonal_up_right'

    # count the same-color tokens on the diagonal down right
    row = r_row
    column = r_column
    while 0 <= row <= 7 and 0 <= column <= 7:
        if g_board[row][column] == r_player:
            down_right_count += 1
            row -= 1
            column += 1
        else:
            break

    # count the same-color tokens on the diagonal upper left
    row = r_row
    column = r_column
    while 0 <= row <= 7 and 0 <= column <= 7:
        if g_board[row][column] == r_player:
            up_left_count += 1
            row += 1
            column -= 1
        else:
            break

    # check if four or more token are connected diagonally upper left
    if down_right_count + up_left_count - 1 >= 4:
        return 'win_diagonal_up_left'

    # check if the board is full
    check_full = True
    for row in g_board[7]:
        if row == 0:
            check_full = False

    # if the board is full, return the tied result
    if check_full:
        return 'tied'

    # return None if result is neither win/tied, and continue the game
    return None


# to display the connected tokens outline
def win_display(win_code, r_row, r_column):

    # to display the outline based on the given row and column
    def win_token_display(row, column):
        win_token.goto(row, column)
        win_token.pendown()
        win_token.pensize(6)
        win_token.pencolor('red')
        win_token.circle(30)
        win_token.penup()

    if win_code == 'win_horizontal':
        win_token_y = -295 + 15 * r_row + 60 * r_row + 30

        for left_column in range(left_count):
            win_token_x = -295 + 15 * (r_column - left_column) + 60 * (r_column - left_column) + 30
            win_token_display(win_token_x, win_token_y)
        # range() starts with 1 for eliminating the repetitive record in count
        for right_column in range(1, right_count):
            win_token_x = -295 + 15 * (r_column + right_column) + 60 * (r_column + right_column) + 30
            win_token_display(win_token_x, win_token_y)

    if win_code == 'win_vertical':
        win_token_x = -295 + 15 * r_column + 60 * r_column + 30

        for up_row in range(up_count):
            win_token_y = -295 + 15 * (r_row + up_row) + 60 * (r_row + up_row) + 30
            win_token_display(win_token_x, win_token_y)
        for down_row in range(1, down_count):
            win_token_y = -295 + 15 * (r_row - down_row) + 60 * (r_row - down_row) + 30
            win_token_display(win_token_x, win_token_y)

    if win_code == 'win_diagonal_up_left':
        up_row = 0
        left_column = 0
        while up_row < up_left_count and left_column < up_left_count:
            win_token_x = -295 + 15 * (r_column - left_column) + 60 * (r_column - left_column) + 30
            win_token_y = -295 + 15 * (r_row + up_row) + 60 * (r_row + up_row) + 30
            win_token_display(win_token_x, win_token_y)
            # increase the row and column by 1 to display diagonally
            up_row += 1
            left_column += 1

        down_row = 0
        right_column = 0
        while down_row < down_right_count and right_column < down_right_count:
            win_token_x = -295 + 15 * (r_column + right_column) + 60 * (r_column + right_column) + 30
            win_token_y = -295 + 15 * (r_row - down_row) + 60 * (r_row - down_row) + 30
            win_token_display(win_token_x, win_token_y)
            down_row += 1
            right_column += 1

    if win_code == 'win_diagonal_up_right':
        up_row = 0
        right_column = 0
        while up_row < up_right_count and right_column < up_right_count:
            win_token_x = -295 + 15 * (r_column + right_column) + 60 * (r_column + right_column) + 30
            win_token_y = -295 + 15 * (r_row + up_row) + 60 * (r_row + up_row) + 30
            win_token_display(win_token_x, win_token_y)
            up_row += 1
            right_column += 1

        down_row = 0
        left_column = 0
        while down_row < down_left_count and left_column < down_left_count:
            win_token_x = -295 + 15 * (r_column - left_column) + 60 * (r_column - left_column) + 30
            win_token_y = -295 + 15 * (r_row - down_row) + 60 * (r_row - down_row) + 30
            win_token_display(win_token_x, win_token_y)
            down_row += 1
            left_column += 1


# to prompt users to start a new game after game over
def new_game_prompt(r_player, is_tied):

    # clear all turtles and reset the board and player
    def new_game():
        global g_board
        global round_player
        g_screen.title('Connect 4')
        token.clear()
        win_token.clear()
        result_display.clear()
        g_board = list()
        for j in range(8):
            g_board.append([0, 0, 0, 0, 0, 0, 0, 0])
        round_player = 1
        # enable the mouse operation for the new game by combining the mouse with function
        g_canvas.bind('<Motion>', mouse_tracker)
        turtle.onscreenclick(drop_token)

    # used later for disable the mouse operation
    def disable_mouse(x, y):
        return x, y

    # set up the display of connected token
    result_display = turtle.Turtle()

    # display the result on both status bar and window
    if is_tied:
        g_screen.title('Game Tied !')
        result_display.goto(0, 200)
        result_display.write('The game is tied!\nPress the SPACE to start a new game',
                             align='center', font=('Arial', 26, 'normal'))
    else:
        if r_player == 1:
            g_screen.title('Winner ! Player 1')
            result_display.penup()
            result_display.goto(0, 200)
            result_display.pencolor('green')
            result_display.write('Player 1 (blue) wins this game!\nPress the SPACE to start a new game',
                                 align='center', font=('Arial', 26, 'normal'))
        elif r_player == 2:
            g_screen.title('Winner ! Player 2')
            result_display.penup()
            result_display.goto(0, 200)
            result_display.pencolor('green')
            result_display.write('Player 2 (purple) wins this game!\nPress the SPACE to start a new game',
                                 align='center', font=('Arial', 26, 'normal'))

    # clear the placeholder outline
    outline.clear()
    # disable the mouse operation by unbinding the mouse with function
    g_canvas.unbind('<Motion>')
    turtle.onscreenclick(disable_mouse)
    # start a new game whe users press the space
    g_screen.onkey(new_game, 'space')
    g_screen.listen()


''' The method I use ensures that as soon as the mouse moves, the outline_display function will be called.
This method will outline the placeholder more accurately than Timer and screen refresh method.'''

# track the movement of the mouse
g_canvas = turtle.getcanvas()

# mouse movement will call the mouse_tracker function to outline placeholders
g_canvas.bind('<Motion>', mouse_tracker)

# valid mouse clicking will drop a new token by calling display and check functions
turtle.onscreenclick(drop_token)

# display the initial column trackers
display_initial()

# to ensure the window won't close during the game
g_screen.mainloop()
