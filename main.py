import random
import time
import os
from rich.console import Console
from rich.style import Style

os.system('')  # Enable ANSI escape codes on Windows

def create_grid(width, height):
    c_grid = []
    for _ in range(height):
        row = [" "] * width
        c_grid.append(row)
    return c_grid

def draw_grid(grid, scale=2):
    width = len(grid[0])
    height = len(grid)

    def stretch(cell):
        return ("█" * scale) if cell != " " else (" " * scale)

    print(f"┌{'─' * width * scale}┐")
    for row in grid:
        stretched_row = ''.join(stretch(cell) for cell in row)
        print(f"│{stretched_row}│")
    print(f"└{'─' * width * scale}┘")

def move_cursor_up(lines=1):
    print(f"\033[{lines}A", end='')

WIDTH = 11
HEIGHT = 12
grid = create_grid(WIDTH, HEIGHT)

colors = [
    "[red]",
    "[green]",
    "[yellow]",
    "[blue]",
    "[magenta]",
    "[cyan]"]

class shape:
    def __init__(self):
        self.type = 0
        self.color = random.randint(0,5)

        self.x = random.randint(0, WIDTH)
        self.y = 0

        self.static = False
        self.dead = False

        if self.type == 0:
            if self.x > WIDTH-4:
                self.x = WIDTH-4

    def draw_shape(self, x, y):
        if self.type == 0:
            if self.static:
                grid[y][x: x + 4] = ["0"] * 4
            else:
                grid[y][x: x + 4] = ["1"] * 4 # Moving

    def clear_shape(self, x, y):
        if self.type == 0:
            grid[y][x: x + 4] = [" "] * 4

    def check_vert_collision(self):
        if self.type == 0:
            if self.y + 1 >= len(grid):
                return False
            for i in range(4):
                try:
                    if grid[self.y + 1][self.x + i] == "0":
                        return False
                except IndexError:
                    return False
            return True

    def check_hori_collision(self, direction):
        if self.type == 0:
            for i in range(4):
                nx = self.x + i + direction
                if nx < 0 or nx >= WIDTH:
                    return False
                if grid[self.y][nx] == "0":
                    return False
        return True

    def gravity(self):
        if self.check_vert_collision():
            self.y += 1
            return True
        else:
            self.static = True
            self.draw_shape(self.x, self.y)  # Draw static blocks as '0'
            if not self.dead:
                blocks.append(shape())
                self.dead = True
            return False

    def update(self):
        self.clear_shape(self.x, self.y)  # Clear current position first
        if self.gravity():
            self.draw_shape(self.x, self.y)
        else:
            self.draw_shape(self.x, self.y)  # Draw at final position (static)


blocks = [shape()]

draw_grid(grid)

run = True
while run:
    time.sleep(0.5)
    for block in blocks:
        if not block.static:
            if not block.check_hori_collision(0):
                run = False
                break
        block.update()
    move_cursor_up(lines=len(grid) + 2)

    draw_grid(grid)

print("\nGame Over")