from FieldInhabitant import FieldInhabitant


class Creature(FieldInhabitant):
    """
    Represents a Creature, which is a specific type of FieldInhabitant.

    The Creature class inherits from FieldInhabitant and adds functionalities
    related to the coordinates (x and y) where the creature is located.

    Attributes:
        _x (int): The x-coordinate of the creature's position.
        _y (int): The y-coordinate of the creature's position.
    """

    def __init__(self, inhabitant: str, x: int, y: int) -> None:
        """
        Initializes a new instance of the Creature class.

        Args:
            inhabitant (str): The type of the inhabitant (passed to the FieldInhabitant base class).
            x (int): The initial x-coordinate position of the Creature.
            y (int): The initial y-coordinate position of the Creature.
        """
        super().__init__(inhabitant)  # Initialize the base class FieldInhabitant
        self.set_x(x)  # Set the x-coordinate of the Creature
        self.set_y(y)  # Set the y-coordinate of the Creature

    def get_x(self) -> int:
        """
        Retrieves the x-coordinate of the Creature.

        Returns:
            int: The x-coordinate of the Creature.
        """
        return self._x  # Return the private attribute _x

    def set_x(self, x: int) -> None:
        """
        Sets the x-coordinate of the Creature.

        Args:
            x (int): The new x-coordinate for the Creature.
        """
        self._x = x  # Set the private attribute _x to the provided value

    def get_y(self) -> int:
        """
        Retrieves the y-coordinate of the Creature.

        Returns:
            int: The y-coordinate of the Creature.
        """
        return self._y  # Return the private attribute _y

    def set_y(self, y: int) -> None:
        """
        Sets the y-coordinate of the Creature.

        Args:
            y (int): The new y-coordinate for the Creature.
        """
        self._y = y  # Set the private attribute _y to the provided value
