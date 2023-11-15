from FieldInhabitant import FieldInhabitant


class Veggie(FieldInhabitant):
    def __init__(self, inhabitant: str, name: str, points: int) -> None:
        super().__init__(inhabitant)
        self.set_name(name)
        self.set_points(points)

    def __str__(self) -> str:
        return f"{self.get_inhabitant()}: {self.get_name()} {self.get_points()} points"

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_points(self) -> int:
        return self.__points

    def set_points(self, points: int) -> None:
        self.__points = points
