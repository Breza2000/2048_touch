import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
from grid import Grid

# Constants for styling the game over frame and label
FRAME_BORDER_WIDTH = 2  # Border width for the game over frame
LABEL_TEXT = "Game Over!"  # Text to display when the game is over
LABEL_BG = 'red'  # Background color for the game over label
LABEL_FG = 'white'  # Foreground (text) color for the game over label
LABEL_FONT = ("Helvetica", 24)  # Font style and size for the game over label

# Constants for the game board and cells
BOARD_BG = '#baada0'  # Background color for the game board
CELL_BG = '#ccc1b4'  # Background color for the cells
CELL_FONT = ("Helvetica", 32, "bold")  # Font style and size for the cell numbers

class GameUI:
    def __init__(self, grid):
        self.grid = grid
        self.root = tk.Tk()
        self.root.title("2048 Game")
        
        # Set the window to fullscreen and allow resizing
        self.root.attributes("-fullscreen", True)
        self.root.resizable(True, True)
        
        # Create the top frame for score and buttons
        self.top_frame = tk.Frame(self.root, bg=BOARD_BG, padx=3, pady=3)
        self.top_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Create the game board frame
        self.board = tk.Frame(self.root, bg=BOARD_BG, padx=3, pady=3)
        self.board.pack(expand=True, fill=tk.BOTH, pady=(10, 0))
        
        self.cells = []
        self.create_grid()
        self.create_score_board()
        self.create_menu()
        
        # Initialize the grid with two random tiles
        self.update_grid()
        
        self.root.bind("<Key>", self.key_handler)
        self.root.bind("<Button-1>", self.start_swipe)          # Bind mouse events for swipe functionality
        self.root.bind("<B1-Motion>", self.move_swipe)          # Bind mouse events for swipe functionality
        self.root.bind("<ButtonRelease-1>", self.end_swipe)     # Bind mouse events for swipe functionality
        
        self.swipe_start_x = 0      # Initialize the swipe start x-coorfinate
        self.swipe_start_y = 0      # Initialize the swipe start y-coorfinate
        
        self.root.mainloop()
    
    def start_swipe(self, event):
        """Record the starting coordinates of the swipe."""
        self.swipe_start_x = event.x
        self.swipe_start_y = event.y
    
    def move_swipe(self, event):
        """Handle the swipe movement (not used in this implementation)."""
        pass  # We don't need to handle this event for swiping
    
    def end_swipe(self, event):
        """Determine the direction of the swipe and move the tiles accordingly."""
        dx = event.x - self.swipe_start_x  # Calculate the horizontal distance swiped
        dy = event.y - self.swipe_start_y  # Calculate the vertical distance swiped
            
        # Determine if the swipe is more horizontal or vertical
        if abs(dx) > abs(dy):
            if dx > 0:
                self.grid.move('right')  # Swipe right
            else:
                self.grid.move('left')   # Swipe left
        else:
            if dy > 0:
                self.grid.move('down')  # Swipe down
            else:
                self.grid.move('up')    # Swipe up
            
        self.update_grid()  # Update the grid display after the move

    def game_over(self):
        """Display the game over message and end the game."""
        try:
            # Create and place the game over frame
            self.game_over_frame = tk.Frame(self.board, borderwidth=FRAME_BORDER_WIDTH, bg=LABEL_BG)
            self.game_over_frame.place(relx=0.5, rely=0.5, anchor="center")

            # Create and pack the game over label
            tk.Label(self.game_over_frame, text=LABEL_TEXT, bg=LABEL_BG, fg=LABEL_FG, font=LABEL_FONT).pack()

            # Unbind events to stop further user interaction
            self.root.unbind("<Key>")
            self.root.unbind("<Configure>")

            # Rebind the Escape key to exit the game
            self.root.bind("<Escape>", self.exit_game)
        except AttributeError:
            messagebox.showerror("Error", "An error occurred. Ensure that 'self.board' and 'self.root' are properly initialized.")

    def exit_game(self, event=None):
        """Exit the game."""
        self.root.destroy()

    def create_grid(self):
        """Create the grid of cells for the game board."""
        cell_size = 100  # Fixed size for the grid cells
        for i in range(self.grid.size):
            row = []
            for j in range(self.grid.size):
                cell = tk.Frame(self.board, bg=CELL_BG, width=cell_size, height=cell_size, padx=5, pady=5)
                cell.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                t = tk.Label(master=cell, text="", bg=CELL_BG, justify=tk.CENTER, font=CELL_FONT)
                t.pack(expand=True, fill=tk.BOTH)
                row.append(t)
            self.cells.append(row)
        
        # Make the grid cells expand to fill the available space
        for i in range(self.grid.size):
            self.board.grid_rowconfigure(i, weight=1)
            self.board.grid_columnconfigure(i, weight=1)

    def create_score_board(self):
        """Create the score board with current score, best score, and control buttons."""
        self.score_label = tk.Label(self.top_frame, text="Score: 0", font=("Helvetica", 24), bg=BOARD_BG)
        self.score_label.grid(row=0, column=0, padx=10)
        
        self.best_score_label = tk.Label(self.top_frame, text="Best Score: 0", font=("Helvetica", 24), bg=BOARD_BG)
        self.best_score_label.grid(row=0, column=1, padx=10)
        
        self.new_game_button = tk.Button(self.top_frame, text="New", command=self.new_game, font=("Helvetica", 14))
        self.new_game_button.grid(row=0, column=2, padx=10)
        
        self.save_game_button = tk.Button(self.top_frame, text="Save", command=self.save_game, font=("Helvetica", 14))
        self.save_game_button.grid(row=0, column=3, padx=10)
        
        self.load_game_button = tk.Button(self.top_frame, text="Load", command=self.load_game, font=("Helvetica", 14))
        self.load_game_button.grid(row=0, column=4, padx=10)
                
        self.load_game_button = tk.Button(self.top_frame, text="Exit", command=self.exit_game, font=("Helvetica", 14))
        self.load_game_button.grid(row=0, column=5, padx=10)

    def update_grid(self):
        """Update the grid display and score labels."""
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                value = self.grid.grid[i][j]
                if value == 0:
                    self.cells[i][j].configure(text="", bg=CELL_BG)
                else:
                    self.cells[i][j].configure(text=str(value), bg=self.get_color(value))
        self.score_label.configure(text=f"Score: {self.grid.score}")
        self.update_best_score()
        self.check_win()
        if not self.grid.can_move():
            self.game_over()

    def get_color(self, value):
        """Return the color associated with a specific tile value."""
        colors = {
            0: CELL_BG,
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
            4096: "#3c3a32",
            8192: "#3c3a32"
        }
        return colors.get(value, CELL_BG)

    def key_handler(self, event):
        """Handle key presses for moving tiles."""
        key = event.keysym
        if key == 'Up':
            self.grid.move('up')
        elif key == 'Down':
            self.grid.move('down')
        elif key == 'Left':
            self.grid.move('left')
        elif key == 'Right':
            self.grid.move('right')
        elif key == 'Escape':
            self.exit_game()

        self.update_grid()

    def create_menu(self):
        """Create the game menu."""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_command(label="Save Game", command=self.save_game)
        file_menu.add_command(label="Load Game", command=self.load_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_game)

    def save_game(self):
        """Save the current game state to a file."""
        # Prompt the user to enter a save name
        save_name = simpledialog.askstring("Save Game", "Enter save name:")
        if save_name:
            # Prepare the data to be saved
            save_data = {
                'grid': self.grid.grid,
                'size': self.grid.size,
                'score': self.grid.score
            }
            # Create the saves directory if it doesn't exist
            if not os.path.exists('saves'):
                os.makedirs('saves')
            # Save the game data to a JSON file
            with open(f"saves/{save_name}.json", 'w') as save_file:
                json.dump(save_data, save_file)
            # Inform the user that the game was saved successfully
            messagebox.showinfo("Save Game", "Game saved successfully!")

    def load_game(self):
        """Load a saved game state from a file."""
        # Prompt the user to enter the name of the save file to load
        load_name = simpledialog.askstring("Load Game", "Enter save name:")
        if load_name is None:
            # User hit cancel, do nothing
            return
        if load_name and os.path.exists(f"saves/{load_name}.json"):
            # Load the game data from the JSON file
            with open(f"saves/{load_name}.json", 'r') as load_file:
                save_data = json.load(load_file)
                self.grid.grid = save_data['grid']
                self.grid.size = save_data['size']
                self.grid.score = save_data['score']
                self.update_grid()
                # Inform the user that the game was loaded successfully
                messagebox.showinfo("Load Game", "Game loaded successfully!")
        else:
            # Show an error message if the save file was not found
            messagebox.showerror("Load Game", "Save file not found!")

    def get_saved_games(self):
        """Return a list of saved games."""
        # Check if the saves directory exists
        if not os.path.exists('saves'):
            return []
        # Return a list of save file names without the .json extension
        return [f.split('.')[0] for f in os.listdir('saves') if f.endswith('.json')]
            
    def new_game(self):
        """Start a new game."""
        # Destroy the game over frame if it exists
        if hasattr(self, 'game_over_frame') and self.game_over_frame:
            self.game_over_frame.destroy()
            self.game_over_frame = None

        self.grid = Grid()
        self.update_grid()

    def update_best_score(self):
        """Update the best score display."""
        best_score = 0
        if os.path.exists('saves/best_score.json'):
            with open('saves/best_score.json', 'r') as best_file:
                best_score = json.load(best_file).get('best_score', 0)
        if self.grid.score > best_score:
            best_score = self.grid.score
            with open('saves/best_score.json', 'w') as best_file:
                json.dump({'best_score': best_score}, best_file)
            self.display_temporary_message("New Record!")
        self.best_score_label.configure(text=f"Best Score: {best_score}")

    def check_win(self):
        """Check if the player has won the game."""
        for row in self.grid.grid:
            if 2048 in row:
                self.display_temporary_message("You Won!")
                break

    def display_temporary_message(self, message):
        """Display a temporary message on the screen."""
        message_label = tk.Label(self.board, text=message, bg=LABEL_BG, fg=LABEL_FG, font=("Helvetica", 24))
        message_label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.after(2000, message_label.destroy)  # Remove the message after 2 seconds

if __name__ == "__main__":
    grid = Grid()
    GameUI(grid)