from constants import *
import tkinter
import random


class Snake:
    """Snake in the snake game.

    Attributes:
        acceleration: an integer indicating the speed bonus the snake has from eating food.
        body_parts: tkinter rectangles list representing body parts of the snake.
        coordinates: list of two coordinates of the lower left corner of each body part.
    """

    def __init__(self):
        """Initializes the snake of length INITIAL_SNAKE_LENGTH.

        Creates INITIAL_SNAKE_LENGTH tkinter rectangles that are body parts of the snake.
        """

        self.acceleration = 0
        self.coordinates = []
        self.body_parts = []
        for i in range(INITIAL_SNAKE_LENGTH):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = main_canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.body_parts.append(square)


class Food:
    """Food in the snake game.

    Attributes:
        acceleration: an integer indicating the acceleration the snake has after eating this food.
        coordinates: list of two coordinates of the lower left corner of the cell in which tkinter oval
          representing the food is located.
    """

    objects_created = 0

    def __init__(self, level_number):
        """Initializes the food based on the current level of the game.

        Firstly finds the coordinates that are suitable for placing food (meaning they
        are free of obstacles and snake body parts). Then chooses the color and the acceleration
        of the food based on level_number. If level_number is 5 then additionally finds the coordinates
        where an obstacle can be placed.

        Args:
          level_number: an integer indicating the current level of the game.
        """

        position_allowed = False
        x = 0
        y = 0
        while not position_allowed:
            x = random.randint(0, CANVAS_WIDTH // CELL_SIZE - 1) * CELL_SIZE
            y = random.randint(0, CANVAS_HEIGHT // CELL_SIZE - 2) * CELL_SIZE
            position_allowed = True
            for body_part_coordinates in main_snake.coordinates:
                if x == body_part_coordinates[0] and y == body_part_coordinates[1]:
                    position_allowed = False
                    break
            for obstacle in main_obstacle_list:
                if x == obstacle[0] and y == obstacle[1]:
                    position_allowed = False
                    break
        self.acceleration = 0
        food_color = DEFAULT_FOOD_COLOR
        if level_number == 2:
            self.acceleration = random.randint(-1, 1)
            self.acceleration *= 2
            if self.acceleration == -2:
                food_color = SLOW_FOOD_COLOR
            elif self.acceleration == 2:
                food_color = FAST_FOOD_COLOR
        if level_number == 3:
            if Food.objects_created % 2 == 0:
                self.acceleration = 6
                food_color = VERY_FAST_FOOD_COLOR
            else:
                self.acceleration = -6
                food_color = VERY_SLOW_FOOD_COLOR
        if level_number == 5:
            main_obstacle_list.append([x, y])
            main_canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=OBSTACLE_COLOR, tags="obstacle")
            position_allowed = False
            while not position_allowed:
                x = random.randint(1, CANVAS_WIDTH // CELL_SIZE - 1) * CELL_SIZE
                y = random.randint(0, CANVAS_HEIGHT // CELL_SIZE - 2) * CELL_SIZE
                position_allowed = True
                for body_part_coordinates in main_snake.coordinates:
                    if x == body_part_coordinates[0] and y == body_part_coordinates[1]:
                        position_allowed = False
                        break
                for obstacle in main_obstacle_list:
                    if x == obstacle[0] and y == obstacle[1]:
                        position_allowed = False
                        break
        self.coordinates = [x, y]
        main_canvas.create_oval(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=food_color, tags="food")
        Food.objects_created += 1


def do_next_move(snake, food, level_number):
    """Does the next move in the snake game.

    Creates new tkinter rectangle based on the direction of the snake. Deletes the tail
    of the snake if the food was eaten. If it was then updates the score, the acceleration of
    the snake and creates new food object. After this checks for collisions and depending on the result
    either continues the game or shows the "Game over!" screen.

    Args:
      snake: current snake object in the game.
      food: current food object in the game.
      level_number: an integer indicating the current level of the game.
    """

    x, y = snake.coordinates[0]
    if main_direction == "right":
        x += CELL_SIZE
    elif main_direction == "left":
        x -= CELL_SIZE
    elif main_direction == "down":
        y += CELL_SIZE
    elif main_direction == "up":
        y -= CELL_SIZE
    snake.coordinates.insert(0, [x, y])
    head_square = main_canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=SNAKE_COLOR)
    snake.body_parts.insert(0, head_square)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global main_score
        main_score += 1
        global main_level_records
        if main_score > main_level_records[level_number - 1]:
            main_level_records[level_number - 1] = main_score
        main_label.config(
            text=f"Max level {level_number} score: {main_level_records[level_number - 1]},  Score: {main_score}")
        snake.acceleration = food.acceleration
        main_canvas.delete("food")
        food = Food(level_number)
    else:
        main_canvas.delete(snake.body_parts[-1])
        del snake.body_parts[-1]
        del snake.coordinates[-1]
    if check_for_collisions(snake):
        show_game_over_screen()
    else:
        main_window.after(GAME_SPEED - (len(snake.coordinates) - INITIAL_SNAKE_LENGTH + snake.acceleration) * ACCELERATION,
                     do_next_move,
                     snake, food, level_number)


def change_main_direction(new_direction):
    """Changes the direction of the snake to new_direction."""

    global main_direction
    if new_direction == 'down':
        if main_direction != 'up':
            main_direction = new_direction
    elif new_direction == 'up':
        if main_direction != 'down':
            main_direction = new_direction
    elif new_direction == 'left':
        if main_direction != 'right':
            main_direction = new_direction
    elif new_direction == 'right':
        if main_direction != 'left':
            main_direction = new_direction


def check_for_collisions(snake):
    """Checks the snake's head for collisions.

    Returns:
      True if the snake's head bumps into the edges of the canvas OR into an obstacle OR
      into the snake's other body part, False otherwise.
    """

    x, y = snake.coordinates[0]
    if x >= CANVAS_WIDTH or x < 0:
        return True
    elif y >= CANVAS_HEIGHT or y < 0:
        return True
    for body_part_coordinates in snake.coordinates[1:]:
        if x == body_part_coordinates[0] and y == body_part_coordinates[1]:
            return True
    for obstacle in main_obstacle_list:
        if x == obstacle[0] and y == obstacle[1]:
            return True
    return False


def show_game_over_screen():
    """Shows the "Game over!" screen.

    Changes the state of the game to inactive. Shows text with instructions on how to continue the game.
    """

    main_canvas.delete(tkinter.ALL)
    main_canvas.create_text(main_canvas.winfo_width() / 2, CELL_SIZE * 2, fill=TEXT_COLOR, font=('consolas', 50),
                       tags="gameover", text="Game over!", width=CANVAS_WIDTH)
    main_canvas.create_text(main_canvas.winfo_width() / 2, CELL_SIZE * (LEVEL_COUNT + 2), fill=TEXT_COLOR, font=('consolas', 30),
                       justify="center", tags="playguide",
                       text="Press key '1'-'5' to start the\ncorresponding level\nOR\nPress key 's' to show level records", width=CANVAS_WIDTH)
    global main_game_active
    main_game_active = False


def run_game(level_number):
    """Starts the game.

    Defaults all objects and parameters in the game based on level_number.

    Args:
      level_number: an integer indicating the current level of the game.
    """

    global main_game_active
    if main_game_active:
        return
    main_canvas.delete(tkinter.ALL)
    global main_obstacle_list
    global main_score
    global main_direction
    global main_snake
    global main_food
    main_obstacle_list = []
    if level_number == 4 or level_number == 5:
        obstacle_count = INITIAL_OBSTACLE_COUNT
        if level_number == 5:
            obstacle_count //= 2
        for i in range(obstacle_count):
            x = random.randint(1, CANVAS_WIDTH // CELL_SIZE - 1) * CELL_SIZE
            y = random.randint(0, CANVAS_HEIGHT // CELL_SIZE - 1) * CELL_SIZE
            main_obstacle_list.append([x, y])
            main_canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=OBSTACLE_COLOR, tags="obstacle")
    main_score = 0
    main_direction = 'down'
    main_snake = Snake()
    main_food = Food(level_number)
    main_game_active = True
    main_label.config(text=f"Max level {level_number} score: {main_level_records[level_number - 1]},  Score: {main_score}")
    do_next_move(main_snake, main_food, level_number)


def show_records():
    """Shows the table of level records.

    Additionally, shows text with instructions on how to continue the game.
    """

    if main_game_active:
        return
    main_canvas.delete(tkinter.ALL)
    main_label.config(text="Level Records")
    for i in range(LEVEL_COUNT):
        main_canvas.create_text(main_canvas.winfo_width() / 2, CELL_SIZE * (i + 1), fill=TEXT_COLOR, font=('consolas', 30),
                           tags="records", text=f"Level {i + 1} record: {main_level_records[i]}", width=CANVAS_WIDTH)
    main_canvas.create_text(main_canvas.winfo_width() / 2, CELL_SIZE * (LEVEL_COUNT + 3), fill=TEXT_COLOR, font=('consolas', 30),
                       justify="center", tags="playguide", text="Press key '1'-'5' to start the\ncorresponding level", width=CANVAS_WIDTH)


main_window = tkinter.Tk()
main_window.title("Snake Game")
main_window.resizable(False, False)

main_score = 0
main_direction = 'down'
main_game_active = False
main_obstacle_list = []
main_level_records = [0, 0, 0, 0, 0]

main_label = tkinter.Label(main_window, font=('consolas', 30), justify="center", wraplength=CANVAS_WIDTH)
main_label.pack()

main_canvas = tkinter.Canvas(main_window, bg=BACKGROUND_COLOR, height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
main_canvas.pack()

main_window.update()

main_canvas.create_text(main_canvas.winfo_width() / 2, CELL_SIZE * (LEVEL_COUNT + 2), font=('consolas', 30),
                   text="Press key '1'-'5' to start the\ncorresponding level\nOR\nPress key 's' to show level records",
                   fill=TEXT_COLOR, tags="playguide",
                   justify="center", width=CANVAS_WIDTH)

window_width = main_window.winfo_width()
window_height = main_window.winfo_height()
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

x_geometry = int((screen_width - window_width) / 2)
y_geometry = int((screen_height - window_height) / 2)
main_window.geometry(f"{window_width}x{window_height}+{x_geometry}+{y_geometry}")

main_window.bind('1', lambda event: run_game(1))
main_window.bind('2', lambda event: run_game(2))
main_window.bind('3', lambda event: run_game(3))
main_window.bind('4', lambda event: run_game(4))
main_window.bind('5', lambda event: run_game(5))
main_window.bind('s', lambda event: show_records())
main_window.bind('<Down>', lambda event: change_main_direction('down'))
main_window.bind('<Up>', lambda event: change_main_direction('up'))
main_window.bind('<Left>', lambda event: change_main_direction('left'))
main_window.bind('<Right>', lambda event: change_main_direction('right'))

main_snake = None
main_food = None

main_window.mainloop()

