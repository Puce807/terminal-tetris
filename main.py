def create_grid(width,height):
    c_grid = []
    for _ in range(height):
        row = [" "] * width
        c_grid.append(row)
    c_grid[2][0] = "■"
    for i in range(len(c_grid)):
        print(c_grid[i])
    return c_grid

def draw_grid(grid, scale=2):
    width = len(grid[0])
    height = len(grid)

    def stretch(cell): return cell * scale

    print(f"┌{'─' * width * scale}┐")
    for row in grid:
        stretched_row = ''.join(stretch(cell) for cell in row)
        print(f"│{stretched_row}│")
    print(f"└{'─' * width * scale}┘")

grid = create_grid(10, 10)
draw_grid(grid)