def print_grid(grid):
    if not all(isinstance(row, list) for row in grid):
        raise ValueError("Grid must be a list of lists")
    for row in grid:
        print('\t'.join(map(str, row)))
    print()

# Example usage
if __name__ == "__main__":
    example_grid = [
        [2, 0, 0, 2],
        [4, 4, 2, 2],
        [0, 0, 0, 0],
        [2, 2, 2, 2]
    ]
    print_grid(example_grid)