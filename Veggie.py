from FieldInhabitant import FieldInhabitant


class Veggie(FieldInhabitant):
    """
    Represents a Veggie, a specific type of FieldInhabitant.

    The Veggie class inherits from FieldInhabitant and adds additional attributes and methods
    related to the name and points associated with a Veggie.

    Attributes:
        __name (str): The name of the Veggie.
        __points (int): The point value associated with the Veggie.
    """

    def __init__(self, inhabitant: str, name: str, points: int) -> None:
        """
        Initializes a new instance of the Veggie class.

        Args:
            inhabitant (str): The type of the inhabitant (passed to the FieldInhabitant base class).
            name (str): The name of the Veggie.
            points (int): The point value of the Veggie.
        """
        super().__init__(inhabitant)  # Initialize the base class FieldInhabitant
        self.set_name(name)  # Set the name of the Veggie
        self.set_points(points)  # Set the points of the Veggie

    def __str__(self) -> str:
        """
        Provides a string representation of the Veggie instance.

        Returns:
            str: A string representing the Veggie, including its type, name, and point value.
        """
        # Return the formatted string representation
        return f"{self.get_inhabitant()}: {self.get_name()} {self.get_points()} points"

    def get_name(self) -> str:
        """
        Retrieves the name of the Veggie.

        Returns:
            str: The name of the Veggie.
        """
        return self.__name  # Return the private attribute __name

    def set_name(self, name: str) -> None:
        """
        Sets the name of the Veggie.

        Args:
            name (str): The new name for the Veggie.
        """
        self.__name = name  # Set the private attribute __name to the provided value

    def get_points(self) -> int:
        """
        Retrieves the point value of the Veggie.

        Returns:
            int: The point value of the Veggie.
        """
        return self.__points  # Return the private attribute __points

    def set_points(self, points: int) -> None:
        """
        Sets the point value of the Veggie.

        Args:
            points (int): The new point value for the Veggie.
        """
        self.__points = (
            points  # Set the private attribute __points to the provided value
        )
