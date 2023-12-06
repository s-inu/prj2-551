import os
import csv
import pickle
import random
import inspect
import textwrap
from types import NoneType
from typing import List, Tuple

from Captain import Captain
from Creature import Creature
from FieldInhabitant import FieldInhabitant
from Rabbit import Rabbit
from Snake import Snake
from Veggie import Veggie


class GameEngine:
    # Game configuration constants
    __NUMBEROFVEGGIES = 30  # Total number of vegetables in the game
    __NUMBEROFRABBITS = 5  # Total number of rabbits in the game
    __HIGHSCOREFILE = "highscore.data"  # File name for saving high scores

    def __init__(self) -> None:
        # Initialize game state
        self.__field: List[
            List[FieldInhabitant]
        ] = []  # The game field, a 2D grid of FieldInhabitants
        self.__rabbits: List[Rabbit] = []  # List to store all rabbit objects
        self.__veggies_possible: List[Veggie] = []  # List of possible vegetable types
        self.__captain: Captain = None  # The player's character
        self.__snake: Snake = None  # The snake character
        self.__score: int = 0  # Player's current score

    def __clear_creature(self, creature: Creature) -> None:
        # Clear a creature from the field
        x = creature.get_x()  # Get creature's x-coordinate
        y = creature.get_y()  # Get creature's y-coordinate
        self.__field[y][x] = None  # Remove the creature from its position

    def init_veggies_possible(self) -> None:
        # Initialize the list of possible vegetables
        self.__veggies_possible = []  # Reset the list to empty

    def initVeggies(self) -> None:
        # Initialize the vegetables on the field by reading their data from a file

        # Prompt the user for the vegetable data file name
        veggie_filename = input("Please enter the name of the vegetable point file: ")

        # Check if the file exists; prompt again if it doesn't
        while not os.path.isfile(veggie_filename):
            veggie_filename = input(
                f"{veggie_filename} does not exist! Please enter the name of the vegetable point file: "
            )

        # Open and read the vegetable data file
        with open(veggie_filename, "r") as fo:
            data = [*csv.reader(fo)]  # Read the CSV data into a list

        # Extract and remove the dimension data from the first line of the file
        _, dim1, dim2 = data.pop(0)

        # Initialize the game field with the extracted dimensions
        self.field_init(int(dim1), int(dim2))

        # Prepare the list for possible vegetables
        self.init_veggies_possible()

        # Process each vegetable type from the file and add it to possible vegetables
        for name, symbol, points in data:
            self.add_veggie_possible(name, symbol, int(points))

        # Place the specified number of vegetables randomly on the field
        for _ in range(self.__NUMBEROFVEGGIES):
            x, y = self.find_space()  # Find a random empty space on the field
            # Place a randomly chosen vegetable at the found location
            self.__field[y][x] = random.choice(self.__veggies_possible)

    def initCaptain(self) -> None:
        # Initialize the Captain (player character) on the game field

        # Clear the current Captain from the field if it exists
        if (captain := self.__captain) is not None:
            self.__clear_creature(captain)

        # Find a random empty space and place the Captain there
        x, y = self.find_space()
        self.__field[y][x] = self.__captain = Captain(x, y)

    def initRabbits(self) -> None:
        # Initialize rabbits on the game field

        # Clear existing rabbits from the field
        if (rabbits := self.__rabbits) is not None:
            for rabbit in rabbits:
                self.__clear_creature(rabbit)
            self.__rabbits.clear()  # Empty the list of rabbits

        # Place a set number of rabbits at random positions on the field
        for _ in range(self.__NUMBEROFRABBITS):
            x, y = self.find_space()  # Find a random empty space for each rabbit
            rabbit = Rabbit(x, y)  # Create a new Rabbit instance
            self.__field[y][x] = rabbit  # Place the rabbit on the field
            self.__rabbits.append(rabbit)  # Add the rabbit to the list

    def initSnake(self) -> None:
        # Initialize the snake on the game field

        # Clear the current snake from the field if it exists
        if (snake := self.__snake) is not None:
            self.__clear_creature(snake)

        # Find a random empty space and place the snake there
        x, y = self.find_space()
        self.__field[y][x] = self.__snake = Snake(x, y)

    def initializeGame(self) -> None:
        # Initialize the entire game by setting up all game elements

        self.initVeggies()  # Initialize vegetables on the field
        self.initCaptain()  # Place the Captain on the field
        self.initRabbits()  # Place rabbits on the field
        self.initSnake()  # Place the snake on the field

    def remainingVeggies(self) -> int:
        # Calculate the number of remaining vegetables on the field

        # Count and return the number of Veggie objects currently on the field
        return sum(isinstance(slot, Veggie) for row in self.__field for slot in row)

    def intro(self) -> None:
        # Display the introductory text of the game

        # Welcome message
        print("Welcome to Captain Veggie!")

        # Game description and instructions
        print(
            textwrap.fill(
                "The rabbits have invaded your garden and you must harvest as many vegetables as possible before the rabbits eat them all! Each vegetable is worth a different number of points so go for the high score!",
                width=58,
            )
        )

        # Display information about the vegetables in the game
        print("\nThe vegetables are:")
        for veggie in self.__veggies_possible:
            symbol = (
                veggie.get_inhabitant()
            )  # Get the symbol representing the vegetable
            name = veggie.get_name()  # Get the vegetable's name
            points = veggie.get_points()  # Get the points value of the vegetable
            print(f"{symbol}: {name} {points}")

        # Information about the player character and the rabbits
        print("\nCaptain Veggie is V, and the rabbits are R's.")

        # Good luck message
        print("\nGood Luck!")

    def printField(self) -> None:
        # Print the current state of the game field

        # Calculate the width of the field for printing
        cols = len(self.__field[0])
        print("#" * (3 * cols + 2))  # Print the top border

        # Print each row of the field
        for row in self.__field:
            symbols = (
                inhabitant.get_inhabitant() if inhabitant is not None else " "
                for inhabitant in row
            )  # Get the symbol for each field inhabitant
            print(f'# {"  ".join(symbols)} #')  # Print the row with symbols

        print("#" * (3 * cols + 2))  # Print the bottom border

    def getScore(self) -> int:
        # Retrieve the current score of the game
        return self.__score  # Return the private attribute holding the game's score

    def moveRabbits(self) -> None:
        # Move each rabbit on the field randomly

        # Define all possible movement options for the rabbits
        moves = [
            (0, 0),  # no move
            (0, -1),  # up
            (0, 1),  # down
            (-1, 0),  # left
            (1, 0),  # right
            (-1, -1),  # up-left
            (1, -1),  # up-right
            (-1, 1),  # down-left
            (1, 1),  # down-right
        ]

        # Move each rabbit in a random direction
        for rabbit in self.__rabbits:
            # Choose a random move from the list and apply it to the rabbit
            self.move_creature(rabbit, *random.choice(moves))

            # action = random.randint(0, 8)
            # if action == 0:
            #     continue
            # elif action == 1:
            #     self.moveCreature(rabbit, 1, 0)
            # elif action == 2:
            #     self.moveCreature(rabbit, -1, 0)
            # elif action == 3:
            #     self.moveCreature(rabbit, 0, 1)
            # elif action == 4:
            #     self.moveCreature(rabbit, 0, -1)
            # elif action == 5:
            #     self.moveCreature(rabbit, 1, 1)
            # elif action == 6:
            #     self.moveCreature(rabbit, -1, 1)
            # elif action == 7:
            #     self.moveCreature(rabbit, 1, -1)
            # elif action == 8:
            #     self.moveCreature(rabbit, -1, -1)

    def moveCptVertical(self, step: int) -> Tuple[FieldInhabitant, bool]:
        return self.move_creature(self.__captain, 0, step)

        # res = self.move_creature(self.__captain, 0, step)
        # if res is not None:
        #     if isinstance(res, Veggie):
        #         print("Yummy! A delicious " + res.get_name())
        #         self.__veggies_collected.append(res)
        #         self.__score += res.get_points()
        #     elif isinstance(res, Rabbit):
        #         print("Don't step on the bunnies!")
        #     else:
        #         print("You can't move that way!")

    def moveCptHorizontal(self, step: int) -> Tuple[FieldInhabitant, bool]:
        return self.move_creature(self.__captain, step, 0)

        # res = self.move_creature(self.__captain, step, 0)
        # if res is not None:
        #     if isinstance(res, Veggie):
        #         print("Yummy! A delicious " + res.get_name())
        #         self.__veggies_collected.append(res)
        #         self.__score += res.get_points()
        #     elif isinstance(res, Rabbit):
        #         print("Don't step on the bunnies!")
        #     else:
        #         print("You can't move that way!")

    def moveCaptain(self) -> None:
        # Move the Captain based on user input

        # Ask the player for the direction to move the Captain
        direction = input(
            "Would you like to move up(W), down(S), left(A), or right(D): "
        ).lower()

        # Mapping of input directions to corresponding movement functions
        direction_map = {
            "w": lambda: self.moveCptVertical(-1),  # Up
            "s": lambda: self.moveCptVertical(1),  # Down
            "a": lambda: self.moveCptHorizontal(-1),  # Left
            "d": lambda: self.moveCptHorizontal(1),  # Right
        }

        # Retrieve the movement function based on the user's input
        valid_option = direction_map.get(direction)
        if valid_option is None:
            print(
                f"{direction} is not a valid option"
            )  # Inform if the direction is invalid
            return

        # Execute the movement and get information about any encounter
        encountered, ok = valid_option()
        if not ok:
            # Handle cases where movement is not successful
            if isinstance(encountered, Rabbit):
                print("Don't step on the bunnies!")  # Warn if a rabbit is encountered
            elif encountered is None:
                print("You can't move that way")  # Inform if movement is blocked
            else:
                print(
                    f"You're running into {encountered.__class__.__name__}"
                )  # General case for other encounters

        # Handle successful movement, especially when encountering a vegetable
        if ok:
            if isinstance(encountered, Veggie):
                print(
                    f"Yummy! A delicious {encountered.get_name()}"
                )  # Celebrate encountering a vegetable
            elif isinstance(encountered, Snake):
                print("Attacked by snake.")

        # if direction == "w":
        #     self.moveCptVertical(-1)
        # elif direction == "s":
        #     self.moveCptVertical(1)
        # elif direction == "a":
        #     self.moveCptHorizontal(-1)
        # elif direction == "d":
        #     self.moveCptHorizontal(1)
        # else:
        #     print(direction + " is not a valid option")

    def moveSnake(self) -> None:
        # Move the snake towards the Captain

        # Calculate the distance between the snake and the Captain in both x and y directions
        distance_x = self.__captain.get_x() - self.__snake.get_x()
        distance_y = self.__captain.get_y() - self.__snake.get_y()

        # Determine the movement direction based on the distance
        mx = (
            0 if distance_x == 0 else 1 if distance_x > 0 else -1
        )  # Horizontal movement direction
        my = (
            0 if distance_y == 0 else 1 if distance_y > 0 else -1
        )  # Vertical movement direction

        # If diagonal movement is needed, choose between horizontal and vertical movement randomly
        if mx * my != 0:
            mx, my = random.choice([(mx, 0), (0, my)])

        # Move the snake and check if it encounters anything
        encountered, ok = self.move_creature(self.__snake, mx, my)

        # If the snake encounters the Captain, trigger an attack
        if not ok and isinstance(encountered, Captain):
            print("Attacked by Snake.")

    def gameOver(self) -> None:
        # Handle the game over scenario

        # Print game over message
        print("GAME OVER!")

        # List all the vegetables harvested by the Captain
        print("You managed to harvest the following vegetables:")
        for veggie in self.__captain.get_veggies():
            print(veggie.get_name())  # Print each vegetable's name

        # Display the final score
        print(f"Your score was: {self.getScore()}")

    def highScore(self) -> None:
        # Handle the high score recording and display

        # Initialize a list to hold high scores
        high_scores = []

        # Load high scores from file if it exists
        if os.path.isfile(self.__HIGHSCOREFILE):
            with open(self.__HIGHSCOREFILE, "rb") as file:
                # Extend the high scores list with the scores loaded from the file
                high_scores.extend(pickle.load(file))

        # Prompt the player for their initials
        new_name = input("Please enter your three initials to go on the scoreboard: ")
        new_name = new_name[
            :3
        ].upper()  # Truncate or pad the name to 3 characters and make it uppercase

        # Add the player's current score to the high scores list
        high_scores.append((new_name, self.getScore()))

        # Sort the high scores in descending order
        high_scores.sort(key=lambda x: x[1], reverse=True)

        # for score in scorelist:
        #     scores.append(score)

        # scores = []
        # if os.path.isfile(self.__HIGHSCOREFILE):
        #     with open(self.__HIGHSCOREFILE, "rb") as file:
        #         scorelist = pickle.load(file)
        #         scores=[*scorelist]
        #         # for score in scorelist:
        #         #     scores.append(score)
        # index = 0
        # for pair in scores:
        #     name, score = pair
        #     if score < self.getScore():
        #         break
        #     index += 1
        # scores.insert(index, (new_name[0 : min(len(new_name), 3)], self.getScore()))

        # Display the high scores
        print("HIGH SCORES")
        print(f'{"Name":<10}{"Score":<10}')  # Print the header
        for name, score in high_scores:
            # Print each high score entry
            print(f"{name:<10}{score:<10}")

    def field_init(self, dim1: int, dim2: int) -> None:
        self.__field = [[None for _ in range(dim2)] for _ in range(dim1)]

    def add_veggie_possible(self, name: str, symbol: str, points: int) -> None:
        self.__veggies_possible.append(Veggie(symbol, name, points))

    def find_space(self) -> Tuple[int, int]:
        # Find an empty space on the game field

        # Determine the dimensions of the field
        row_len = len(self.__field)
        col_len = len(self.__field[0])
        # Set a limit on the number of attempts to find an empty space
        max_attempt = int(row_len * col_len / 2)

        # Try to find an empty space randomly
        x = random.randrange(col_len)
        y = random.randrange(row_len)
        # Continue searching until an empty space is found or attempts run out
        while max_attempt > 0 and self.__field[y][x] is not None:
            x = random.randrange(col_len)
            y = random.randrange(row_len)
            max_attempt -= 1

        # If no empty space is found within the attempt limit,
        # select an empty space from the remaining empty spaces
        if max_attempt == 0:
            spaces = (
                (x, y)
                for y in range(row_len)
                for x in range(col_len)
                if self.__field[y][x] is None
            )
            x, y = random.choice(
                list(spaces)
            )  # Choose randomly from the list of empty spaces

        return x, y  # Return the coordinates of the found empty space

    def move_creature(
        self, creature: Creature, mx: int, my: int
    ) -> Tuple[FieldInhabitant, bool]:
        # Move a creature by a specified amount on the field

        # Return immediately if no movement is specified
        if mx == 0 and my == 0:
            return creature, True  # No movement, so the creature stays in place

        # Get the current position of the creature
        x_original = creature.get_x()
        y_original = creature.get_y()

        # Calculate the new position based on the movement
        x_new = x_original + mx
        y_new = y_original + my

        # Get the dimensions of the field for boundary checking
        row_len = len(self.__field)
        col_len = len(self.__field[0])

        # Check if the new position is within the field boundaries
        if not (0 <= y_new < row_len) or not (0 <= x_new < col_len):
            return None, False  # Movement is out of bounds

        # Check for encounters at the new position
        encountered, ok = self.on_encounter(creature, x_new, y_new)
        if ok:
            # If movement is successful, update the creature's position on the field
            self.__field[y_original][x_original] = None  # Clear the original position
            self.__field[y_new][
                x_new
            ] = creature  # Place the creature at the new position
            creature.set_x(x_new)  # Update the creature's x-coordinate
            creature.set_y(y_new)  # Update the creature's y-coordinate

        # Return the object encountered and whether the move was successful
        return encountered, ok

        # if x < 0 or x > len(self.__field[0]) - 1 or y < 0 or y > len(self.__field) - 1:
        #     return "Wall"
        # else:
        #     if self.__field[y_new][x_new] is None:
        #         creature.set_x(x_new)
        #         creature.set_y(y_new)
        #         self.__field[y_new][x_new] = creature
        #         self.__field[y_new - my][x_new - mx] = None
        #     elif isinstance(self.__field[y_new][x_new], Veggie):
        #         tempVeggie = self.__field[y_new][x_new]
        #         creature.set_x(x_new)
        #         creature.set_y(y_new)
        #         self.__field[y_new][x_new] = creature
        #         self.__field[y_new - my][x_new - mx] = None
        #         return tempVeggie
        #     elif isinstance(self.__field[y_new][x_new], Rabbit):
        #         return self.__field[y_new][x_new]
        # return None

    def on_encounter(
        self,
        subject: Creature,
        object_x: int,
        object_y: int,
    ) -> Tuple[FieldInhabitant, bool]:
        # Handle the encounter between a moving creature and another object on the field

        # Get the dimensions of the field for boundary checking
        row_len = len(self.__field)
        col_len = len(self.__field[0])

        # Check if the coordinates are within the field boundaries
        if not (0 <= object_y < row_len) or not (0 <= object_x < col_len):
            return None, False  # Return False if the coordinates are out of bounds

        # Retrieve the object at the given coordinates
        obj = self.__field[object_y][object_x]

        # Return True if the subject encounters itself (e.g., didn't move)
        if obj is subject:
            return obj, True

        # Define handlers for different types of encounters based on the object's type
        handlers = {
            Captain: self.on_encounter_Captain,
            Rabbit: self.on_encounter_Rabbit,
            Snake: self.on_encounter_Snake,
            Veggie: self.on_encounter_Veggie,
            NoneType: self.on_encounter_None,
        }

        # Retrieve the appropriate handler based on the type of the encountered object
        handler = handlers.get(type(obj))

        # Raise an error if no handler is found for the encountered object's type
        if handler is None:
            raise NotImplementedError(f"on encounter {obj.__class__.__name__}")

        # Execute the handler and return its result
        return handler(subject, obj, object_x, object_y)

    def on_encounter_Rabbit(
        self, subject: Creature, rabbit: Rabbit, *_
    ) -> Tuple[Rabbit, bool]:
        # Handle an encounter with a rabbit
        if isinstance(subject, Captain):
            return rabbit, False  # Captain encounters rabbit, no movement
        if isinstance(subject, Rabbit):
            return rabbit, False  # Rabbit encounters another rabbit, no movement
        if isinstance(subject, Snake):
            return rabbit, False  # Snake encounters rabbit, no movement

        # If the subject type is not handled, raise an error
        raise NotImplementedError(get_func_name())

    def on_encounter_Captain(
        self, subject: Creature, captain: Captain, *_
    ) -> Tuple[Captain, bool]:
        # Handle an encounter with the Captain
        if isinstance(subject, Snake):
            # Snake encounters Captain, Captain loses some veggies
            veggies_lost = captain.lose_veggie(5)
            points_lost = sum(veggie.get_points() for veggie in veggies_lost)
            self.__score -= points_lost  # Deduct points for lost veggies
            self.initSnake()  # Reinitialize the snake
            return captain, False
        if isinstance(subject, Rabbit):
            return captain, False  # Rabbit encounters Captain, no movement
        if isinstance(subject, Captain):
            return captain, False  # Captain encounters itself, no movement

        # If the subject type is not handled, raise an error
        raise NotImplementedError(get_func_name())

    def on_encounter_Veggie(
        self, subject: Creature, veggie: Veggie, *_
    ) -> Tuple[Veggie, bool]:
        # Handle an encounter with a vegetable
        if isinstance(subject, Captain):
            # Captain encounters vegetable, adds it to collection
            subject.addVeggie(veggie)
            self.__score += veggie.get_points()  # Increase score
            return veggie, True
        if isinstance(subject, Rabbit):
            return veggie, True  # Rabbit encounters vegetable, movement allowed
        if isinstance(subject, Snake):
            return veggie, False  # Snake encounters vegetable, no movement

        # If the subject type is not handled, raise an error
        raise NotImplementedError(get_func_name())

    def on_encounter_Snake(
        self, subject: Creature, snake: Snake, *_
    ) -> Tuple[Snake, bool]:
        # Handle an encounter with a snake
        if isinstance(subject, Captain):
            veggies_lost = subject.lose_veggie(5)
            points_lost = sum(veggie.get_points() for veggie in veggies_lost)
            self.__score -= points_lost  # Deduct points for lost veggies
            self.initSnake()  # Reinitialize the snake
            return snake, True  # Captain encounters snake
        if isinstance(subject, Rabbit):
            return snake, False  # Rabbit encounters snake, no movement
        if isinstance(subject, Snake):
            return snake, False  # Snake encounters itself, no movement

        # If the subject type is not handled, raise an error
        raise NotImplementedError(get_func_name())

    def on_encounter_None(self, subject: Creature, none: None, *_) -> Tuple[None, bool]:
        # Handle an encounter with an empty space
        if type(subject) in (Captain, Rabbit, Snake):
            return None, True  # Movement allowed into an empty space

        # If the subject type is not handled, raise an error
        raise NotImplementedError(get_func_name())


def get_func_name() -> str:
    # Utility function to get the name of the current function
    return inspect.currentframe().f_back.f_code.co_name
