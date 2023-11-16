import os
import csv
import pickle
import random

from Captain import Captain
from Rabbit import Rabbit
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

    def findSpace(self):
        x = random.randint(0, len(self.__field[0] - 1))
        y = random.randint(0, len(self.__field) - 1)
        while self.__field[y][x] != None:
            x = random.randint(0, len(self.__field[0] - 1))
            y = random.randint(0, len(self.__field) - 1)
        return (x,y)


    def initVeggies(self) -> None:
        veggie_filename = input("Please enter the name of the vegetable point file: ")
        while not os.path.isfile(veggie_filename):
            veggie_filename = input(
                f"{veggie_filename} does not exist! Please enter the name of the vegetable point file: "
            )

        with open(veggie_filename, "r") as fo:
            data = [*csv.reader(fo)]

        _, dim1, dim2 = data.pop(0)
        self.field_init(dim1, dim2)

        for name, symbol, points in data:
            self.add_veggie_possible(name, symbol, int(points))

        for i in range(self.__NUMBEROFVEGGIES):
            veggie_kind=random.randint(0,len(self.__veggies_possible)-1)
            (x,y)=self.findSpace()
            self.__field[y][x]=self.__veggies_possible[veggie_kind]





    def initCaptain(self):
        (x,y)=self.findSpace()
        self.__field[y][x]=Captain(x,y)
        self.__captain=self.__field[y][x]

    def initRabbits(self):
        for i in range(self.__NUMBEROFRABBITS):
            (x,y)=self.findSpace()
            rabbit=Rabbit(x,y)
            self.__field[y][x]=rabbit
            self._rabbits.append(rabbit)

    def initializeGame(self):
        self.initVeggies()
        self.initCaptain()
        self.initRabbits()

    def remainingVeggies(self):
        count=0
        for row in self.__field:
            for obj in row:
                if isinstance(obj,Veggie):
                    count+=1
        return count


    def intro(self):
        print("Welcome to Captain Veggie!")
        print("The rabbits have invaded your garden and you must harvest\
        as many vegetables as possible before the rabbits eat them\
        all! Each vegetable is worth a different number of points\
        so go for the high score!\n")
        print("The vegetables are:")
        for veggie in self.__veggies_possible:
            print(veggie.get_inhabitant()+": "+veggie.get_name()+" "+str(veggie.get_points()+" points"))
        print("\nCaptain Veggie is V, and the rabbits are R's.\n\nGood Luck!")

    def printField(self):
        for i in range(3*len(self.__field[0])+2):
            print("#",end="")
        for row in self.__field:
            print("\n#",end="")
            for obj in row:
                if obj!=None:
                    print(" "+obj.get_inhabitant()+" ")
                else:
                    print("   ")
            print("#",end="")
        print("\n")
        for i in range(3*len(self.__field[0])+2):
            print("#",end="")



    def getScore(self):
        return self.__score

    def moveCreature(self,creature,mx,my):
        x=creature.get_x()
        y=creature.get_y()
        x+=mx
        y+=my
        if x<0 or x>len(self.__field[0])-1 or y<0 or y>len(self.__field):
            return "Wall"
        else:
            if self.__field[y][x] == None:
                creature.set_x(x)
                creature.set_y(y)
                self.__field[y][x] = creature
                self.__field[y-my][x-mx]=None
            elif isinstance(self.__field[y][x], Veggie):
                tempVeggie=self.__field[y][x]
                creature.set_x(x)
                creature.set_y(y)
                self.__veggies.remove(self.__field[y][x])
                self.__field[y][x] = creature
                self.__field[y - my][x - mx] = None
                return tempVeggie
            elif isinstance(self.__field[y][x],Rabbit):
                return self.__field[y][x]
        return None

    def moveRabbits(self):
        for rabbit in self._rabbits:
            action=random.randint(0,8)
            if action==0:
                continue
            elif action==1:
                self.moveCreature(rabbit,1,0)
            elif action==2:
                self.moveCreature(rabbit,-1,0)
            elif action==3:
                self.moveCreature(rabbit,0,1)
            elif action==4:
                self.moveCreature(rabbit,0,-1)
            elif action==5:
                self.moveCreature(rabbit,1,1)
            elif action==6:
                self.moveCreature(rabbit,-1,1)
            elif action==7:
                self.moveCreature(rabbit,1,-1)
            elif action==8:
                self.moveCreature(rabbit,-1,1)


    def moveCptVertical(self,step):
        res=self.moveCreature(self.__captain,0,step)
        if res!=None:
            if isinstance(res,Veggie):
                print("Yummy! A delicious "+res.get_name())
                self.__veggies.append(res)
                self.__score+=res.get_points()
            elif isinstance(res,Rabbit):
                print("Don't step on the bunnies!")
            else:
                print("You can't move that way!")

    def moveCptHorizontal(self, step):
        res = self.moveCreature(self.__captain, step, 0)
        if res != None:
            if isinstance(res, Veggie):
                print("Yummy! A delicious " + res.get_name())
                self.__veggies.append(res)
                self.__score += res.get_points()
            elif isinstance(res, Rabbit):
                print("Don't step on the bunnies!")
            else:
                print("You can't move that way!")



    def moveCaptain(self):
        direction=input("Would you like to move up(W), down(S), left(A), or right(D): ")
        if direction.lower()=="w":
            self.moveCptVertical(1)
        elif direction.lower()=="s":
            self.moveCptVertical(-1)
        elif direction.lower()=="a":
            self.moveCptHorizontal(-1)
        elif direction.lower()=="d":
            self.moveCptHorizontal(1)
        else:
            print(direction+" is not a valid option")


    def gameOver(self):
        print("GAME OVER!")
        print("You managed to harvest the following vegetables:")
        for veggie in self.__veggies:
            print(veggie.get_name())
        print("Your score was: "+self.getScore())


    def highScore(self):
        scores=[]
        if os.path.exists(self.__HIGHSCOREFILE):
            with open(self.__HIGHSCOREFILE,"rb") as file:
                scorelist = pickle.load(file)
                for score in scorelist:
                    scores.append(score)
        name = input("Please enter your three initials to go on the scoreboard: ")
        index=0
        for pair in scores:
            name,score=pair
            if score<self.getScore():
                break
            index+=1
        scores.insert(index,(name[0:min(len(name),3)],self.getScore()))

        print("HIGH SCORES")
        print("Name    Score")
        for pair in scores:
            name,score=pair
            print(name.ljest(17)+str(score))

        with open(self.__HIGHSCOREFILE, "rw") as file:
            pickle.dump(scores,file)



    def field_init(self, dim1: int, dim2: int) -> None:
        self.__filed = [[None for _ in range(dim2)] for _ in range(dim1)]

    def add_veggie_possible(self, name: str, symbol: str, points: int) -> None:
        self.__veggies_possible.append(Veggie(symbol, name, points))
