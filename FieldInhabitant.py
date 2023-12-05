class FieldInhabitant:
    """
    Represents an inhabitant of a field.

    This class provides methods to set and get the type of the inhabitant.

    Attributes:
        _inhabitant (str): A string representing the type of the inhabitant.
    """

    def __init__(self, inhabitant: str) -> None:
        """
        Initializes a new FieldInhabitant instance.

        Args:
            inhabitant (str): The type of the inhabitant to be set for this field.
        """
        self.set_inhabitant(
            inhabitant
        )  # Set the inhabitant using the provided argument

    def get_inhabitant(self) -> str:
        """
        Retrieves the type of the inhabitant.

        Returns:
            str: The type of the inhabitant.
        """
        return self._inhabitant  # Return the private attribute _inhabitant

    def set_inhabitant(self, inhabitant: str) -> None:
        """
        Sets the type of the inhabitant.

        Args:
            inhabitant (str): The type of the inhabitant to set.
        """
        self._inhabitant = (
            inhabitant  # Set the private attribute _inhabitant to the provided value
        )
