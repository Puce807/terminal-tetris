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
full_line = [i for i in range(WIDTH)]

colours = [
    "red",
    "bright_cyan",
    "bright_green",
    "yellow",
    "bright_magenta",
    "bright_blue",
]

SHAPES = {
    "I": [
        [(-2, 0), (-1, 0), (0, 0), (1, 0)],  # Horizontal
        [(0, -1), (0, 0), (0, 1), (0, 2)],   # Vertical
        [(-2, 1), (-1, 1), (0, 1), (1, 1)],  # Horizontal (offset)
        [(1, -1), (1, 0), (1, 1), (1, 2)]    # Vertical (offset)
    ],
    "O": [  # Square (only 1 rotation needed)
        [(0, 0), (1, 0), (0, 1), (1, 1)] * 4
    ],
    "T": [
        [(0, 0), (-1, 0), (1, 0), (0, 1)],   # Up
        [(0, 0), (0, -1), (0, 1), (1, 0)],   # Right
        [(0, 0), (-1, 0), (1, 0), (0, -1)],  # Down
        [(0, 0), (0, -1), (0, 1), (-1, 0)]   # Left
    ],
    "S": [
        [(0, 0), (1, 0), (0, 1), (-1, 1)],   # Horizontal
        [(0, 0), (0, -1), (1, 0), (1, 1)],   # Vertical
        [(0, 0), (1, 0), (0, 1), (-1, 1)],   # Horizontal (repeated)
        [(0, 0), (0, -1), (1, 0), (1, 1)]    # Vertical (repeated)
    ],
    "Z": [
        [(0, 0), (-1, 0), (0, 1), (1, 1)],   # Horizontal
        [(0, 0), (0, -1), (-1, 0), (-1, 1)], # Vertical
        [(0, 0), (-1, 0), (0, 1), (1, 1)],   # Horizontal (repeated)
        [(0, 0), (0, -1), (-1, 0), (-1, 1)]  # Vertical (repeated)
    ],
    "J": [
        [(0, 0), (-1, 0), (1, 0), (1, 1)],   # Up
        [(0, 0), (0, -1), (0, 1), (1, -1)],  # Right
        [(0, 0), (-1, 0), (1, 0), (-1, -1)], # Down
        [(0, 0), (0, -1), (0, 1), (-1, 1)]   # Left
    ],
    "L": [
        [(0, 0), (-1, 0), (1, 0), (-1, 1)],  # Up
        [(0, 0), (0, -1), (0, 1), (1, 1)],   # Right
        [(0, 0), (-1, 0), (1, 0), (1, -1)],  # Down
        [(0, 0), (0, -1), (0, 1), (-1, -1)]  # Left
    ]
}

debug = False

def clear_phantom():
    if grid[0][0] == "0":
        grid[0][0] = " "
    if grid[0][1] == "0":
        grid[0][1] = " "
    if grid[1][0] == "0":
        grid[1][0] = " "
    if grid[1][1] == "0":
        grid[1][1] = " "

def get_block_positions(shape_name, rotation, position):
    block_data = SHAPES[shape_name][rotation]
    x, y = position
    block_positions = []
    for data in block_data:
        dx, dy = data
        grid_x = x + dx
        grid_y = y + dy
        block_positions.append((grid_x, grid_y))
    return block_positions

class shape:
    def __init__(self):
        self.shape = random.choice(list(SHAPES.keys()))
        self.rotation = 0
        self.rotation_frame = 0
        self.colour = random.choice(colours)
        self.static = False
        self.dead = False

        # Get shape width
        shape_blocks = SHAPES[self.shape][self.rotation]
        xs = [x for x, y in shape_blocks]
        min_x, max_x = min(xs), max(xs)
        shape_width = max_x - min_x + 1

        self.x = random.randint(0, WIDTH - shape_width)
        self.y = 0

        block_positions = get_block_positions(self.shape, self.rotation, (self.x, self.y))
        global run
        for data in block_positions:
            x, y = data
            if grid[y][x] == "0":
                run = False
                break

    def draw(self):
        if debug:
            print("Function: draw")
        val = "0" if self.static else "1"
        for dx, dy in SHAPES[self.shape][self.rotation]:
            gx, gy = self.x + dx, self.y + dy
            if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
                grid[gy][gx] = val
                colour_grid[gy][gx] = self.colour

    def clear_shape(self):
        if debug:
            print("Function: clear_shape")
        for dx, dy in SHAPES[self.shape][self.rotation]:
            gx, gy = self.x + dx, self.y + dy
            if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
                grid[gy][gx] = " "

        return True

    def check_collision(self, dx=0, dy=0, test_rotation=None):
        if debug:
            print("Function: check_collision")
        shape_blocks = SHAPES[self.shape][test_rotation if test_rotation is not None else self.rotation]
        for x_offset, y_offset in shape_blocks:
            gx = self.x + dx + x_offset
            gy = self.y + dy + y_offset

            # Check if out of bounds
            if gx < 0 or gx >= WIDTH or gy >= HEIGHT:
                return True

            # Ignore negative gy (above the grid)
            if gy >= 0 and grid[gy][gx] == "0":
                return True

        return False

    def check_vert_collision(self):
        return not self.check_collision(dy=1)

    def check_hori_collision(self, direction):
        return not self.check_collision(dx=direction)

    def gravity(self):
        if debug:
            print("Function: gravity")
        if self.check_vert_collision():
            self.y += 1
            return
        else: # Landed
            if not self.static:
                self.static = True
                return "static"

    def rotate(self):
        if debug:
            print("Function: rotate")
        next_rotation = (self.rotation + 1) % len(SHAPES[self.shape])
        if not self.check_collision(test_rotation=next_rotation):
            self.clear_shape()
            self.rotation = next_rotation
            self.draw()

    def move(self,dx,dy):
        if debug:
            print("Function: move")
        if not self.check_collision(dx,dy):
            self.clear_shape()
            self.x += dx
            self.y += dy
            self.draw()

    def update(self):
        if debug:
            print("Function: update")
        self.clear_shape()
        if frame % 2 == 0:
            if self.gravity() == "static":
                return "static"
        self.draw()
        if not self.static:
            if keyboard.is_pressed('right'):
                self.move(1, 0)
            if keyboard.is_pressed('left'):
                self.move(-1, 0)
            if keyboard.is_pressed('down'):
                self.move(0, 1)
            if keyboard.is_pressed('r') or keyboard.is_pressed('up'):
                if frame > self.rotation_frame:
                    self.rotate()
                    self.rotation_frame = frame + 1

# Main loop
blocks = [shape()]
draw_grid(grid, colour_grid)

run = True
frame = 0
while run:
    time.sleep(0.25)
    frame += 1
    active_block = blocks[-1]
    if not active_block.static:
        if active_block.update() == "static":
            blocks.append(shape())
        else:
            active_block.draw()
    for block in blocks:
        if block != active_block and block.static:
            block.draw()
    clear_phantom()
    if debug:
        for i in range(HEIGHT):
            print(grid[i])

    move_cursor_up(lines=len(grid) + 2)
    draw_grid(grid, colour_grid)

print_ascii("Game Over!")
