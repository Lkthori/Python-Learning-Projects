
import curses   #library to customize terminal
from curses import wrapper  #function to handle initialization and clean up automatically
import queue
import time

# ------------------- Define Maze -------------------
maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

start = "O"
end = "X"

# Function to print the maze
def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            if (row_idx, col_idx) in path:
                stdscr.addstr(row_idx, col_idx * 2, "X", RED)
            else:
                stdscr.addstr(row_idx, col_idx * 2, cell, BLUE)

# Function to find the starting position ("O") in the maze
def find_start(maze, start):
    for row_idx, row in enumerate(maze):
        for col_idx, cell in enumerate(row):
            if cell == start:
                return (row_idx, col_idx)
    return None

# Function to find valid neighboring positions (up, down, left, right)
def find_neighbors(maze, row, col):
    neighbors = []
    if row >= 0 and row < len(maze) - 1 and maze[row+1][col] != "#":
        neighbors.append((row +1 , col))
    if col >=0 and col < len(maze[0]) - 1 and maze[row][col + 1] != "#":
        neighbors.append((row, col + 1))

    return neighbors

# Function to find the shortest path from "O" to "X"
def find_path(maze,stdscr):
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))
    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()  # Clear the screen before drawing the maze
        print_maze(maze, stdscr, path)  # Print the maze with the current path
        # time.sleep(0.2)  # Pause for visualization
        stdscr.refresh()  # Refresh the screen to update the displayed maze

        if maze[row][col] == "X":  # If end is reached, return the path
            return path

        for neighbor in find_neighbors(maze, row, col):
            if neighbor not in visited:
                visited.add(neighbor)
                q.put((neighbor, path + [neighbor]))  # Add new position with updated path

# Main function to initialize the curses library and run the program
def main(stdscr):
    # Initialize color pairs (pair_number, foreground, background)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Blue text
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Red text

    find_path(maze, stdscr)
    stdscr.getch()  # Wait for a key press before closing

# Start program using the curses wrapper
wrapper(main)

