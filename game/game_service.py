from game.grid import Grid

class GameService():

    def create_game(self) -> Grid:
        from game.generator import Generator
        generator = Generator(size=10)  # Assuming a default size of 10x10
        return generator.grid