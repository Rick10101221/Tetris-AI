import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800  # window size
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

# where on the screen we will start drawing shapes
top_left_x = (s_width - play_width) // 2  # = 250
top_left_y = s_height - play_height       # = 100


# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
        

def create_grid(locked_positions={}):
    '''Fills the grid with either black or colored squares'''
    # Filling grid with black squares
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    # If square is colored (or has piece there),
    # recolor it to that color in the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c

    return grid


def convert_shape_format(shape):
    '''Takes a shape (from those defined above) and converts to\
        something that the program can work with''' 
    positions = []
    # Gets the exact form and rotation of the shape
    form = shape.shape[shape.rotation % len(shape.shape)]

    # TODO
    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    # Constant offset to graphically render the pieces properly
    for i , pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    '''Checks if the given shape is in a valid position in the grid'''
    # Creates a list of all accepted or 'valid' positions in the grid. 
    # This ONLY includes squares that are black, which do not have any pieces in them
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    # Flatten the list into just tuples
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                    return False
    return True


def check_lost(positions):
    '''Checks if we have lost the game'''
    # Returns true if the y-value for any of the passed in positions 
    # (of pieces?) is <= 0, which is at or above the play area 
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    pass

   
def draw_grid(surface, row, col):
    '''Draws grey lines that represent the grid'''
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx + play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):
    pass


def draw_next_shape(shape, surface):
    # Creates a font using pygame.font.SysFont('font', size)
    font = pygame.font.SysFont('timesnewroman', 30)
    # Creates a label that will render the font onto the play surface
    label = font.render('Next Shape', 1, (255,255,255))

    # The x and y position where the label (or shape?) will be drawn
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid):
    '''TODO'''
    # Initializes font module so other font functions can work
    pygame.font.init()
    # Returns a new font object that is loaded from system fonts
    font = pygame.font.SysFont('timesnewroman', 60, 1)
    # Will create a new surface with the given text rendered onto it
    label = font.render('Tetris', 1, (255,255,255))
    # Draws the label onto the surface at the given coordinate position
    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 30))

    # TODO 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    # TODO
    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 5)    
    
    # TODO Missing correct row and col parameter
    draw_grid(surface, grid)
    # TODO Need display to be initalized first?
    pygame.display.update()


def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False            # TODO
    run = True                      # Whether or not the game is running
    current_piece = get_shape()     # TODO
    next_piece = get_shape()        # TODO
    clock = pygame.time.Clock()     # TODO
    fall_time = 0                   # TODO
    fall_speed = 0.27               # How long its gonna take before each shape starts falling

    # Runs the game and checks for key presses. TODO
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece -= 1
                change_piece = True

        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                run = False

            # If a key is pressed 'down'. TODO tutorial may be incorrect
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

        draw_window(win, grid)

        if check_lost(locked_positions):
            run = False

    pygame.display.quit()

def main_menu(win):
    main(win)

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game