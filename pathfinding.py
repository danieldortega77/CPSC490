import pygame as pg
from pygame.color import THECOLORS as colors
from pygame.display import toggle_fullscreen
from pygame.draw import *

from enum import IntEnum
from datetime import datetime
from random import random, randrange, choice
import json
import pyOSC3
from tkinter import *
from tkinter import filedialog

pg.init()
pg.mixer.init()

############################################ PROGRAM VARIABLES ################################################

# Set up OSC client
client = pyOSC3.OSCClient()
client.connect( ( '127.0.0.1', 57120 ) )
clock = pg.time.Clock()

# Flags
running = True
run_speed = 7
mouse_down = False
to_restart = False

# Circle of fifths
# Use these for "fifths" save files
# pitches = ["F", "C", "G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
# pitches = ["F", "C", "G", "D", "A", "E", "B"]

# Chromatic
# pitches = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Diatonic
# Use this for "chords" and "diagonal" save files
pitches = ["C", "D", "E", "F", "G", "A", "B"]

class DrawMode(IntEnum):
    none = 0
    wall_place = 1
    wall_remove = 2
    start_move = 3
    finish_move = 4
    select = 5
    deselect = 6

draw_mode = DrawMode.none

# Set up screen
dim = 800
n_tiles = 30
tile_size = dim // n_tiles
bg_color = colors['lightblue']

screen = pg.display.set_mode((dim * 1.5, dim))
pg.display.set_caption('Pathfinding')

fontBig = pg.font.Font('freesansbold.ttf', 24)
fontMedium = pg.font.Font('freesansbold.ttf', 20)
fontSmall = pg.font.Font('freesansbold.ttf', 14)

def createText(text, center, font):
    render = font.render(text, True, colors['black'])
    rect = render.get_rect(center=center)
    return render, rect

def createTextList(text_list, center, font):
    renders = [None for _ in range(len(text_list))]
    rects = [None for _ in range(len(text_list))]
    for i, text in enumerate(text_list):
        renders[i], rects[i] = createText(text, center, font)
    return renders, rects

# Create text for current algorithm
algLabel, algLabelRect = createText('Current Algorithm:', (dim * 1.25, dim/8), fontBig)
algNames = ['A Star', 'Dijkstra', 'Greedy Best First Search', 'Depth First Search', 'Breadth First Search']
algRenders, algRects = createTextList(algNames, (dim * 1.25, dim/4), fontMedium)

# Create text for current draw mode
drawModeLabel, drawModeLabelRect = createText('Current Draw Mode:', (dim * 1.25, 3 * dim/8), fontBig)
drawModes = ['None', 'Place Walls', 'Erase Walls', 'Place Start', 'Place Finish', 'Select', 'Deselect']
drawModeRenders, drawModeRects = createTextList(drawModes, (dim * 1.25, dim/2), fontMedium)

##################################################################################################

class NodeState(IntEnum):
    start = 0
    finish = 1
    wall = 2
    moveable = 3

class Node:
    def __init__(self, i, j, state=NodeState.moveable):
        # for a*
        self.f = 0
        self.g = 0
        self.h = 0

        self.pos = i, j
        self.state = state
        self.visited = False
        self.timeSinceVisited = 0
        self.parent = None
        self.selected = False

        # Fully random pitch assignment
        # self.pitch = pitches[int(random() * len(pitches))]
        # self.pitch = choice(pitches)

        # Assign pitch by column
        # self.pitch = i % len(pitches)

        # Construct chords in the grid
        chord = ((i//6) + (j//6)) % len(pitches)
        self.pitch = (chord + (i % 3) * 2) % len(pitches)

        # Add rows and columns of walls
        # if i % 6 == 5 or j % 6 == 5:

        # Add completely random walls
        if random() < 0.2:
            self.state = NodeState.wall

        self.in_path = False

    def draw(self, screen):
        rect_color = colors['white']

        # Color the node correctly according to its state
        if self.state == NodeState.start:
            rect_color = colors['lightgreen']
        elif self.state == NodeState.finish:
            rect_color = colors['coral']
        elif self.in_path:
            rect_color = colors['yellow']
        elif self.visited:
            if self.timeSinceVisited == 1:
                rect_color = colors['lightpink']
            elif self.timeSinceVisited == 2:
                rect_color = colors['lightpink1']
            elif self.timeSinceVisited == 3:
                rect_color = colors['lightpink2']
            elif self.timeSinceVisited == 4:
                rect_color = colors['lightpink3']
            else:
                rect_color = colors['lightpink4']
        elif self.state == NodeState.wall:
            rect_color = colors['black']
        elif self.selected:
            rect_color = colors['lightblue1']

        # Render white square for node
        rect(screen, rect_color, (self.pos[0] * tile_size,
                                  self.pos[1] * tile_size, tile_size, tile_size))

        # Render node border
        rect(screen, bg_color, (self.pos[0] * tile_size,
                                self.pos[1] * tile_size, tile_size, tile_size), 2)
        
        # Render text
        if self.state == NodeState.moveable:
            pitchRender = fontSmall.render(pitches[self.pitch], True, colors['black'])
            pitch_rect = pitchRender.get_rect(center=((self.pos[0] + 0.5) * tile_size, (self.pos[1] + 0.5) * tile_size))
            screen.blit(pitchRender, pitch_rect)
        
        if self.visited:
            self.timeSinceVisited += 1


    def get_neighbours(self, grid):
        nb = []
        if self.state == NodeState.wall:
            return nb

        arr = [
            [-1, 0],
            [1, 0],
            [0, 1],
            [0, -1],
        ]

        for _, pos in enumerate(arr):
            i = self.pos[0] + pos[0]
            j = self.pos[1] + pos[1]

            if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                t = grid[i][j]
                if t.state != NodeState.wall and not t.visited:
                    t.parent = self

                    nb.append(t)

        return nb

#################################################### ALGORITHM FUNCTIONS #################################################################


def make_path(node):
    for i in grid:
        for j in i:
            j.in_path = False

    n = node
    while True:
        if n is None: break

        n.in_path = True
        n = n.parent


def play_music(pitch):
    msg = pyOSC3.OSCMessage()
    msg.setAddress("/pathfinding")
    msg.append(pitches[pitch])
    client.send(msg)

#################################################### ALGORITHMS #################################################################


def bfs():
    node = queue.pop(0)

    if not node.visited:
        queue.extend(node.get_neighbours(grid))

    return node


def dfs():
    node = queue.pop()

    if not node.visited:
        queue.extend(node.get_neighbours(grid))

    return node


def best_search_heuristic(n, end):
    return pow(pow(n.pos[0] - end.pos[0], 2) + pow(n.pos[1] - end.pos[1], 2), .5)
    # return abs(n.pos[0] - end.pos[0]) + abs(n.pos[1] - end.pos[1])
    # return max(abs(n.pos[0] - end.pos[0]), abs(n.pos[1] - end.pos[1]))


def greedy_bfs():
    winner = 0
    for i in range(len(queue)):
        if (queue[i].h < queue[winner].h):
            winner = i

    node = queue.pop(winner)

    if not node.visited:
        for n in node.get_neighbours(grid):
            if n.visited:
                continue

            n.h = best_search_heuristic(n, finish_node)
            queue.append(n)

    return node


def a_star():
    winner = 0
    for i in range(len(queue)):
        if (queue[i].f < queue[winner].f):
            winner = i

    node = queue.pop(winner)

    if not node.visited:
        for n in node.get_neighbours(grid):
            if n.visited:
                continue

            temp_g = node.g + 1
            new_path = False

            if n in queue:
                if temp_g < n.g:
                    n.g = temp_g
                    new_path = True
            else:
                n.g = temp_g
                new_path = True
                queue.append(n)

            if new_path:
                n.h = best_search_heuristic(n, finish_node)
                n.f = n.g + n.h

    return node


def dijkstra():
    winner = 0
    for i in range(len(queue)):
        if (queue[i].g < queue[winner].g):
            winner = i

    node = queue.pop(winner)
    play_music(node.pitch)

    if not node.visited:
        for n in node.get_neighbours(grid):
            if n.visited:
                continue

            temp_g = node.g + 1

            if n in queue:
                if temp_g < n.g:
                    n.g = temp_g
            else:
                n.g = temp_g
                queue.append(n)

    return node

algSymbols = [a_star, dijkstra, greedy_bfs, dfs, bfs]

################################################### ALGORITHM VARIABLES #########################################################

order = 0

(grid,
start_node,
finish_node,
selected_node,
queue,
algorithm,
simul_running) = [None for _ in range(7)]

def load_grid(data):
    global grid, start_node, finish_node, selected_node, queue, algorithm, simul_running, order, to_restart

    simul_running = False

    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            nodeDict = data[i][j]
            node.f = nodeDict["f"]
            node.g = nodeDict["g"]
            node.h = nodeDict["h"]
            node.visited = nodeDict["visited"]
            node.timeSinceVisited = nodeDict["timeSinceVisited"]
            node.parent = nodeDict["parent"]
            node.in_path = nodeDict["in_path"]
            node.state = nodeDict["state"]
            node.pitch = nodeDict["pitch"]

            if node.state == NodeState.start:
                start_node = node
            elif node.state == NodeState.finish:
                finish_node = node

    queue = start_node.get_neighbours(grid)
    algorithm = algSymbols[order % 5]

    to_restart = False

def restart():
    global grid, start_node, finish_node, selected_node, queue, algorithm, simul_running, order, to_restart

    simul_running = False

    for row in grid:
        for node in row:
            node.f = 0
            node.g = 0
            node.h = 0
            node.visited = False
            node.timeSinceVisited = 0
            node.parent = None
            node.in_path = False
    
    start_node.visited = True

    queue = start_node.get_neighbours(grid)
    algorithm = algSymbols[order % 5]

    to_restart = False

def restart_random():

    global grid, start_node, finish_node, queue, algorithm, simul_running, order, to_restart

    simul_running = False

    grid = [[Node(i, j) for j in range(n_tiles)] for i in range(n_tiles)]

    start_node = grid[randrange(n_tiles)][randrange(n_tiles)]
    finish_node = grid[randrange(n_tiles)][randrange(n_tiles)]

    start_node.state = NodeState.start
    finish_node.state = NodeState.finish
    start_node.visited = True

    queue = start_node.get_neighbours(grid)
    algorithm = algSymbols[order % 5]

    to_restart = False

# Set the current algorithm to the nth in the list
def change_algorithm(n):
    global algorithm, order
    algorithm = algSymbols[n % 5]
    order = n % 5

# Set node to the current start node
def change_start(node):
    global grid, start_node, queue
    
    node.state = NodeState.start
    node.visited = True
    start_node.state = NodeState.moveable
    start_node.visited = False
    start_node = node
    queue = start_node.get_neighbours(grid)

# Set node to the current finish node
def change_finish(node):
    global finish_node
    
    node.state = NodeState.finish
    finish_node.state = NodeState.moveable
    finish_node = node

# Change selected nodes to pitch
def edit_selection(pitch):
    global grid

    for row in grid:
        for tile in row:
            if tile.selected:
                tile.pitch = pitch

# Transpose selected nodes by n (integer value, negative is down)
def transpose_selection(n):
    global grid

    numPitches = len(pitches)
    for row in grid:
        for tile in row:
            if tile.selected:
                tile.pitch = (tile.pitch + n) % numPitches

# Select no nodes
def clear_selection():
    global grid

    for row in grid:
        for tile in row:
            tile.selected = False    

# Executes every time we visit a node and see if we have finished
def check_finish(node):
    global simul_running
    global to_restart

    node.visited = True
    play_music(node.pitch)
    make_path(node)

    if node.state == NodeState.finish:
        print('Found the finish node')
        simul_running = False
        to_restart = True

##################################################### MAIN LOOP #########################################################
    
restart_random()

while running:
    clock.tick(run_speed)

    screen.fill(bg_color)

    if simul_running:
        if len(queue) > 0:
            check_finish(algorithm())
        else:
            print("Couldn't find the finish node")
            simul_running = False
            to_restart = True

    for row in grid:
        for tile in row:
            tile.draw(screen)

    # Keybindings
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                simul_running = True
            # Change draw mode
            if event.key == pg.K_1:
                draw_mode = DrawMode.wall_place
            if event.key == pg.K_2:
                draw_mode = DrawMode.wall_remove
            if event.key == pg.K_3:
                draw_mode = DrawMode.start_move
            if event.key == pg.K_4:
                draw_mode = DrawMode.finish_move
            if event.key == pg.K_5:
                draw_mode = DrawMode.select
            if event.key == pg.K_6:
                draw_mode = DrawMode.deselect
            if event.key == pg.K_0:
                draw_mode = DrawMode.none
            
            # Change algorithm
            if not simul_running:
                if draw_mode == DrawMode.select:
                    if event.key == pg.K_a:
                        edit_selection(pitches.index('A'))
                    if event.key == pg.K_b:
                        edit_selection(pitches.index('B'))
                    if event.key == pg.K_c:
                        edit_selection(pitches.index('C'))
                    if event.key == pg.K_d:
                        edit_selection(pitches.index('D'))
                    if event.key == pg.K_e:
                        edit_selection(pitches.index('E'))
                    if event.key == pg.K_f:
                        edit_selection(pitches.index('F'))
                    if event.key == pg.K_g:
                        edit_selection(pitches.index('G'))
                    if event.key == pg.K_UP:
                        transpose_selection(1)
                    if event.key == pg.K_DOWN:
                        transpose_selection(-1)
                if event.key == pg.K_DELETE:
                    clear_selection()
                if event.key == pg.K_ESCAPE:
                    restart_random()
                if event.key == pg.K_TAB:
                    change_algorithm(order + 1)
                if event.key == pg.K_p:
                    msg = pyOSC3.OSCMessage()
                    msg.setAddress("/instrument1")
                    msg.append("instrument1")
                    client.send(msg)
                if event.key == pg.K_o:
                    msg = pyOSC3.OSCMessage()
                    msg.setAddress("/instrument2")
                    msg.append("instrument2")
                    client.send(msg)
                # Save to file with date and time
                if event.key == pg.K_s:
                    now = datetime.now().time()
                    with open('saves/' + str(now).replace(':', '.') + '.txt', 'w') as test:
                        json.dump(json.dumps(grid, default=vars), test)
                # Load from file
                if event.key == pg.K_l:
                    filepath = filedialog.askopenfilename(title="Load Grid", filetypes= (("text files","*.txt"),("all files","*.*")))
                    with open(filepath, 'r') as test:
                        data = json.loads(json.load(test))
                        load_grid(data)

        elif event.type == pg.MOUSEBUTTONDOWN and not simul_running:
            mouse_down = True

        elif event.type == pg.MOUSEBUTTONUP and not simul_running:
            mouse_down = False
            
    # Draw mode functionality
    if mouse_down:
        pos = pg.mouse.get_pos()

        # i = int(pos[0] / dim * n_tiles)
        i = int(pos[0] // tile_size)
        # j = int(pos[1] / dim * n_tiles)
        j = int(pos[1] // tile_size)
        
        if i < n_tiles and j < n_tiles:
            t = grid[i][j]

            if draw_mode == DrawMode.wall_place and t.state == NodeState.moveable:
                t.state = NodeState.wall
            elif draw_mode == DrawMode.wall_remove and t.state == NodeState.wall:
                t.state = NodeState.moveable
            elif draw_mode == DrawMode.start_move and t.state != NodeState.finish:
                change_start(t)
            elif draw_mode == DrawMode.finish_move and t.state != NodeState.start:
                change_finish(t)
            elif draw_mode == DrawMode.select:
                t.selected = True
            elif draw_mode == DrawMode.deselect:
                t.selected = False


    # Draw algorithm and draw mode text
    screen.blit(algLabel, algLabelRect)
    screen.blit(algRenders[order], algRects[order])
    screen.blit(drawModeLabel, drawModeLabelRect)
    screen.blit(drawModeRenders[draw_mode], drawModeRects[draw_mode])
    pg.display.update()

    if to_restart:
        restart()

pg.quit()
