from Creature import Creature


class Snake(Creature):
    """
    Represents a Snake, a specialized form of Creature.

    The Snake class inherits from the Creature class and is characterized by a specific
    inhabitant type symbol ("S"). It maintains the coordinates functionalities of the Creature class.

    Attributes:
        Inherited from the Creature class.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new instance of the Snake class.

        The Snake is initialized with a specific inhabitant symbol ("S") and its position coordinates.

        Args:
            x (int): The initial x-coordinate position of the Snake.
            y (int): The initial y-coordinate position of the Snake.
        """
        super().__init__(
            "S", x, y
        )  # Initialize the Creature base class with 'S' for Snake and the given coordinates
