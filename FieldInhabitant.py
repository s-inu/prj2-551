class FieldInhabitant:
    def __init__(self, inhabitant: str) -> None:
        self.set_inhabitant(inhabitant)

    def get_inhabitant(self) -> str:
        return self._inhabitant

    def set_inhabitant(self, inhabitant: str) -> None:
        self._inhabitant = inhabitant
