import csv
import inspect
import os
import pickle
import random
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
    __NUMBEROFVEGGIES = 30
    __NUMBEROFRABBITS = 5
    __HIGHSCOREFILE = "highscore.data"

    def __init__(self) -> None:
        self.__field: List[List[FieldInhabitant]] = []
        self.__rabbits: List[Rabbit] = []
        self.__veggies_collected: List[Veggie] = []
        self.__veggies_possible: List[Veggie] = []
        self.__captain: Captain = None
        self.__snake: Snake = None
        self.__score: int = 0

    def initVeggies(self) -> None:
        veggie_filename = input("Please enter the name of the vegetable point file: ")
        while not os.path.isfile(veggie_filename):
            veggie_filename = input(
                f"{veggie_filename} does not exist! Please enter the name of the vegetable point file: "
            )

        with open(veggie_filename, "r") as fo:
            data = [*csv.reader(fo)]
        _, dim1, dim2 = data.pop(0)
        self.field_init(int(dim1), int(dim2))

        for name, symbol, points in data:
            self.add_veggie_possible(name, symbol, int(points))

        for _ in range(self.__NUMBEROFVEGGIES):
            x, y = self.find_space()
            self.__field[y][x] = random.choice(self.__veggies_possible)
            # veggie_kind = random.randint(0, len(self.__veggies_possible) - 1)
            # (x, y) = self.findSpace()
            # self.__field[y][x] = self.__veggies_possible[veggie_kind]

    def initCaptain(self) -> None:
        if (captain := self.__captain) is not None:
            captain_x = captain.get_x()
            captain_y = captain.get_y()
            self.__field[captain_y][captain_x] = None

        x, y = self.find_space()
        self.__field[y][x] = self.__captain = Captain(x, y)

    def initRabbits(self) -> None:
        if (rabbits := self.__rabbits) is not None:
            for rabbit in rabbits:
                rabbit_x = rabbit.get_x()
                rabbit_y = rabbit.get_y()
                self.__field[rabbit_y][rabbit_x] = None
            self.__rabbits.clear()
        for _ in range(self.__NUMBEROFRABBITS):
            x, y = self.find_space()
            rabbit = Rabbit(x, y)
            self.__field[y][x] = rabbit
            self.__rabbits.append(rabbit)

    def initSnake(self) -> None:
        if (snake := self.__snake) is not None:
            snake_x = snake.get_x()
            snake_y = snake.get_y()
            self.__field[snake_y][snake_x] = None

        x, y = self.find_space()
        self.__field[y][x] = self.__snake = Snake(x, y)

    def initializeGame(self) -> None:
        self.initVeggies()
        self.initCaptain()
        self.initRabbits()
        self.initSnake()

    def remainingVeggies(self) -> int:
        return sum(isinstance(slot, Veggie) for row in self.__field for slot in row)
        # count = 0
        # for row in self.__field:
        #     for obj in row:
        #         if isinstance(obj, Veggie):
        #             count += 1
        # return count

    def intro(self) -> None:
        print("Welcome to Captain Veggie!")
        print(
            textwrap.fill(
                "The rabbits have invaded your garden and you must harvest as many vegetables as possible before the rabbits eat them all! Each vegetable is worth a different number of points so go for the high score!",
                width=58,
            )
        )

        print("\nThe vegetables are:")
        for veggie in self.__veggies_possible:
            symbol = veggie.get_inhabitant()
            name = veggie.get_name()
            points = veggie.get_points()
            print(f"{symbol}: {name} {points}")

        print("\nCaptain Veggie is V, and the rabbits are R's.")

        print("\nGood Luck!")

    def printField(self) -> None:
        cols = len(self.__field[0])

        print("#" * (3 * cols + 2))
        for row in self.__field:
            symbols = (
                inhabitant.get_inhabitant() if inhabitant is not None else " "
                for inhabitant in row
            )
            print(f'# {"  ".join(symbols)} #')
        print("#" * (3 * cols + 2))
        # for i in range(3 * len(self.__field[0]) + 2):
        #     print("#", end="")
        # for row in self.__field:
        #     print("\n#", end="")
        #     for obj in row:
        #         if obj is not None:
        #             print(" " + obj.get_inhabitant() + " ", end="")
        #         else:
        #             print("   ", end="")
        #     print("#", end="")
        # print("")
        # for i in range(3 * len(self.__field[0]) + 2):
        #     print("#", end="")
        # print("")

    def getScore(self) -> int:
        return self.__score

    def moveRabbits(self) -> None:
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
        for rabbit in self.__rabbits:
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
        direction = input(
            "Would you like to move up(W), down(S), left(A), or right(D): "
        ).lower()

        direction_map = {
            "w": lambda: self.moveCptVertical(-1),
            "s": lambda: self.moveCptVertical(1),
            "a": lambda: self.moveCptHorizontal(-1),
            "d": lambda: self.moveCptHorizontal(1),
        }

        valid_option = direction_map.get(direction)
        if not valid_option:
            print(f"{direction} is not a valid option")
            return

        encountered, ok = valid_option()
        if not ok:
            if encountered is None:
                print("You can't move that way")
            else:
                print(f"You're running into {encountered.__class__.__name__}")

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
        distance_x = self.__captain.get_x() - self.__snake.get_x()
        distance_y = self.__captain.get_y() - self.__snake.get_y()

        mx = 0 if distance_x == 0 else 1 if distance_x > 0 else -1
        my = 0 if distance_y == 0 else 1 if distance_y > 0 else -1

        if mx * my != 0:
            mx, my = random.choice([(mx, 0), (0, my)])
        encountered, ok = self.move_creature(self.__snake, mx, my)

        if isinstance(encountered, Captain):
            print("Attacked by Snake.")

    def gameOver(self) -> None:
        print("GAME OVER!")
        print("You managed to harvest the following vegetables:")
        for veggie in self.__veggies_collected:
            print(veggie.get_name())
        print(f"Your score was: {self.getScore()}")
        # print("Your score was: " + str(self.getScore()))

    def highScore(self) -> None:
        high_scores = []
        if os.path.isfile(self.__HIGHSCOREFILE):
            with open(self.__HIGHSCOREFILE, "rb") as file:
                high_scores.extend(pickle.load(file))

        new_name = input("Please enter your three initials to go on the scoreboard: ")
        new_name = new_name[:3].upper()

        high_scores.append((new_name, self.getScore()))
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

        print("HIGH SCORES")
        print(f'{"Name":<10}{"Score":<10}')
        for name, score in high_scores:
            print(f"{name:<10}{score:<10}")

        with open(self.__HIGHSCOREFILE, "wb") as file:
            pickle.dump(high_scores, file)

    def field_init(self, dim1: int, dim2: int) -> None:
        self.__field[:] = [[None for _ in range(dim2)] for _ in range(dim1)]

    def add_veggie_possible(self, name: str, symbol: str, points: int) -> None:
        self.__veggies_possible.append(Veggie(symbol, name, points))

    def find_space(self) -> Tuple[int, int]:
        row_len = len(self.__field)
        col_len = len(self.__field[0])
        max_attempt = int(row_len * col_len / 2)

        x = random.randrange(col_len)
        y = random.randrange(row_len)
        # x = random.randint(0, len(self.__field[0]) - 1)
        # y = random.randint(0, len(self.__field) - 1)
        while max_attempt > 0 and self.__field[y][x] is not None:
            x = random.randrange(col_len)
            y = random.randrange(row_len)
            max_attempt -= 1
            # x = random.randint(0, len(self.__field[0]) - 1)
            # y = random.randint(0, len(self.__field) - 1)
        if max_attempt == 0:
            spaces = (
                (x, y)
                for y in range(row_len)
                for x in range(col_len)
                if self.__field[y][x] is not None
            )
            x, y = random.choice(spaces)

        return x, y

    def move_creature(
        self, creature: Creature, mx: int, my: int
    ) -> Tuple[FieldInhabitant, bool]:
        if mx == 0 and my == 0:
            return creature, True

        x_original = creature.get_x()
        y_original = creature.get_y()
        x_new = x_original + mx
        y_new = y_original + my
        row_len = len(self.__field)
        col_len = len(self.__field[0])
        # x_new += mx
        # y_new += my

        if x_new < 0 or y_new < 0 or x_new > col_len or y_new > row_len:
            return None, False

        encountered, ok = self.on_encounter(creature, x_new, y_new)
        if ok:
            self.__field[y_original][x_original] = None
            self.__field[y_new][x_new] = creature
            creature.set_x(x_new)
            creature.set_y(y_new)

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
        row_len = len(self.__field)
        col_len = len(self.__field[0])
        if object_x < 0 or object_y < 0 or object_x >= col_len or object_y >= row_len:
            return None, False

        obj = self.__field[object_y][object_x]
        if obj is subject:
            return obj, True

        handlers = {
            Captain: self.on_encounter_Captain,
            Rabbit: self.on_encounter_Rabbit,
            Snake: self.on_encounter_Snake,
            Veggie: self.on_encounter_Veggie,
            NoneType: self.on_encounter_None,
        }
        handler = handlers.get(type(obj))
        if handler is None:
            raise NotImplementedError(get_func_name())
        return handler(subject, obj, object_x, object_y)

    def on_encounter_Rabbit(
        self, subject: Creature, rabbit: Rabbit, *_
    ) -> Tuple[Rabbit, bool]:
        if isinstance(subject, Captain):
            print("Don't step on the bunnies!")
            return rabbit, False
        if isinstance(subject, Rabbit):
            return rabbit, False
        if isinstance(subject, Snake):
            return rabbit, False

        raise NotImplementedError(get_func_name())

    def on_encounter_Captain(
        self, subject: Creature, captain: Captain, *_
    ) -> Tuple[Captain, bool]:
        if isinstance(subject, Snake):
            veggies_collected = self.__veggies_collected

            veggies_lost = veggies_collected[-5:]
            self.__score -= sum(veggie.get_points() for veggie in veggies_lost)

            veggies_collected[:] = (
                veggies_collected[:-5] if len(veggies_collected) >= 5 else []
            )

            self.initSnake()
            return captain, False
        if isinstance(subject, Rabbit):
            return captain, False
        if isinstance(subject, Captain):
            return captain, False

        raise NotImplementedError(get_func_name())

    def on_encounter_Veggie(
        self, subject: Creature, veggie: Veggie, veggie_x: int, veggie_y: int
    ) -> Tuple[Veggie, bool]:
        subject_x = subject.get_x()
        subject_y = subject.get_y()
        if isinstance(subject, Captain):
            self.__field[veggie_y][veggie_x] = subject
            self.__field[subject_y][subject_x] = None
            self.__veggies_collected.append(veggie)
            self.__score += veggie.get_points()
            print(f"Yummy! A delicious {veggie.get_name()}")
            return veggie, True
        if isinstance(subject, Rabbit):
            self.__field[veggie_y][veggie_x] = subject
            self.__field[subject_y][subject_x] = None
            return veggie, True
        if isinstance(subject, Snake):
            return veggie, False

        raise NotImplementedError(get_func_name())

    def on_encounter_Snake(
        self, subject: Creature, snake: Snake, *_
    ) -> Tuple[Snake, bool]:
        if isinstance(subject, Captain):
            return snake, False
        if isinstance(subject, Rabbit):
            return snake, False
        if isinstance(subject, Snake):
            return snake, False

        raise NotImplementedError(get_func_name())

    def on_encounter_None(
        self, subject: Creature, none: None, object_x: int, object_y: int
    ) -> Tuple[None, bool]:
        if type(subject) in (Captain, Rabbit, Snake):
            subject_x = subject.get_x()
            subject_y = subject.get_y()
            self.__field[object_y][object_x] = subject
            self.__field[subject_y][subject_x] = None
            return None, True

        raise NotImplementedError(get_func_name())


def get_func_name() -> str:
    return inspect.currentframe().f_back.f_code.co_name
