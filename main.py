from GameEngine import GameEngine


def main():
    game_engine = GameEngine()
    game_engine.initializeGame()
    game_engine.intro()
    count = game_engine.remainingVeggies()
    while count > 0:
        print(f"{count} veggies remaining. Current score: {game_engine.getScore()}")
        game_engine.printField()
        game_engine.moveRabbits()
        game_engine.moveCaptain()
        game_engine.moveSnake()
        count = game_engine.remainingVeggies()
    game_engine.gameOver()
    game_engine.highScore()


if __name__ == "__main__":
    main()
