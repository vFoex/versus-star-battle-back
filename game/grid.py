from turtle import width
from typing import List, Tuple
from model.grid_model import GridCellContent, GridCellModel, GridModel
import random


class GridCell():
    is_occupied: bool
    region_color: str
    x: int
    y: int

    def __init__(self, x: int, y: int, is_occupied: bool = False, region_color: str = None):
        self.is_occupied = is_occupied
        self.region_color = region_color
        self.x = x
        self.y = y

    def to_dto(self) -> GridCellModel:
        if self.region_color is None:
            raise ValueError("Region color is not set")
        
        return GridCellModel(
            x=self.x,
            y=self.y,
            region_color=self.region_color
        )

class Grid():
    colors: List[str]
    cells: List[List[GridCell]]
    width: int
    height: int
    
    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height
        self.colors = []
        self.generate_random_colors(nb_colors=min(self.width, self.height))
        self.init_grid()

    def init_grid(self):
        self.cells = [[GridCell(x, y, region_color=self.colors[0]) for x in range(self.width)] for y in range(self.height)]
    # def generate_v2(self):

    #     while self.get_star_count() < min(self.width, self.height):
    #         self.cells = [[GridCell(x, y) for x in range(self.width)] for y in range(self.height)]
    #         positions = [(x, y) for x in range(self.width) for y in range(self.height)]
    #         random.shuffle(positions)

    #         for i in range(len(self.colors)):
    #             x, y = positions[i]
    #             color = self.colors[i % len(self.colors)]
    #             self.cells[y][x] = GridCell(x, y, is_occupied=False, region_color=color)

    #         self.fill_empty_cells()

    #         for x, y in positions:
    #             if self.is_valid_star_position(x, y):
    #                 self.cells[y][x].is_occupied = True
        
    #     i = 0
    #     # while self.count_solutions(self.cells) > 1:
    #     #     print(f"Try {i}: Count solutions: {self.count_solutions(self.cells)}")
    #     #     current_solutions_count = self.count_solutions(self.cells)
    #     #     copied_cells = [row[:] for row in self.cells]
    #     #     positions = [(x, y) for x in range(self.width) for y in range(self.height)]
    #     #     random.shuffle(positions)
    #     #     for x, y in positions:
    #     #         if self.cells[y][x].is_occupied:
    #     #             continue
    #     #         adgacent_colors = self.get_adgacent_colors(x, y)
    #     #         simplified_adgacent_colors = [color for color in adgacent_colors if color != self.cells[y][x].region_color]
    #     #         if len(simplified_adgacent_colors) > 0:
    #     #             for color in simplified_adgacent_colors:
    #     #                 copied_cells[y][x].region_color = color
    #     #                 new_solutions_count = self.count_solutions(copied_cells)
    #     #                 if new_solutions_count > 0 and new_solutions_count < current_solutions_count:
    #     #                     break
    #     #             else:
    #     #                 copied_cells[y][x].region_color = self.cells[y][x].region_color
    #     #     self.cells = copied_cells
    #     #     i += 1
    #     print(f"Final count solutions: {self.count_solutions(self.cells)}")


    def generate(self):
        # Créer une liste de toutes les positions possibles

        while self.get_star_count() < min(self.width, self.height):
            self.init_grid()
            positions = [(x, y) for x in range(self.width) for y in range(self.height)]
            random.shuffle(positions)

            star_positions = []

            first_star = True
            first_star_color = self.colors[0]

            for x, y in positions:
                if self.is_valid_star_position(x, y):
                    color = self.colors[(y * self.width + x) % len(self.colors)]
                    self.cells[y][x] = GridCell(x, y, is_occupied=True, region_color=color)
                    if not first_star:
                        star_positions.append((y, x))
                    else:
                        first_star = False

            # color_changed_number = 0
            # while color_changed_number < (self.width*self.height)/2:
        
            for star_pos in star_positions:
                random_range = 0.9
                current_position = (star_pos[0], star_pos[1])
                r = random.random()
                while r < random_range:
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    random.shuffle(directions)
                    for direction in directions:
                        test_grid = self.copy_cells()
                        y, x = current_position[0] - direction[0], current_position[1] - direction[1]
                        if 0 <= y < self.height and 0 <= x < self.width:
                            if not test_grid[y][x].is_occupied and test_grid[y][x].region_color == first_star_color and test_grid[y][x].region_color != test_grid[current_position[0]][current_position[1]].region_color:
                                test_grid[y][x].region_color = test_grid[current_position[0]][current_position[1]].region_color
                                if Grid().check_adjacency(test_grid) and Grid().count_solutions(test_grid) == 1:
                                    self.cells[y][x].region_color = test_grid[y][x].region_color
                                    current_position = (y, x)
                                    random_range = random_range - 0.05
                                    break
                                else:
                                    if self.cells[y][x].region_color == test_grid[y][x].region_color:
                                        print(f"AYO")
                    random_range = random_range - 0.02

        print(f"Count solutions: {Grid().count_solutions(self.cells)}")

    def check_adjacency(cls, cells: List[List[GridCell]]) -> bool:
        """
        Check if the grid has valid adjacency colors.
        """

        colors_dict = {}

        for y in range(len(cells)):
            for x in range(len(cells[y])):
                neighbor_cells_colors = set()
                if y-1 >= 0:
                    neighbor_cells_colors.add(cells[y-1][x].region_color)
                if y+1  < len(cells):
                    neighbor_cells_colors.add(cells[y+1][x].region_color)
                if x-1 >= 0:
                    neighbor_cells_colors.add(cells[y][x-1].region_color)
                if x+1 < len(cells[y]):
                    neighbor_cells_colors.add(cells[y][x+1].region_color)
                if cells[y][x].region_color not in colors_dict:
                    colors_dict[cells[y][x].region_color] = {
                        'count': 1,
                    }
                else:
                    colors_dict[cells[y][x].region_color]['count'] += 1
                if cells[y][x].region_color not in list(neighbor_cells_colors):
                    colors_dict[cells[y][x].region_color]['no_neighbor'] = True

        for color, data in colors_dict.items():
            if data['count'] > 1 and 'no_neighbor' in data:
                return False
        return True

    def copy_cells(self) -> List[List[GridCell]]:
        """
        Returns a deep copy of the cells.
        """
        return [[GridCell(cell.x, cell.y, cell.is_occupied, cell.region_color) for cell in row] for row in self.cells]
        

    def generate_random_colors(self, nb_colors: int):

        # fill the colors list with random Hexa colors, not too dark or too light and not too similar
        # to avoid confusion for players
        self.colors = []
        for _ in range(nb_colors):
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            while color in self.colors or self.is_too_similar(color):
                color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            self.colors.append(color)

    def is_valid_star_position(self, x: int, y: int) -> bool:

        # current_color_cells = [cell for row in self.cells for cell in row if cell.region_color == self.cells[y][x].region_color]
        # if any(cell.is_occupied for cell in current_color_cells):
        #     return False

        # Check adjacency cells (including diagonals) to ensure no other stars are present
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.cells[ny][nx].is_occupied:
                        return False
        
        # Check row and column for existing stars
        for i in range(self.width):
            if self.cells[y][i].is_occupied:
                return False
            
        for i in range(self.height):
            if self.cells[i][x].is_occupied:
                return False
        
        return True


    def is_too_similar(self, color: str) -> bool:
        if not self.colors:
            return False
        # Check if the color is too similar to any existing color in the grid
        r1, g1, b1 = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        for existing_color in self.colors:
            r2, g2, b2 = int(existing_color[1:3], 16), int(existing_color[3:5], 16), int(existing_color[5:7], 16)
            if abs(r1 - r2) < 50 and abs(g1 - g2) < 50 and abs(b1 - b2) < 50:
                return True
        return False 
    
    def fill_empty_cells(self):

        # Fill color of cells without colors, a cell should be of a color of an adjacency cell, if no colored adjacency cell, go to the next cell. Do this till all cells are colored
        while any(cell.region_color is None for row in self.cells for cell in row):
            for y in range(self.height):
                for x in range(self.width):
                    if self.cells[y][x].region_color is not None:
                        continue
                    adgacent_colors = self.get_adgacent_colors(x, y)
                    if len(adgacent_colors) == 0:
                        continue
                    self.cells[y][x].region_color = random.choice(adgacent_colors)

    def get_adgacent_colors(self, x: int, y: int) -> List[str]:
        # Get colors of adjacent cells (not diagonals)
        adgacent_colors = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                adjacent_cell: GridCell = self.cells[ny][nx]
                if adjacent_cell.region_color is not None:
                    adgacent_colors.add(adjacent_cell.region_color)
        return list(adgacent_colors)

    def to_string(self) -> str:
        grid_str = ""
        for row in self.cells:
            row_str = " | ".join(
                f"{'*' if cell.is_occupied else ''}{cell.region_color if cell.region_color else 'Empty'}"
                for cell in row
            )
            grid_str += row_str + "\n"
        return grid_str

    def to_dto(self) -> GridModel:
        return GridModel(
            width=self.width,
            height=self.height,
            cells=[[cell.to_dto() for cell in row] for row in self.cells]
        )
    
    def check_game_over(self, grid_model: GridModel) -> bool:
        if self.height != grid_model.height or self.width != grid_model.width:
            return False        
        
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                grid_cell = grid_model.cells[y][x]
                if (cell.region_color != grid_cell.region_color) or (cell.is_occupied and (grid_cell.content != GridCellContent.STAR)) or (not cell.is_occupied and grid_cell.content == GridCellContent.STAR):
                    print(f"Game not over: cell mismatch at ({x}, {y}), cell content should be {'star' if cell.is_occupied else 'empty'}, but got {grid_cell.content}")
                    return False
        print("Game over: all cells match")
        return True

    def count_solutions(cls, cells: List[List[GridCell]]) -> int:
        """
        Compte le nombre de solutions valides pour cette grille,
        en plaçant une étoile par région.
        """

        # Obtenir les régions (dictionnaire: couleur -> liste de positions)
        regions = {}
        for y in range(len(cells)):
            for x in range(len(cells[y])):
                cell = cells[y][x]
                if cell.region_color not in regions:
                    regions[cell.region_color] = []
                regions[cell.region_color].append((x, y))

        # Variables pour le backtracking
        used_rows = set()
        used_cols = set()
        stars = set()  # positions déjà utilisées
        solutions = [0]  # compteur modifiable dans la fonction récursive

        def is_valid(x, y):
            # Vérifie l'adjacence
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (x + dx, y + dy) in stars:
                        return False
            return True

        def backtrack(region_index=0):
            if region_index == len(regions):
                solutions[0] += 1
                return

            region_colors = list(regions.keys())
            region = regions[region_colors[region_index]]

            for x, y in region:
                if y in used_rows or x in used_cols:
                    continue
                if not is_valid(x, y):
                    continue

                # Place une étoile
                stars.add((x, y))
                used_rows.add(y)
                used_cols.add(x)

                backtrack(region_index + 1)

                # Retire l'étoile (backtrack)
                stars.remove((x, y))
                used_rows.remove(y)
                used_cols.remove(x)

        backtrack()
        return solutions[0]
    

    def get_star_count(self) -> int:
        """
        Retourne le nombre d'étoiles dans la grille.
        """
        return sum(1 for row in self.cells for cell in row if cell.is_occupied)