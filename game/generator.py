from game.grid import Grid


class Generator():

    def __init__(self, size: int):
        self.grid = self._generate_grid(size, size)

    def _generate_grid(self, width: int, height: int):

        grid = Grid(width=width, height=height)

        grid.generate()

        print(f"Count solutions: {Grid().count_solutions(grid.cells)}")

        return grid