import os
import csv


class GameEngine:
    __NUMBEROFVEGGIES = 30
    __NUMBEROFRABBITS = 5
    __HIGHSCOREFILE = "highscore.data"

    def __init__(self) -> None:
        __field, __rabbits, __veggies = [], [], []
        __captain = None
        __score = 0

    def initVeggies(self) -> None:
        veggie_filename = input("Please enter the name of the vegetable point file: ")
        while not os.path.isfile(veggie_filename):
            veggie_filename = input(
                f"{veggie_filename} does not exist! Please enter the name of the vegetable point file: "
            )

        with open(veggie_filename, "w") as fo:
            data = [*csv.reader(fo)]

        _, dim1, dim2 = data.pop(0)


        for name,symbol,points in data:
            

    def initField(self,dim1:int,dim2:int)->None:
        
