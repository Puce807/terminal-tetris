import random
import time
import os
from rich.console import Console
from rich.style import Style
import pyfiglet

console = Console()
os.system('')  # Enable ANSI escape codes on Windows

def create_grid(width, height):
    c_grid = []
    for _ in range(height):
        row = [" "] * width
        c_grid.append(row)
    return c_grid

def draw_grid(grid, colour_grid, scale=2):
    width = len(grid[0])
    height = len(grid)

    def stretch(cell, x, y):
        colour = colour_grid[y][x]
        return (f"[{colour}]█[/{colour}]" * scale) if cell != " " else (" " * scale)

    print(f"┌{'─' * width * scale}┐")
    for y, row in enumerate(grid):
        stretched_row = ''.join(stretch(cell, x, y) for x, cell in enumerate(row))
        console.print(f"│{stretched_row}│")
    print(f"└{'─' * width * scale}┘")

def move_cursor_up(lines=1):
    print(f"\033[{lines}A", end='')

def print_ascii(text):
    ascii_text = pyfiglet.figlet_format(text, font="big")
    print(ascii_text)

WIDTH = 11
HEIGHT = 12
grid = create_grid(WIDTH, HEIGHT)
colour_grid = create_grid(WIDTH, HEIGHT)

colours = [
    "red",
    "bright_cyan",
    "bright_green",
    "yellow",
    "bright_magenta",
    "bright_blue",
]


class shape:
    def __init__(self):
        self.type = random.randint(0,1)
        self.color = random.randint(0,5)

        self.x = random.randint(0, WIDTH)
        self.y = 0

        self.static = False
        self.dead = False

        # Exit Bounds
        if self.type == 0:
            if self.x > WIDTH-4:
                self.x = WIDTH-4
        if self.type == 1:
            if self.x > WIDTH-2:
                self.x = WIDTH-2

    def draw_shape(self, x, y):
        if self.type == 0:
            grid[y][x : x + 4] = [("0" if self.static else "1")] * 4
            colour_grid[y][x : x + 4] = [colours[self.color]] * 4
        if self.type == 1:
            grid[y][x: x + 2] = [("0" if self.static else "1")] * 2
            grid[y-1][x: x + 2] = [("0" if self.static else "1")] * 2
            colour_grid[y][x: x + 2] = [colours[self.color]] * 2
            colour_grid[y-1][x: x + 2] = [colours[self.color]] * 2


    def clear_shape(self, x, y):
        if self.type == 0:
            grid[y][x: x + 4] = [" "] * 4
        if self.type == 1:
            grid[y][x: x + 2] = [" "] * 2
            grid[y-1][x: x + 2] = [" "] * 2

    def check_vert_collision(self):
        if self.type == 0:
            if self.y + 1 >= len(grid):
                return False
            for i in range(4):
                if self.x + i >= len(grid[0]):
                    return False
                if grid[self.y + 1][self.x + i] == "0":
                    return False
        if self.type == 1:
            if self.y + 1 >= len(grid):
                return False
            for i in range(2):
                if self.x + i >= len(grid[0]):
                    return False
                if grid[self.y + 1][self.x + i] == "0":
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
        elif self.type == 1:
            # Check lower row
            for i in range(2):
                nx = self.x + i + direction
                if nx < 0 or nx >= WIDTH:
                    return False
                if grid[self.y][nx] == "0":
                    return False
            # Check upper row (y - 1)
            if self.y - 1 >= 0:
                for i in range(2):
                    nx = self.x + i + direction
                    if nx < 0 or nx >= WIDTH:
                        return False
                    if grid[self.y - 1][nx] == "0":
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

draw_grid(grid,colour_grid)

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

    draw_grid(grid, colour_grid)

print_ascii("Game Over!")