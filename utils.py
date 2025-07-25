import pyfiglet
import math
import time
from rich.text import Text

import config

console = config.CONSOLE

WIDTH = config.WIDTH
HEIGHT = config.HEIGHT

def clear_phantom(grid):
    if grid[0][0] == "0":
        grid[0][0] = " "
    if grid[0][1] == "0":
        grid[0][1] = " "
    if grid[1][0] == "0":
        grid[1][0] = " "
    if grid[1][1] == "0":
        grid[1][1] = " "
    if grid[0][2] == "0":
        grid[0][2] = " "
    return grid

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

    # Build and return the grid lines
    lines = [f"┌{'─' * width * scale}┐"]
    for y, row in enumerate(grid):
        stretched_row = ''.join(stretch(cell, x, y) for x, cell in enumerate(row))
        lines.append(f"│{stretched_row}│")
    lines.append(f"└{'─' * width * scale}┘")
    return lines

def print_grid_with_side_text(grid_lines, side_text_lines=None, side_style=None):
    for i in range(len(grid_lines)):
        grid_line = grid_lines[i]
        style = side_style[i] if side_style and i < len(side_style) else ""
        side_line = Text(side_text_lines[i] if side_text_lines and i < len(side_text_lines) else "", style=style)
        console.print(f"{''.join(grid_line)} {side_line}")

def move_cursor_up(lines=1):
    print(f"\033[{lines}A", end='')

def print_ascii(text):
    ascii_text = pyfiglet.figlet_format(text, font="big")
    print(ascii_text)

def handle_clear(grid, colour_grid):
    full_line = ["0" for i in range(WIDTH)]
    cleared = False
    for y in range(HEIGHT - 1, -1, -1):  # Start from bottom row
        if grid[y] == full_line:
            # Clear the row
            del grid[y]
            grid.insert(0, [" " for _ in range(WIDTH)])
            del colour_grid[y]
            colour_grid.insert(0, ["white" for _ in range(WIDTH)])
            cleared = True
    return cleared

def get_block_positions(shape_name, rotation, position):
    block_data = config.SHAPES[shape_name][rotation]
    x, y = position
    block_positions = []
    for data in block_data:
        dx, dy = data
        grid_x = x + dx
        grid_y = y + dy
        block_positions.append((grid_x, grid_y))
    return block_positions

def handle_level(line_clears):
    level = math.floor(line_clears/5)
    return level

def get_mini_display(shape_name, rotation=0):
    coords = config.SHAPES[shape_name][rotation]

    min_x = min(x for x, y in coords)
    min_y = min(y for x, y in coords)

    grid = [[" " for _ in range(16)] for _ in range(2)]

    for x, y in coords:
        new_x = (x - min_x + 2) * 2
        new_y = y - min_y
        if 0 <= new_x < 15 and 0 <= new_y < 2:
            grid[new_y][new_x] = "█"
            grid[new_y][new_x + 1] = "█"

    return ["".join(row) for row in grid]

