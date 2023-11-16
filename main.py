from GameEngine import GameEngine


def main():
    gameEngine=GameEngine()
    gameEngine.initializeGame()
    gameEngine.intro()
    count=gameEngine.remainingVeggies()
    while count>0:
        print(str(count)+" veggies remaining. Current score: "+str(gameEngine.getScore()))
        gameEngine.printField()
        gameEngine.moveRabbits()
        gameEngine.moveCaptain()
        count=gameEngine.remainingVeggies()
    gameEngine.gameOver()
    gameEngine.highScore()

if __name__ == "__main__":
    main()
