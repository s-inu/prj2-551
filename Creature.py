from FieldInhabitant import FieldInhabitant


class Creature(FieldInhabitant):
    def __init__(self, inhabitant: str, x: int, y: int) -> None:
        super().__init__(inhabitant)
        self.set_x(x)
        self.set_y(y)

    def get_x(self) -> int:
        return self._x

    def set_x(self, x: int) -> None:
        self._x = x

    def get_y(self) -> int:
        return self._y

    def set_y(self, y: int) -> None:
        self._y = y
