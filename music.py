import pygame as pg
from pygame.color import THECOLORS as colors
from pygame.display import toggle_fullscreen
from pygame.draw import *

from enum import IntEnum
from random import random, randrange, choice
import time
import pyOSC3

pg.init()
pg.mixer.init()

############################################ PROGRAM VARIABLES ################################################

# Set up OSC client
client = pyOSC3.OSCClient()
client.connect( ( '127.0.0.1', 57120 ) )

# Flags
running = True
run_speed = 10
mouse_down = False
to_restart = False
# pitches = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
pitches = ["C", "D", "E", "F", "G", "A", "B"]
clock = pg.time.Clock()

class DrawMode(IntEnum):
    none = 0
    wall_place = 1
    wall_remove = 2
    start_move = 3
    finish_move = 4

draw_mode = DrawMode.none

dim = 600
n_tiles = 30
tile_size = dim // n_tiles
bg_color = colors['lightblue']

# Set up screen
screen = pg.display.set_mode((dim * 1.5, dim))
pg.display.set_caption('Pathfinding')

fontBig = pg.font.Font('freesansbold.ttf', 32)
fontSmall = pg.font.Font('freesansbold.ttf', 14)

# (a_star, 'A Star'),
# (dijkstra, 'Dijkstra'),
# (greedy_bfs, 'Greedy Best First Search'),
# (dfs, 'Depth First Search'),
# (bfs, 'Breadth First Search')
algNames = ['A Star', 'Dijkstra', 'Greedy Best First Search', 'Depth First Search', 'Breadth First Search']
numAlgs = len(algNames)
algRenders = [None for _ in range(numAlgs)]
algRects = [None for _ in range(numAlgs)]
for i, alg in enumerate(algNames):
    algRenders[i] = fontSmall.render(alg, True, colors['black'])
    algRects[i] = rect(screen, colors['black'], (dim + 3.5 * tile_size, tile_size * (i + 1) * 2 + 2, dim / 2, dim))

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
        # self.pitch = choice(pitches)
        # TODO Allow for customized pitch grids
        # Temporarily select pitch by column
        self.pitch = pitches[i % len(pitches)]

        if random() < 0.2:
            self.state = NodeState.wall

        self.in_path = False

    def draw(self, screen):
        rect_color = colors['white']

        # Color the node correctly according to its state
        if self.in_path:
            rect_color = colors['yellow']
        elif self.state == NodeState.start:
            rect_color = colors['lightgreen']
        elif self.state == NodeState.finish:
            rect_color = colors['coral']
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

        # Render white square for node
        rect(screen, rect_color, (self.pos[0] * tile_size,
                                  self.pos[1] * tile_size, tile_size, tile_size))

        # Render node border
        rect(screen, bg_color, (self.pos[0] * tile_size,
                                self.pos[1] * tile_size, tile_size, tile_size), 2)
        
        # Render text
        if self.state == NodeState.moveable:                        
            pitchRender = fontSmall.render(self.pitch, True, colors['black'])
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

            # Uncomment to add diagonal neighbors
            # [-1, 1, up],
            # [1, 1, down],
            # [1, -1, right],
            # [-1, -1, left]
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
    msg.setAddress("/test")
    msg.append(pitch)
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


################################################### ALGORITHM VARIABLES #########################################################

order = 0

(grid,
start_node,
finish_node,
queue,
algorithm,
text,
text_rect,
simul_running) = [None for _ in range(8)]

def restart():

    global grid, start_node, finish_node, queue, algorithm, simul_running, text, text_rect, order, to_restart

    if order == 0:
        simul_running = False
    else:
        simul_running = True
        time.sleep(.3)

    grid = [[Node(i, j) for j in range(n_tiles)] for i in range(n_tiles)]

    start_node = grid[randrange(n_tiles)][randrange(n_tiles)]
    finish_node = grid[randrange(n_tiles)][randrange(n_tiles)]

    start_node.state = NodeState.start
    finish_node.state = NodeState.finish
    start_node.visited = True

    queue = start_node.get_neighbours(grid)
    algorithm, text_content = [
        (a_star, 'A Star'),
        (dijkstra, 'Dijkstra'),
        (greedy_bfs, 'Greedy Best First Search'),
        (dfs, 'Depth First Search'),
        (bfs, 'Breadth First Search')
    ][order % 5]

    text = fontBig.render(text_content, True, colors['red'])
    text_rect = text.get_rect()
    text_rect.center = dim*2//3, 50
    to_restart = False

# Set the current algorithm to the nth in the list
def change_algorithm(n):
    global algorithm, text, text_rect, order
    algorithm, text_content = [
        (a_star, 'A Star'),
        (dijkstra, 'Dijkstra'),
        (greedy_bfs, 'Greedy Best First Search'),
        (dfs, 'Depth First Search'),
        (bfs, 'Breadth First Search')
    ][n % 5]

    order = n

    text = fontBig.render(text_content, True, colors['red'])
    text_rect = text.get_rect()
    text_rect.center = dim*2//3, 50

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
    
restart()

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
            if event.key == pg.K_a:
                draw_mode = DrawMode.wall_place
            if event.key == pg.K_s:
                draw_mode = DrawMode.wall_remove
            if event.key == pg.K_d:
                draw_mode = DrawMode.start_move
            if event.key == pg.K_f:
                draw_mode = DrawMode.finish_move
            if event.key == pg.K_ESCAPE:
                draw_mode = DrawMode.none
            # Change algorithm
            if event.key == pg.K_1:
                change_algorithm(0)
            if event.key == pg.K_2:
                change_algorithm(1)
            if event.key == pg.K_3:
                change_algorithm(2)
            if event.key == pg.K_4:
                change_algorithm(3)
            if event.key == pg.K_5:
                change_algorithm(4)

        elif event.type == pg.MOUSEBUTTONDOWN and not simul_running:
            mouse_down = True

        elif event.type == pg.MOUSEBUTTONUP and not simul_running:
            mouse_down = False
            
    # Place or remove walls
    if mouse_down:
        pos = pg.mouse.get_pos()

        # i = int(pos[0] / dim * n_tiles)
        i = int(pos[0] // tile_size)
        # j = int(pos[1] / dim * n_tiles)
        j = int(pos[1] // tile_size)

        t = grid[i][j]

        if draw_mode == DrawMode.wall_place and t.state == NodeState.moveable:
            t.state = NodeState.wall
        elif draw_mode == DrawMode.wall_remove and t.state == NodeState.wall:
            t.state = NodeState.moveable
        elif draw_mode == DrawMode.start_move and t.state != NodeState.finish:
            change_start(t)
        elif draw_mode == DrawMode.finish_move and t.state != NodeState.start:
            change_finish(t)

    # Draw algorithm text
    # screen.blit(text, text_rect)
    pg.draw.rect(screen, colors['red'], pg.Rect(dim + 2 * tile_size, (order + 1) * tile_size * 2, tile_size, tile_size))
    for i in range(numAlgs):
        screen.blit(algRenders[i], algRects[i])
    pg.display.update()

    if to_restart:
        restart()

pg.quit()
