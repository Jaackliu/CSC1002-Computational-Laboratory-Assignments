import turtle
import random
from random import randrange, randint
turtle.tracer(0)  # disable the animation

# set up the screen and the initial status bar
g_screen = turtle.Screen()
g_screen.setup(580, 660)
g_screen.title('Snake')

# set up the status area
g_status = turtle.Turtle()
g_status.hideturtle()
g_status.penup()
g_status.goto(-210, 240)

'''the position of the snake and monster will be stored in list [x, y],
from [0, 0] at the left bottom to [24, 24] at the right top, later used in turtle display.'''

# set up the snake head and initial position
snake_head = turtle.Turtle("square")
snake_head.color('red')
snake_head.left(90)
snake_head.penup()
head_current_location = [12, 12]
head_target_location = []

# set up the snake tail and initial position
snake_tail = turtle.Turtle("square")
snake_tail.color('black')
snake_tail.hideturtle()
snake_tail.penup()
snake_tail.pencolor('blue')
snake_tail_length = 0
snake_tail_expand_num = 5  # initial tail length is 5
snake_tail_position = []

# set up the monster and random initial position
monster = turtle.Turtle('square')
monster.color('purple')
monster.penup()
monster_target_location = [12, 12]
while 7 <= monster_target_location[0] <= 17:  # to ensure monster is enough far from snake
    monster_target_location[0] = randrange(0, 24, 1)
while 7 <= monster_target_location[1] <= 17:
    monster_target_location[1] = randrange(0, 24, 1)
monster_current_location = monster_target_location

# set up some gaming initial parameters
g_time = 0  # gaming time
g_contact = 0  # snake tail and monster contact time
snake_motion = 'Paused'  # initial snake motion status
former_snake_motion = 'Paused'
snake_speed = 200  # initial snake speed
monster_speed = 500  # initial monster speed
is_start_time = True  # True if the game starts
is_end_time = False  # True if the game ends
valid_food_list = [1, 2, 3, 4, 5]  # food left for eating
hide_food_list = []  # food hide in the round
only_count = 0  # used to make the left food shown to reduce difficulty


# refresh the data and display the status bar
def refresh_status_bar():
    g_status.clear()
    g_status.write('Contact: ' + str(g_contact) + '          Time: ' + str(g_time)
                   + '          Motion: ' + snake_motion, font=('Arial', 16, 'bold'))


# refresh the game time every second after start
def refresh_time():
    global g_time
    global is_start_time
    global is_end_time

    if is_start_time:
        is_start_time = False
        g_screen.ontimer(refresh_time, 1000)
    else:
        if not is_end_time:
            g_time += 1
            refresh_status_bar()
            g_screen.ontimer(refresh_time, 1000)
        else:
            return


# display the frame of the game board
def display_frame():
    global g_intro

    # set up the screen frame
    screen_frame = turtle.Turtle()
    screen_frame.hideturtle()
    screen_frame.pensize(2)
    screen_frame.penup()
    screen_frame.goto(-250, -290)
    screen_frame.pendown()
    screen_frame.fd(500)
    screen_frame.left(90)
    screen_frame.fd(500)
    screen_frame.left(90)
    screen_frame.fd(500)
    screen_frame.left(90)
    screen_frame.fd(500)
    screen_frame.penup()
    screen_frame.goto(-250, 210)
    screen_frame.pendown()
    screen_frame.left(180)
    screen_frame.fd(80)
    screen_frame.right(90)
    screen_frame.fd(500)
    screen_frame.right(90)
    screen_frame.fd(80)

    # display the introduction
    g_intro = turtle.Turtle()
    g_intro.hideturtle()
    g_intro.penup()
    g_intro.goto(-110, 125)
    g_intro.write('Welcome to Snake!\n\nClick anywhere to start, have fun!', font=('Arial', 16, 'normal'))

    refresh_status_bar()
    g_screen.update()


# refresh and display the snake
def display_snake():
    # display the snake head
    snake_head.goto(-240 + head_current_location[0] * 20, -280 + head_current_location[1] * 20)
    # display the snake tail
    for each_block_location in snake_tail_position:
        snake_tail.goto(-240 + each_block_location[0] * 20, -280 + each_block_location[1] * 20)
        snake_tail.stamp()
    g_screen.update()


# refresh and display the food
def display_food():
    global food_1
    global food_2
    global food_3
    global food_4
    global food_5

    food_1 = turtle.Turtle()
    food_1.penup()
    food_1.hideturtle()
    food_1.goto(-243 + food_location_1[0] * 20, -290 + food_location_1[1] * 20)
    food_1.write('1', font=('Arial', 16, 'normal'))

    food_2 = turtle.Turtle()
    food_2.penup()
    food_2.hideturtle()
    food_2.goto(-243 + food_location_2[0] * 20, -290 + food_location_2[1] * 20)
    food_2.write('2', font=('Arial', 16, 'normal'))

    food_3 = turtle.Turtle()
    food_3.penup()
    food_3.hideturtle()
    food_3.goto(-243 + food_location_3[0] * 20, -290 + food_location_3[1] * 20)
    food_3.write('3', font=('Arial', 16, 'normal'))

    food_4 = turtle.Turtle()
    food_4.penup()
    food_4.hideturtle()
    food_4.goto(-243 + food_location_4[0] * 20, -290 + food_location_4[1] * 20)
    food_4.write('4', font=('Arial', 16, 'normal'))

    food_5 = turtle.Turtle()
    food_5.penup()
    food_5.hideturtle()
    food_5.goto(-243 + food_location_5[0] * 20, -290 + food_location_5[1] * 20)
    food_5.write('5', font=('Arial', 16, 'normal'))


# refresh and display the monster
def display_monster():
    monster.goto(-230 + monster_target_location[0] * 20, -270 + monster_target_location[1] * 20)
    g_screen.update()


# display that game is over on the top of monster
def display_game_over():
    game_over_reminder = turtle.Turtle()
    game_over_reminder.penup()
    game_over_reminder.hideturtle()
    game_over_reminder.pencolor('purple')
    game_over_reminder.goto(-260 + monster_current_location[0] * 20, -257 + monster_current_location[1] * 20)
    game_over_reminder.write('Game Over!', font=('Arial', 12, 'bold'))


# display that user wins the game on the top of snake
def display_game_win():
    game_win_reminder = turtle.Turtle()
    game_win_reminder.penup()
    game_win_reminder.hideturtle()
    game_win_reminder.pencolor('red')
    game_win_reminder.goto(-262 + head_current_location[0] * 20, -267 + head_current_location[1] * 20)
    game_win_reminder.write('Winner!', font=('Arial', 13, 'bold'))


# detect if food's positions contain overlapping
def is_food_valid(loc_1, loc_2, loc_3, loc_4, loc_5):
    loc_list = []
    for loc in [loc_1, loc_2, loc_3, loc_4, loc_5]:
        if loc not in loc_list:
            loc_list.append(loc)
    if len(loc_list) == 5 and [12, 12] not in loc_list:
        return True
    else:
        # if position overlaps, return False
        return False


# set the random position of food
def set_food():
    global food_location_1
    global food_location_2
    global food_location_3
    global food_location_4
    global food_location_5
    global show_food_pos_list
    global original_food_pos_1
    global original_food_pos_2
    global original_food_pos_3
    global original_food_pos_4
    global original_food_pos_5

    food_location_1 = [randrange(0, 25, 1), randrange(0, 25, 1)]
    food_location_2 = [randrange(0, 25, 1), randrange(0, 25, 1)]
    food_location_3 = [randrange(0, 25, 1), randrange(0, 25, 1)]
    food_location_4 = [randrange(0, 25, 1), randrange(0, 25, 1)]
    food_location_5 = [randrange(0, 25, 1), randrange(0, 25, 1)]

    # original position used to redisplay food
    original_food_pos_1 = [[], []]
    original_food_pos_2 = [[], []]
    original_food_pos_3 = [[], []]
    original_food_pos_4 = [[], []]
    original_food_pos_5 = [[], []]
    original_food_pos_1[0] = food_location_1[0]
    original_food_pos_1[1] = food_location_1[1]
    original_food_pos_2[0] = food_location_2[0]
    original_food_pos_2[1] = food_location_2[1]
    original_food_pos_3[0] = food_location_3[0]
    original_food_pos_3[1] = food_location_3[1]
    original_food_pos_4[0] = food_location_4[0]
    original_food_pos_4[1] = food_location_4[1]
    original_food_pos_5[0] = food_location_5[0]
    original_food_pos_5[1] = food_location_5[1]

    # set up the food position again if containing overlapping
    if not is_food_valid(food_location_1, food_location_2,
                         food_location_3, food_location_4, food_location_5):
        set_food()


# set the snake to go up
def set_snake_direction_up():
    global snake_motion
    snake_motion = 'Up'


# set the snake to go down
def set_snake_direction_down():
    global snake_motion
    snake_motion = 'Down'


# set the snake to go left
def set_snake_direction_left():
    global snake_motion
    snake_motion = 'Left'


# set the snake to go right
def set_snake_direction_right():
    global snake_motion
    snake_motion = 'Right'


# set the snake to pause and continue
def set_snake_paused():
    global snake_motion
    global former_snake_motion

    if snake_motion != 'Paused':
        former_snake_motion = snake_motion
        snake_motion = 'Paused'  # snake pauses
    else:
        snake_motion = former_snake_motion  # snake continues to go


# check if the next step of snake is movable, return False if not
def is_snake_movable(target_loc):
    # check if tail blocks the movement of head
    if target_loc not in snake_tail_position:
        # check if board frame blocks the movement of head
        if 0 <= target_loc[0] <= 24 and 0 <= target_loc[1] <= 24:
            return True
    else:
        return False


# let snake move at a certain time interval
def snake_move():
    global snake_motion
    global snake_speed
    global head_target_location
    global head_current_location
    global snake_tail_length
    global snake_tail_position
    tail_to_expand_position = [12, 12]

    if is_game_over():
        return  # stop moving if game over
    else:
        # when snake doesn't pause
        if snake_motion != 'Paused':
            # find the position snake head goes
            if snake_motion == 'Up':
                refresh_status_bar()
                head_target_location = [head_current_location[0], head_current_location[1] + 1]
            elif snake_motion == 'Down':
                refresh_status_bar()
                head_target_location = [head_current_location[0], head_current_location[1] - 1]
            elif snake_motion == 'Left':
                refresh_status_bar()
                head_target_location = [head_current_location[0] - 1, head_current_location[1]]
            elif snake_motion == 'Right':
                refresh_status_bar()
                head_target_location = [head_current_location[0] + 1, head_current_location[1]]

            # when snake can move to next position
            if is_snake_movable(head_target_location):
                # update the position of every block of snake tail
                if snake_tail_length > 0:
                    tail_to_expand_position = snake_tail_position[snake_tail_length - 1]
                    for verse_order in range(snake_tail_length):
                        if verse_order <= snake_tail_length - 1:
                            snake_tail_position[snake_tail_length - verse_order - 1] \
                                = snake_tail_position[snake_tail_length - verse_order - 2]
                    snake_tail_position[0] = head_current_location
                # update the current snake head position
                head_current_location = head_target_location

                # expand the snake tail if needed
                if snake_tail_expand_num != 0:
                    snake_expand(tail_to_expand_position)
                else:
                    snake_speed = 200

                # display the moved snake based on the position
                snake_tail.clearstamps()
                display_snake()
                eat_food()
                # move the snake again after a certain time interval
                g_screen.ontimer(snake_move, snake_speed)
            # when snake can't move to next position (blocked by frame/tail)
            else:
                g_screen.ontimer(snake_move, snake_speed)
        # when snake pauses
        else:
            refresh_status_bar()
            g_screen.ontimer(snake_move, snake_speed)


# expand the snake tail
def snake_expand(to_expand_pos):
    global snake_tail_length
    global snake_tail_expand_num
    global snake_tail_position
    global snake_speed

    snake_speed = 400  # snake slows down when expanding the tail
    snake_tail_position.append(to_expand_pos)
    snake_tail_length += 1
    snake_tail_expand_num -= 1


# check if the next step of monster is movable, return False if not
def is_monster_movable(target_loc):
    # check if board frame blocks the movement of monster
    if 0 <= target_loc[0] <= 23 and 0 <= target_loc[1] <= 23:
        return True
    else:
        return False


# let monster's speed randomly change
def set_monster_speed():
    global monster_speed
    # monster randomly changes its speed every 3 seconds
    monster_speed = randrange(450, 600, 5)
    g_screen.ontimer(set_monster_speed, 3000)


# let snake move at a certain time interval
def monster_move():
    global monster_speed
    global monster_current_location
    global monster_target_location

    if is_game_over():
        return  # monster stops when game over

    else:
        delta_x = head_current_location[0] - monster_current_location[0]  # the difference of row order
        delta_y = head_current_location[1] - monster_current_location[1]  # the difference of column order
        # set monster's next step by chasing snake head
        if delta_y >= delta_x and delta_y >= -delta_x and delta_y >= 0:
            monster_target_location = [monster_current_location[0], monster_current_location[1] + 1]
        elif delta_y <= delta_x and delta_y <= -delta_x and delta_y <= 0:
            monster_target_location = [monster_current_location[0], monster_current_location[1] - 1]
        elif -delta_x <= delta_y <= delta_x and delta_x >= 0:
            monster_target_location = [monster_current_location[0] + 1, monster_current_location[1]]
        elif delta_x <= delta_y <= -delta_x and delta_x <= 0:
            monster_target_location = [monster_current_location[0] - 1, monster_current_location[1]]

        # check if next step is movable and move the monster
        if is_monster_movable(monster_target_location):
            monster_current_location = monster_target_location
            check_contact()
            display_monster()
            # move the monster again after a certain time interval
            g_screen.ontimer(monster_move, monster_speed)
        else:
            monster_target_location = monster_current_location
            check_contact()
            g_screen.ontimer(monster_move, monster_speed)


# check if snake eats food, and remove the eaten ones
def eat_food():
    global snake_tail_expand_num

    if food_location_1 == head_current_location:
        food_1.clear()
        food_location_1[0] = -1  # move the eaten food out of the game board
        food_location_1[1] = -1
        valid_food_list.remove(1)
        snake_tail_expand_num += 1
    if food_location_2 == head_current_location:
        food_2.clear()
        food_location_2[0] = -1
        food_location_2[1] = -1
        valid_food_list.remove(2)
        snake_tail_expand_num += 2
    if food_location_3 == head_current_location:
        food_3.clear()
        food_location_3[0] = -1
        food_location_3[1] = -1
        valid_food_list.remove(3)
        snake_tail_expand_num += 3
    if food_location_4 == head_current_location:
        food_4.clear()
        food_location_4[0] = -1
        food_location_4[1] = -1
        valid_food_list.remove(4)
        snake_tail_expand_num += 4
    if food_location_5 == head_current_location:
        food_5.clear()
        food_location_5[0] = -1
        food_location_5[1] = -1
        valid_food_list.remove(5)
        snake_tail_expand_num += 5


# randomly hide the uneaten food
def hide_food():
    global valid_food_list
    global hide_food_list
    global only_count

    # used to hide and remove the food from the board
    def hide_food_1():
        global original_food_pos_1
        original_food_pos_1[0] = food_location_1[0]
        original_food_pos_1[1] = food_location_1[1]
        food_1.clear()
        food_location_1[0] = -1
        food_location_1[1] = -1

    def hide_food_2():
        global original_food_pos_2
        original_food_pos_2[0] = food_location_2[0]
        original_food_pos_2[1] = food_location_2[1]
        food_2.clear()
        food_location_2[0] = -1
        food_location_2[1] = -1

    def hide_food_3():
        global original_food_pos_3
        original_food_pos_3[0] = food_location_3[0]
        original_food_pos_3[1] = food_location_3[1]
        food_3.clear()
        food_location_3[0] = -1
        food_location_3[1] = -1

    def hide_food_4():
        global original_food_pos_4
        original_food_pos_4[0] = food_location_4[0]
        original_food_pos_4[1] = food_location_4[1]
        food_4.clear()
        food_location_4[0] = -1
        food_location_4[1] = -1

    def hide_food_5():
        original_food_pos_5[0] = food_location_5[0]
        original_food_pos_5[1] = food_location_5[1]
        food_5.clear()
        food_location_5[0] = -1
        food_location_5[1] = -1

    # show the former hidden food and replace it at original position
    def show_food_1():
        global original_food_pos_1
        food_location_1[0] = original_food_pos_1[0]
        food_location_1[1] = original_food_pos_1[1]
        food_1.goto(-243 + food_location_1[0] * 20, -290 + food_location_1[1] * 20)
        food_1.write('1', font=('Arial', 16, 'normal'))

    def show_food_2():
        global original_food_pos_2
        food_location_2[0] = original_food_pos_2[0]
        food_location_2[1] = original_food_pos_2[1]
        food_2.goto(-243 + food_location_2[0] * 20, -290 + food_location_2[1] * 20)
        food_2.write('2', font=('Arial', 16, 'normal'))

    def show_food_3():
        global original_food_pos_3
        food_location_3[0] = original_food_pos_3[0]
        food_location_3[1] = original_food_pos_3[1]
        food_3.goto(-243 + food_location_3[0] * 20, -290 + food_location_3[1] * 20)
        food_3.write('3', font=('Arial', 16, 'normal'))

    def show_food_4():
        global original_food_pos_4
        food_location_4[0] = original_food_pos_4[0]
        food_location_4[1] = original_food_pos_4[1]
        food_4.goto(-243 + food_location_4[0] * 20, -290 + food_location_4[1] * 20)
        food_4.write('4', font=('Arial', 16, 'normal'))

    def show_food_5():
        global original_food_pos_5
        food_location_5[0] = original_food_pos_5[0]
        food_location_5[1] = original_food_pos_5[1]
        food_5.goto(-243 + food_location_5[0] * 20, -290 + food_location_5[1] * 20)
        food_5.write('5', font=('Arial', 16, 'normal'))

    if not is_end_time:
        former_hide_food_list = hide_food_list
        hide_food_list = []

        # randomly choose the food to hide
        valid_food_length = len(valid_food_list)
        if valid_food_length != 1 and valid_food_length != 0:
            hide_num = 1
        elif valid_food_length == 1 and only_count < 1:
            only_count += 1
            hide_num = randint(0, 1)
        else:
            hide_num = 0
        if is_start_time:
            hide_num = 0  # do not hide food at the first 5 seconds
        hide_food_list = random.sample(valid_food_list, hide_num)

        # show the hidden food
        if 1 in former_hide_food_list:  # condition: hidden at last round
            if 1 not in hide_food_list:  # condition: not hidden at this round
                show_food_1()
        if 2 in former_hide_food_list:
            if 2 not in hide_food_list:
                show_food_2()
        if 3 in former_hide_food_list:
            if 3 not in hide_food_list:
                show_food_3()
        if 4 in former_hide_food_list:
            if 4 not in hide_food_list:
                show_food_4()
        if 5 in former_hide_food_list:
            if 5 not in hide_food_list:
                show_food_5()
        # hide the unhidden food
        if 1 in hide_food_list:  # condition: hidden at this round
            if 1 not in former_hide_food_list:  # condition: not hidden at last round
                hide_food_1()
        if 2 in hide_food_list:
            if 2 not in former_hide_food_list:
                hide_food_2()
        if 3 in hide_food_list:
            if 3 not in former_hide_food_list:
                hide_food_3()
        if 4 in hide_food_list:
            if 4 not in former_hide_food_list:
                hide_food_4()
        if 5 in hide_food_list:
            if 5 not in former_hide_food_list:
                hide_food_5()

        # randomly pick and hide food every 5 seconds
        g_screen.ontimer(hide_food, 5000)


# check if snake head crush monster, or snake eats all food, and end the game
def is_game_over():
    global is_end_time
    # check if head and monster crush
    if -1 <= monster_current_location[0] - head_current_location[0] <= 0:
        if -1 <= monster_current_location[1] - head_current_location[1] <= 0:
            display_game_over()
            is_end_time = True
            return True
        else:
            return False
    # check if snake eats all the food
    elif snake_tail_length == 20:
        display_game_win()
        is_end_time = True
        return True
    else:
        return False


# detect if monster contacts snake
def check_contact():
    global g_contact
    for each_block in snake_tail_position:
        if -1 <= monster_current_location[0] - each_block[0] <= 0:
            if -1 <= monster_current_location[1] - each_block[1] <= 0:
                g_contact += 1
                refresh_status_bar()
                return


# start the game if click detected
def start_game(x, y):
    global g_intro
    global g_time
    g_intro.clear()
    g_screen.onclick(None)

    display_food()  # set up the food
    hide_food()
    refresh_time()  # set up the timer
    snake_move()  # move the snake
    set_monster_speed()  # set up the monster
    monster_move()  # move the monster
    return x, y


# main execution function of the game
def main():
    display_frame()
    display_snake()
    display_monster()
    set_food()
    g_screen.onkey(set_snake_direction_up, 'Up')
    g_screen.onkey(set_snake_direction_down, 'Down')
    g_screen.onkey(set_snake_direction_left, 'Left')
    g_screen.onkey(set_snake_direction_right, 'Right')
    g_screen.onkey(set_snake_paused, 'space')
    g_screen.onclick(start_game)


if __name__ == '__main__':
    main()
    g_screen.listen()
    g_screen.mainloop()
