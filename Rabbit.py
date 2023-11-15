from Creature import Creature


class Rabbit(Creature):
    def __init__(self, x: int, y: int) -> None:
        super().__init__("R", x, y)
