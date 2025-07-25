# Terminal Tetris in Python

A classic **Tetris** game playable directly in your terminal, built with **Python**!

---

## 🚀 Features
- 🧱 Classic Tetris Gameplay
 Drop, move, and rotate falling blocks to clear lines and score points.

- ⌨️ Simple Keyboard Controls
Intuitive keys for movement and rotation (customizable if needed).

- 🖥️ Runs in the Terminal
No GUI needed — enjoy Tetris directly in your command line!

- 🌈 Colourful Blocks
Uses the rich library for vibrant, colourful shapes and grid.

- 🔁 Smooth Game Loop
Real-time piece dropping with speed control and collision detection.

- 📦 Lightweight & Portable
Just one Python file with minimal dependencies — easy to run anywhere.

---

## 🛠️ Setup & Installation
> ## ❗ - DISCLAIMER:
> Your IDE terminal may not support cursor manipulation or Rich text formatting. For best results, please use **Command Prompt** or any standard terminal emulator (such as `bash`, `zsh`, `PowerShell`, or your system's default terminal on macOS/Linux). Personally, I prefer the look of terminal tetris in Command Prompt. Only use your IDE if you are debugging or testing! Thank you!

1. Clone this repository:
```bash
git clone https://github.com/Puce807/terminal-tetris
cd <WHEREVER YOU HAVE YOUR FOLDER>
```

2. Install required packages: _rich, pyfiglet, keyboard_
```bash
pip install -r requirements.txt
```

3. Run the game!
```bash
python main.py
```

---

## 🎮 How to Play

- **Start the Game:** Run `python main.py` in your terminal.
- **Controls:**
  - **Left Arrow (`←`)** – Move the current piece left
  - **Right Arrow (`→`)** – Move the current piece right
  - **Down Arrow (`↓`)** – Move the current piece down faster
  - **Up Arrow (`↑`)** – Rotate the current piece
  - **Q** – Quit the game
- **Objective:** Arrange the falling pieces to complete horizontal lines. Completed lines will clear, giving you points and making room for more pieces. The game ends if the stack of pieces reaches the top of the grid.

Enjoy playing Tetris!

---

## 📦 Project Structure
```bash
terminal_tetris/
├── main.py           # Main game loop and logic
├── requirements.txt  # File containing all requirements
└── README.md         # This file
