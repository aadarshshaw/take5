from Game import Game

def main():
    # Initialize the game
    game = Game()

    # Start the server and wait for players to connect
    game.waitForPlayers()

    # Once all players have connected, start the game
    game.startGame()

    # Run the game until it's finished
    game.runGame()

if __name__ == "__main__":
    main()
