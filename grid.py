import random

class Grid:
    def __init__(self, size=4):
        """
        Initialize the grid for the 2048 game.

        Parameters:
        size (int): The size of the grid (default is 4).
        """
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        """Add a new tile (2 or 4) to a random empty cell in the grid."""
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice([2, 4])

    def can_move(self):
        """Check if any moves are possible."""
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return True
                if i < self.size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return True
                if j < self.size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return True
        return False

    def move(self, direction):
        """Move tiles in the specified direction."""
        def move_row_left(row):
            new_row = [i for i in row if i != 0]
            for i in range(len(new_row) - 1):
                if new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    self.score += new_row[i]
                    new_row[i + 1] = 0
            new_row = [i for i in new_row if i != 0]
            return new_row + [0] * (self.size - len(new_row))

        moves = {
            'left': lambda grid: [move_row_left(row) for row in grid],
            'right': lambda grid: [move_row_left(row[::-1])[::-1] for row in grid],
            'up': lambda grid: list(map(list, zip(*[move_row_left(row) for row in zip(*grid)]))),
            'down': lambda grid: list(map(list, zip(*[move_row_left(row[::-1])[::-1] for row in zip(*grid)])))
        }

        if direction in moves:
            self.grid = moves[direction](self.grid)
            self.add_new_tile()