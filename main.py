import random
import time
import os
from rich.console import Console
import keyboard
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

SHAPES = {
    "I": [  # Line
        [(0, 0), (1, 0), (2, 0), (3, 0)],
    ] * 4,

    "O": [  # Square
        [(0, 0), (1, 0), (0, -1), (1, -1)],
    ] * 4,

    "T": [  # Small T
        [(1, 0), (0, 1), (1, 1), (2, 1)],
    ] * 4,
}


def has_spawn_space(shape_name, rotation, x_offset):
    shape_blocks = SHAPES[shape_name][rotation]
    for dx, dy in shape_blocks:
        gx = x_offset + dx
        gy = 0 + dy
        if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
            if grid[gy][gx] == "0":
                return False
    return True

class shape:
    def __init__(self):
        self.shape = random.choice(list(SHAPES.keys()))
        self.rotation = 0
        self.colour = random.choice(colours)
        self.static = False
        self.dead = False
        self.y = 0

        # Get shape width
        shape_blocks = SHAPES[self.shape][self.rotation]
        xs = [x for x, y in shape_blocks]
        min_x, max_x = min(xs), max(xs)
        shape_width = max_x - min_x + 1

        possible_positions = list(range(0, WIDTH - shape_width + 1))
        random.shuffle(possible_positions)

        global run
        for pos in possible_positions:
            if has_spawn_space(self.shape, self.rotation, pos):
                self.x = pos
            else:
                self.x = pos
                run = False
                break

    def draw_shape(self):
        val = "0" if self.static else "1"
        for dx, dy in SHAPES[self.shape][self.rotation]:
            gx, gy = self.x + dx, self.y + dy
            if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
                grid[gy][gx] = val
                colour_grid[gy][gx] = self.colour

    def clear_shape(self):
        for dx, dy in SHAPES[self.shape][self.rotation]:
            gx, gy = self.x + dx, self.y + dy
            if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
                grid[gy][gx] = " "

        return True

    def check_collision(self, dx=0, dy=0):
        for bx, by in SHAPES[self.shape][self.rotation]:
            nx = self.x + bx + dx
            ny = self.y + by + dy
            if nx < 0 or nx >= WIDTH or ny < 0 or ny >= HEIGHT:
                return True
            if grid[ny][nx] == "0":
                return True
            if ny >= HEIGHT:
                return False
        return False

    def check_vert_collision(self):
        return not self.check_collision(dy=1)

    def check_hori_collision(self, direction):
        return not self.check_collision(dx=direction)

    def gravity(self):
        if self.check_vert_collision():
            self.y += 1
            return True
        else:
            self.static = True
            self.draw_shape()
            if not self.dead:
                blocks.append(shape())
                self.dead = True
            return False

    def move(self,dx,dy):
        if not self.check_collision(dx,dy):
            self.clear_shape()
            self.x += dx
            self.y += dy
            self.draw_shape()

    def update(self):
        self.clear_shape()
        if frame % 2 == 0:
            self.gravity()
        self.draw_shape()
        if not self.static:
            if keyboard.is_pressed('right'):
                self.move(1, 0)
            if keyboard.is_pressed('left'):
                self.move(-1, 0)
            if keyboard.is_pressed('down'):
                self.move(0, 1)

# Main loop
blocks = [shape()]
draw_grid(grid, colour_grid)

run = True
frame = 0
while run:
    time.sleep(0.25)
    frame += 1
    for block in blocks:
        block.update()

    move_cursor_up(lines=len(grid) + 2)
    draw_grid(grid, colour_grid)

print_ascii("Game Over!")
