import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class SlidingPuzzle:
    def __init__(self, root):
        # Initialize the main game window and core game parameters
        self.root = root
        self.root.title("Sliding Puzzle")
        
        # Game configuration: 3x3 grid, each cell 100 pixels, initial moves zero
        self.size = 3
        self.cell_size = 100
        self.moves = 0
        
        # Load image tiles for the puzzle
        self.load_image("Sliding_Puzzle\puzzle_image.png")
        
        # Set initial empty cell to bottom-right corner
        self.empty_cell = (self.size - 1, self.size - 1)
        
        # Create the initial puzzle state with sequential numbered tiles
        self.current_state = self.create_initial_state()
        
        # Create GUI elements like grid, move counter, and new game button
        self.create_widgets()
        
        # Bind keyboard events for arrow key controls
        self.root.bind("<Key>", self.handle_keyboard)
        
        # Shuffle the board and reset moves to zero
        self.shuffle_board()
        self.moves = 0
        self.move_label.config(text="Moves: 0")
        self.update_board()

    def load_image(self, image_path):
        # Attempt to load and split an image into puzzle tiles
        try:
            # Open and resize the input image to fit the puzzle grid
            image = Image.open(image_path)
            image = image.resize((self.cell_size * self.size, self.cell_size * self.size))
            
            # Container to store image tiles
            self.tiles = []
            
            # Crop the image into individual tiles
            for row in range(self.size):
                for col in range(self.size):
                    # Calculate the bounding box for each tile
                    box = (col * self.cell_size, row * self.cell_size, 
                          (col + 1) * self.cell_size, (row + 1) * self.cell_size)
                    tile = image.crop(box)
                    
                    # Add all tiles except the last one (which will be the empty tile)
                    if row != self.size - 1 or col != self.size - 1:
                        self.tiles.append(ImageTk.PhotoImage(tile))
            
            # Create a white empty tile for the last position
            empty_tile = Image.new('RGB', (self.cell_size, self.cell_size), 'white')
            self.tiles.append(ImageTk.PhotoImage(empty_tile))
            
        # Fallback to colored tiles if image loading fails
        except FileNotFoundError:
            self.tiles = []
            colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'white']
            for color in colors:
                # Create solid color tiles as a backup
                img = Image.new('RGB', (self.cell_size, self.cell_size), color)
                self.tiles.append(ImageTk.PhotoImage(img))

    def create_initial_state(self):
        # Generate the solved state of the puzzle
        # Creates a 2D list with sequential numbers representing tile positions
        return [[i * self.size + j for j in range(self.size)] 
                for i in range(self.size)]

    def create_widgets(self):
        # Set up the game's graphical user interface
        # Create a frame to hold the puzzle grid
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)
        
        # Create a 2D list of labels to represent puzzle tiles
        self.buttons = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                # Create a label for each tile with border and click event
                button = tk.Label(self.frame, borderwidth=1, relief="solid")
                button.grid(row=i, column=j, padx=1, pady=1)
                button.bind("<Button-1>", lambda e, row=i, col=j: self.handle_click(row, col))
                row.append(button)
            self.buttons.append(row)
        
        # Create a label to display move count
        self.move_label = tk.Label(self.root, text="Moves: 0")
        self.move_label.pack(pady=5)
        
        # Create a button to start a new game
        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.pack(pady=5)

    def shuffle_board(self):
        # Randomize the puzzle board by making 1000 random valid moves
        moves = 1000
        for _ in range(moves):
            # Get list of possible moves around the empty cell
            possible_moves = self.get_possible_moves()
            # Choose and execute a random move without updating GUI
            move = random.choice(possible_moves)
            self.make_move(move[0], move[1], update_gui=False, count_move=False)

    def get_possible_moves(self):
        # Determine valid moves based on the current empty cell position
        moves = []
        empty_row, empty_col = self.empty_cell
        
        # Check adjacent cells in four directions: right, down, left, up
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = empty_row + dr, empty_col + dc
            # Ensure the move is within the puzzle grid
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                moves.append((new_row, new_col))
        return moves

    def make_move(self, row, col, update_gui=True, count_move=True):
        # Execute a tile move if the selected cell is a valid move
        if (row, col) in self.get_possible_moves():
            # Get current empty cell position
            empty_row, empty_col = self.empty_cell
            
            # Swap the clicked tile with the empty cell
            self.current_state[empty_row][empty_col] = self.current_state[row][col]
            self.current_state[row][col] = self.size * self.size - 1
            self.empty_cell = (row, col)
            
            # Increment move counter if it's a player move
            if count_move:
                self.moves += 1
                self.move_label.config(text=f"Moves: {self.moves}")
            
            # Update the board and check for win condition
            if update_gui:
                self.update_board()
                if self.check_win():
                    messagebox.showinfo("Congratulations!", 
                                      f"You solved the puzzle in {self.moves} moves!")

    def handle_click(self, row, col):
        # Handle mouse click events on puzzle tiles
        self.make_move(row, col)

    def handle_keyboard(self, event):
        # Handle keyboard arrow key events for moving tiles
        empty_row, empty_col = self.empty_cell
        
        # Determine move based on arrow key pressed
        if event.keysym == "Up" and empty_row < self.size - 1:
            self.make_move(empty_row + 1, empty_col)
        elif event.keysym == "Down" and empty_row > 0:
            self.make_move(empty_row - 1, empty_col)
        elif event.keysym == "Left" and empty_col < self.size - 1:
            self.make_move(empty_row, empty_col + 1)
        elif event.keysym == "Right" and empty_col > 0:
            self.make_move(empty_row, empty_col - 1)

    def update_board(self):
        # Refresh the GUI to reflect the current puzzle state
        for i in range(self.size):
            for j in range(self.size):
                value = self.current_state[i][j]
                # Display either the tile image or the empty white tile
                if value == self.size * self.size - 1:
                    self.buttons[i][j].config(image=self.tiles[-1])
                else:
                    self.buttons[i][j].config(image=self.tiles[value])

    def check_win(self):
        # Check if puzzle is solved by comparing current state with goal state
        goal_state = self.create_initial_state()
        return self.current_state == goal_state

    def new_game(self):
        # Reset the game to initial conditions
        self.moves = 0
        self.move_label.config(text="Moves: 0")
        self.empty_cell = (self.size - 1, self.size - 1)
        self.current_state = self.create_initial_state()
        self.shuffle_board()
        self.update_board()

if __name__ == "__main__":
    # Create the main game window and start the game
    root = tk.Tk()
    game = SlidingPuzzle(root)
    root.mainloop()
