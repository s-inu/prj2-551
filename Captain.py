from typing import List

from Creature import Creature
from Veggie import Veggie


class Captain(Creature):
    """
    Represents a Captain, a specific type of Creature, with unique properties and actions.

    The Captain class inherits from the Creature class and adds the functionality to manage
    a collection of 'Veggie' objects.

    Attributes:
        __veggies (List[Veggie]): A private list to store Veggie objects.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new instance of the Captain class.

        Args:
            x (int): The x-coordinate position of the Captain.
            y (int): The y-coordinate position of the Captain.
        """
        super().__init__("V", x, y)  # Initialize the Creature base class
        self.__veggies = []  # Initialize an empty list to store Veggie objects

    def get_veggies(self) -> List[Veggie]:
        """
        Retrieves the list of Veggie objects the Captain has.

        Returns:
            List[Veggie]: The list of Veggie objects.
        """
        return self.__veggies  # Return the private attribute __veggies

    def addVeggie(self, veggie: Veggie) -> None:
        """
        Adds a Veggie object to the Captain's collection.

        Args:
            veggie (Veggie): The Veggie object to be added.
        """
        self.__veggies.append(
            veggie
        )  # Append the provided Veggie object to the __veggies list

    def lose_veggie(self, count: int) -> List[Veggie]:
        """
        Removes a specified number of Veggie objects from the end of the Captain's collection
        and returns them.

        Args:
            count (int): The number of Veggie objects to remove.

        Returns:
            List[Veggie]: The list of removed Veggie objects.
        """
        count = min(
            count, len(self.__veggies)
        )  # Determine the actual number of veggies to be removed
        # Split __veggies into the remaining and the removed veggies
        self.__veggies, veggies_lost = self.__veggies[:-count], self.__veggies[-count:]

        return veggies_lost  # Return the list of removed Veggie objects
