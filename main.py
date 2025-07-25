import random
import time
import os
import keyboard

import config
import utils

os.system('')

WIDTH = config.WIDTH
HEIGHT = config.HEIGHT
grid = utils.create_grid(WIDTH, HEIGHT)
colour_grid = utils.create_grid(WIDTH, HEIGHT)

colours = config.COLOURS

SHAPES = config.SHAPES

DEBUG_MODE = config.DEBUG_MODE

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

        self.x = random.randint(1, WIDTH - shape_width)
        self.y = 0

        block_positions = utils.get_block_positions(self.shape, self.rotation, (self.x, self.y))
        global run
        for data in block_positions:
            x, y = data
            if grid[y][x] == "0":
                run = False
                break

    def draw(self):
        if DEBUG_MODE == 1:
            print("Function: draw")
        val = "0" if self.static else "1"
        for dx, dy in SHAPES[self.shape][self.rotation]:
            gx, gy = self.x + dx, self.y + dy
            if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
                grid[gy][gx] = val
                colour_grid[gy][gx] = self.colour

    def cement(self):
        for dx, dy in SHAPES[self.shape][self.rotation]:
            gx = self.x + dx
            gy = self.y + dy
            if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
                grid[gy][gx] = "0"
                colour_grid[gy][gx] = self.colour

    def clear_shape(self):
        if DEBUG_MODE == 1:
            print("Function: clear_shape")
        for dx, dy in SHAPES[self.shape][self.rotation]:
            gx, gy = self.x + dx, self.y + dy
            if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
                grid[gy][gx] = " "

        return True

    def check_collision(self, dx=0, dy=0, test_rotation=None):
        if DEBUG_MODE == 1:
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
        if DEBUG_MODE == 1:
            print("Function: gravity")
        if self.check_vert_collision():
            self.y += 1
            return
        else: # Landed
            if not self.static:
                self.static = True
                self.cement()
                return "static"
            global run
            if self.y == 0:
                run = False


    def rotate(self):
        if DEBUG_MODE == 1:
            print("Function: rotate")
        next_rotation = (self.rotation + 1) % len(SHAPES[self.shape])
        if not self.check_collision(test_rotation=next_rotation):
            self.clear_shape()
            self.rotation = next_rotation
            self.draw()

    def move(self,dx,dy):
        if DEBUG_MODE == 1:
            print("Function: move")
        if not self.check_collision(dx,dy):
            self.clear_shape()
            self.x += dx
            self.y += dy
            self.draw()

    def update(self):
        if DEBUG_MODE == 1:
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
side_text = [
    "",
    "",
    "",
    "",
    "",
    "",
    ""
]
blocks = [shape()]
grid_lines = utils.draw_grid(grid, colour_grid, scale=2)
utils.print_grid_with_side_text(grid_lines, side_text)

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
    grid = utils.clear_phantom(grid)
    utils.handle_clear(grid, colour_grid)

    if DEBUG_MODE == 2:
        side_text = ["".join(row) for row in grid]

    utils.move_cursor_up(lines=len(grid) + 2)
    grid_lines = utils.draw_grid(grid, colour_grid, scale=2)
    utils.print_grid_with_side_text(grid_lines, side_text)

    if keyboard.is_pressed('q'):
        run = False

utils.print_ascii("Game Over!")
