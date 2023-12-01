from Creature import Creature


class Snake(Creature):
    def __init__(self, x: int, y: int) -> None:
        super().__init__("S", x, y)
