# Import necessary modules
try:
    from grid import Grid
    from ui import GameUI
except ImportError as e:
    print(f"Error importing modules: {e}")
    exit(1)

# Define the main function
def main():
    print("Initializing game...")  # Debugging print statement
    # Initialize the game grid
    try:
        grid = Grid()
        print("Grid initialized.")  # Debugging print statement
    except Exception as e:
        print(f"Error initializing grid: {e}")
        return

    # Initialize the game UI with the grid
    try:
        ui = GameUI(grid)
        print("UI initialized.")  # Debugging print statement
    except Exception as e:
        print(f"Error initializing UI: {e}")
        return

    # Start the game loop (handled by the UI main loop)
    try:
        ui.root.mainloop()
        print("Game loop started.")  # Debugging print statement
    except Exception as e:
        print(f"Error in game loop: {e}")

# Check if the script is being run directly
if __name__ == "__main__":
    print("Running main function...")  # Debugging print statement
    # Call the main function
    main()