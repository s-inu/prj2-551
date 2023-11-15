import os
import csv
import random
from Veggie import Veggie


class GameEngine:
    __NUMBEROFVEGGIES = 30
    __NUMBEROFRABBITS = 5
    __HIGHSCOREFILE = "highscore.data"

    def __init__(self) -> None:
        self.__field, self._rabbits, self.__veggies = [], [], []
        self.__captain = None
        self.__score = 0
        self.__veggies_possible = []

    def initVeggies(self) -> None:
        veggie_filename = input("Please enter the name of the vegetable point file: ")
        while not os.path.isfile(veggie_filename):
            veggie_filename = input(
                f"{veggie_filename} does not exist! Please enter the name of the vegetable point file: "
            )

        with open(veggie_filename, "w") as fo:
            data = [*csv.reader(fo)]

        _, dim1, dim2 = data.pop(0)
        self.initField(dim1, dim2)

        for name, symbol, points in data:
            self.add_veggie_possible(name, symbol, points)

    def initCaptain(self):
        pass

    def initRabbits(self):
        pass

    def initializeGame(self):
        pass

    def remainingVeggies(self):
        pass

    def intro(self):
        pass

    def printField(self):
        pass

    def getScore(self):
        pass

    def moveRabbits(self):
        pass

    def moveCptVertical(self):
        pass

    def moveCptHorizontal(self):
        pass

    def moveCaptain(self):
        pass

    def gameOver(self):
        pass

    def highScore(self):
        pass

    def initField(self, dim1: int, dim2: int) -> None:
        for _ in range(dim1):
            self.__field.append([None for _ in range(dim2)])

    def add_veggie_possible(self, name: str, symbol: str, points: int) -> None:
        self.__veggies_possible.append(Veggie(symbol, name, points))
