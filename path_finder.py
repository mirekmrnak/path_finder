# Path finder / Maze Navigator - Script to find the shortest way between points A to B
# Author: Miroslav Mrnak
# Inspired from 'Tech with Tim'

# pip install windows-curses
import curses
import queue
import time

maze = [
    ["#", "#", "#", "O", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#", "#", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", " ", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#", " ", "#", "#", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#", " ", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", "#", "#", " ", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#", "#", "#", " ", "#", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", "#", " ", " ", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", "#", " ", " ", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", "#", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", "#", " ", " ", " ", " ", "#", " ", " ", "#", " ", "#", " ", " ", "#"],
    ["#", " ", "#", "#", " ", " ", "#", "#", "#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", "#", "#", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

def print_maze(maze, stdscr, path=[], visited=set()):
    WHITE = curses.color_pair(1)
    BLUE = curses.color_pair(2)
    RED = curses.color_pair(3)
    YELLOW = curses.color_pair(4)
    POINT = curses.color_pair(5)

    # print legend
    stdscr.addstr(len(maze) + 2, 2, 'XX', POINT)
    stdscr.addstr(len(maze) + 2, 6, 'Start / End')
    stdscr.addstr(len(maze) + 4, 2, '  ', WHITE)
    stdscr.addstr(len(maze) + 4, 6, 'Way / Not Visited')
    stdscr.addstr(len(maze) + 6, 2, '  ', BLUE)
    stdscr.addstr(len(maze) + 6, 6, 'Obstacle')
    stdscr.addstr(len(maze) + 8, 2, '  ', YELLOW)
    stdscr.addstr(len(maze) + 8, 6, 'Visited')
    stdscr.addstr(len(maze) + 10, 2, '  ', RED)
    stdscr.addstr(len(maze) + 10, 6, 'Path')
    
    

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, 'X'*2, RED)
            elif (i, j) in visited:
                stdscr.addstr(i, j*2, value*2, YELLOW)
            elif maze[i][j] == '#':
                stdscr.addstr(i, j*2, value*2, BLUE)
            elif maze[i][j] == 'O' or maze[i][j] == 'X':
                stdscr.addstr(i, j*2, value*2, POINT)
            else:
                stdscr.addstr(i, j*2, value*2, WHITE)

def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i,j
    return None

def find_path(maze, stdscr):
    start = 'O'
    end = 'X'
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path, visited)
        stdscr.refresh()
        time.sleep(0.05)

        if maze[row][col] == end:
            return path
        
        neighbors = find_neighbors(maze, row, col)
        
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            
            r, c = neighbor
            if maze[r][c] == '#':
                continue
                
            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)
        
def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:
        neighbors.append((row-1, col))
    if row+1 < len(maze):
        neighbors.append((row+1, col))
    if col > 0:
        neighbors.append((row, col-1))
    if col+1 < len(maze[0]):
        neighbors.append((row, col+1))

    return neighbors

def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE) #white
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_CYAN) #blue
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_RED) #red
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_YELLOW) #yellow
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE) #start, end
    
    find_path(maze, stdscr)
    stdscr.getch()

curses.wrapper(main)