from GameEngine import GameEngine  # Import the GameEngine class


def main():
    # Main function to run the game

    game_engine = GameEngine()  # Create an instance of the game engine
    game_engine.initializeGame()  # Initialize the game (setup field, creatures, etc.)
    game_engine.intro()  # Display the introductory text of the game

    # Get the initial count of remaining vegetables
    count = game_engine.remainingVeggies()

    # Continue the game loop as long as there are vegetables remaining
    while count > 0:
        # Display the number of remaining veggies and current score
        print(f"{count} veggies remaining. Current score: {game_engine.getScore()}")

        game_engine.printField()  # Print the current state of the game field
        game_engine.moveRabbits()  # Move the rabbits on the field
        game_engine.moveCaptain()  # Move the Captain based on player input
        game_engine.moveSnake()  # Move the snake towards the Captain

        # Update the count of remaining vegetables
        count = game_engine.remainingVeggies()

    # Handle the end of the game
    game_engine.gameOver()  # Display the game over message
    game_engine.highScore()  # Handle the high score recording and display


if __name__ == "__main__":
    main()
