from Creature import Creature


class Rabbit(Creature):
    """
    Represents a Rabbit, a specialized form of Creature.

    The Rabbit class inherits from the Creature class and is characterized by a specific
    inhabitant type symbol ("R"). It maintains the coordinates functionalities of the Creature class.

    Attributes:
        Inherited from the Creature class.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new instance of the Rabbit class.

        The Rabbit is initialized with a specific inhabitant symbol ("R") and its position coordinates.

        Args:
            x (int): The initial x-coordinate position of the Rabbit.
            y (int): The initial y-coordinate position of the Rabbit.
        """
        super().__init__(
            "R", x, y
        )  # Initialize the Creature base class with 'R' for Rabbit and the given coordinates
