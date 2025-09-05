import tkinter as tk
import random
import time

class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake Game")
        self.geometry("800x800")
        self.resizable(False, False)

        self.width = 800
        self.height = 800
        self.cell_size = 20
        self.snake_direction = 'Right'
        self.snake = [(100, 100), (80, 100), (60, 100)]

        self.food = None
        self.food_type = 1
        self.place_food()

        self.running = True

        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(fill="both", expand=True)

        self.game_frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.game_frame, bg='black', width=self.width, height=self.height)
        self.start_time = time.time()
        self.start_game()

    def start_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.canvas.pack()
        self.setup_ui()
        self.run_game()

    def setup_ui(self):
        self.update_ui()
        self.bind("<KeyPress>", self.change_direction)

    def update_ui(self):
        self.canvas.delete('all')
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill='green')

        if self.food:
            color = 'red' if self.food_type == 1 else 'yellow'
            fx, fy = self.food
            self.canvas.create_oval(fx, fy, fx + self.cell_size, fy + self.cell_size, fill=color)
    # Show the food and the snake on the screen

    def run_game(self):
        if self.running:
            self.move_snake()
            self.after(100, self.run_game)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.snake_direction == 'Left':
            head_x -= self.cell_size
        elif self.snake_direction == 'Right':
            head_x += self.cell_size
        elif self.snake_direction == 'Up':
            head_y -= self.cell_size
        elif self.snake_direction == 'Down':
            head_y += self.cell_size

        new_head = (head_x, head_y)

        if not (0 <= head_x < self.width and 0 <= head_y < self.height):
            self.game_over()
            return
        
        if new_head in self.snake:
            self.game_over()
            return
        
        if len(self.snake) >= 8:
            self.game_over()
            return
    # Move the snake and judge whether the game is over
    
        self.snake = [new_head] + self.snake

        if self.food and new_head == self.food:
            growth = self.food_type
            for i in range(growth - 1):
                self.snake.append(self.snake[-1])
            self.place_food()
        else:
            self.snake.pop()

        self.update_ui()
    # Increase the length when the snake eat the food
    
    def change_direction(self, event):
        opposite_directions = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}
        if event.keysym in ['Left', 'Right', 'Up', 'Down']:
            # Check if the new direction is opposite to the current direction
            if event.keysym != opposite_directions[self.snake_direction]:
                self.snake_direction = event.keysym

    def game_over(self):
        self.canvas.create_text(
            self.width // 2, self.height // 2 - 30,
            text="Game Over", fill="red", font=("Arial", 40)
        )
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 30,
            text=f"Snake Length: {len(self.snake)}\nGame Time: {int(time.time()-self.start_time)} seconds",
            fill="white", font=("Arial", 20)
        )
        self.running = False
    # Show the gameover information, game time and length on the screen

    def place_food(self):
        while True:
            x = random.randint(0, (self.width - self.cell_size) // self.cell_size) * self.cell_size
            y = random.randint(0, (self.height - self.cell_size) // self.cell_size) * self.cell_size
            if (x, y) not in self.snake:
                self.food = (x, y)
                self.food_type = random.choice([1, 2])
                break
    # Randomly put either type of food on the screen


if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()