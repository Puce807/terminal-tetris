# Only change this file if you know what you are doing!

from rich.console import Console

CONSOLE = Console()

WIDTH = 12
HEIGHT = 15

DEBUG_MODE = 0

CLEAR_POINTS = 40

COLOURS = [
    "red",
    "bright_cyan",
    "bright_green",
    "yellow",
    "bright_magenta",
    "bright_blue",
    "blue1",
    "purple"
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