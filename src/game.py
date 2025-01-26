from snake_game import SnakeGame


def main():
    game = SnakeGame()
    while not game.quit:
        game.update()
        game.draw()


if __name__ == "__main__":
    main()
