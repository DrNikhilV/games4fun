import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class SlidingPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle")
        
        self.size = 3
        self.cell_size = 100
        self.moves = 0
        
        self.load_image("puzzle_image.png")
        
        self.empty_cell = (self.size - 1, self.size - 1)
        self.current_state = self.create_initial_state()
        
        self.create_widgets()
        
        self.root.bind("<Key>", self.handle_keyboard)
        
        self.shuffle_board()
        self.moves = 0  # Reset moves after shuffling
        self.move_label.config(text="Moves: 0")  # Update display
        self.update_board()

    def load_image(self, image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((self.cell_size * self.size, self.cell_size * self.size))
            
            self.tiles = []
            for row in range(self.size):
                for col in range(self.size):
                    box = (col * self.cell_size, row * self.cell_size, 
                          (col + 1) * self.cell_size, (row + 1) * self.cell_size)
                    tile = image.crop(box)
                    if row != self.size - 1 or col != self.size - 1:
                        self.tiles.append(ImageTk.PhotoImage(tile))
            
            empty_tile = Image.new('RGB', (self.cell_size, self.cell_size), 'white')
            self.tiles.append(ImageTk.PhotoImage(empty_tile))
            
        except FileNotFoundError:
            self.tiles = []
            colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'white']
            for color in colors:
                img = Image.new('RGB', (self.cell_size, self.cell_size), color)
                self.tiles.append(ImageTk.PhotoImage(img))

    def create_initial_state(self):
        return [[i * self.size + j for j in range(self.size)] 
                for i in range(self.size)]

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)
        
        self.buttons = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Label(self.frame, borderwidth=1, relief="solid")
                button.grid(row=i, column=j, padx=1, pady=1)
                button.bind("<Button-1>", lambda e, row=i, col=j: self.handle_click(row, col))
                row.append(button)
            self.buttons.append(row)
        
        self.move_label = tk.Label(self.root, text="Moves: 0")
        self.move_label.pack(pady=5)
        
        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
        self.new_game_button.pack(pady=5)

    def shuffle_board(self):
        moves = 1000
        for _ in range(moves):
            possible_moves = self.get_possible_moves()
            move = random.choice(possible_moves)
            self.make_move(move[0], move[1], update_gui=False, count_move=False)  # Don't count shuffling moves

    def get_possible_moves(self):
        moves = []
        empty_row, empty_col = self.empty_cell
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                moves.append((new_row, new_col))
        return moves

    def make_move(self, row, col, update_gui=True, count_move=True):
        if (row, col) in self.get_possible_moves():
            empty_row, empty_col = self.empty_cell
            self.current_state[empty_row][empty_col] = self.current_state[row][col]
            self.current_state[row][col] = self.size * self.size - 1
            self.empty_cell = (row, col)
            
            if count_move:  # Only increment moves for player actions
                self.moves += 1
                self.move_label.config(text=f"Moves: {self.moves}")
            
            if update_gui:
                self.update_board()
                if self.check_win():
                    messagebox.showinfo("Congratulations!", 
                                      f"You solved the puzzle in {self.moves} moves!")

    def handle_click(self, row, col):
        self.make_move(row, col)

    def handle_keyboard(self, event):
        empty_row, empty_col = self.empty_cell
        if event.keysym == "Up" and empty_row < self.size - 1:
            self.make_move(empty_row + 1, empty_col)
        elif event.keysym == "Down" and empty_row > 0:
            self.make_move(empty_row - 1, empty_col)
        elif event.keysym == "Left" and empty_col < self.size - 1:
            self.make_move(empty_row, empty_col + 1)
        elif event.keysym == "Right" and empty_col > 0:
            self.make_move(empty_row, empty_col - 1)

    def update_board(self):
        for i in range(self.size):
            for j in range(self.size):
                value = self.current_state[i][j]
                if value == self.size * self.size - 1:
                    self.buttons[i][j].config(image=self.tiles[-1])
                else:
                    self.buttons[i][j].config(image=self.tiles[value])

    def check_win(self):
        goal_state = self.create_initial_state()
        return self.current_state == goal_state

    def new_game(self):
        self.moves = 0
        self.move_label.config(text="Moves: 0")
        self.empty_cell = (self.size - 1, self.size - 1)
        self.current_state = self.create_initial_state()
        self.shuffle_board()
        self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = SlidingPuzzle(root)
    root.mainloop()
