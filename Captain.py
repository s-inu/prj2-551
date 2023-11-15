from typing import List
from Creature import Creature
from Veggie import Veggie


class Captain(Creature):
    def __init__(self, x: int, y: int) -> None:
        super().__init__("V", x, y)
        self.__veggies = []

    def get_veggies(self) -> List[Veggie]:
        return self.__veggies

    def addVeggie(self, veggie: Veggie) -> None:
        self.__veggies.append(veggie)
