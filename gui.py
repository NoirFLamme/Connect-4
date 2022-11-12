import numpy as np
import pygame
import sys
import math
from playsound import playsound


BLUE = (0,139,139)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0
display_type = 0
algo = "def"

# initalize pygame
pygame.init()

# define our screen size
SQUARESIZE = 100

# define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
# Calling function draw_board again


myfont = pygame.font.SysFont("monospace", 75)
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
# this font
quit = smallfont.render('quit', True, (255,255,255))
alphabeta = smallfont.render('alphabeta', True, (255,255,255))
minmax = smallfont.render('minmax', True, (255,255,255))

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            if display_type != 0:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if display_type == 0:
                if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                    pygame.quit()
                elif width / 2 - 60 <= mouse[0] <= width / 2 + 80 and height / 2 - 50 <= mouse[1] <= height / 2 - 10:
                    display_type = 1
                    algo = "min"
                    screen.fill(BLACK)
                    draw_board(board)
                    pygame.display.update()
                elif width / 2 - 60 <= mouse[0] <= width / 2 + 80 and height / 2 - 100 <= mouse[1] <= height / 2 - 60:
                    display_type = 1
                    algo = "alpha"
                    screen.fill(BLACK)
                    draw_board(board)
                    pygame.display.update()
            else:
                playsound("SoundEffects/move.wav")
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render("Player 1 Point!", 1, RED)
                            screen.blit(label, (40, 10))
                            playsound("SoundEffects/point.wav")



                # # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 Point!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            playsound("SoundEffects/point.wav")

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)

        if display_type == 0:
            screen.fill((60, 25, 60))

            # stores the (x,y) coordinates into
            # the variable as a tuple
            mouse = pygame.mouse.get_pos()

            # if mouse is hovered on a button it
            # changes to lighter shade
            if width / 2 - 60 <= mouse[0] <= width / 2 + 80 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.draw.rect(screen, (170,170,170), [width / 2 - 60, height / 2, 140, 40])

            else:
                pygame.draw.rect(screen, (100,100,100), [width / 2 - 60, height / 2, 140, 40])

            if width / 2 - 60 <= mouse[0] <= width / 2 + 80 and height / 2 - 50 <= mouse[1] <= height / 2 - 10:
                pygame.draw.rect(screen, (170, 170, 170), [width / 2 - 60, height / 2 - 50 , 140, 40])

            else:
                pygame.draw.rect(screen, (100, 100, 100), [width / 2 - 60, height / 2 - 50 , 140, 40])

            if width / 2 - 60 <= mouse[0] <= width / 2 + 80 and height / 2 - 100 <= mouse[1] <= height / 2 - 60:
                pygame.draw.rect(screen, (170, 170, 170), [width / 2 - 60, height / 2 - 100 , 140, 40])

            else:
                pygame.draw.rect(screen, (100, 100, 100), [width / 2 - 60, height / 2 - 100, 140, 40])

            # superimposing the text onto our button
            screen.blit(quit, (width / 2 + 50 - 70, height / 2))
            screen.blit(minmax, (width / 2 + 50 - 95, height / 2 - 100))
            screen.blit(alphabeta, (width / 2 + 50 - 110,  height / 2 - 50))


            # updates the frames of the game
            pygame.display.update()