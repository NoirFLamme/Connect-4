import numpy as np
import pygame
import sys
import math
from API import getMove, scores
from trace import save_tree

BLUE = (0, 139, 139)
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
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r *
                             SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
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
scoreAI = 0
scoreP = 0

# initalize pygame
pygame.init()

# define our screen size
SQUARESIZE = 100

# define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height + 200)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
# Calling function draw_board again


myfont = pygame.font.SysFont("monospace", 75)
smallfont = pygame.font.SysFont('Corbel', 35)


# rendering a text written in
# this font
quit = smallfont.render('quit', True, (255, 255, 255))
alphabeta = smallfont.render('alphabeta', True, (255, 255, 255))
minmax = smallfont.render('minmax', True, (255, 255, 255))
trace = smallfont.render('trace', True, (255, 255, 255))
scoreP1 = smallfont.render('P1:', True, (255, 255, 255))
scoreP2 = smallfont.render('P2:', True, (255, 255, 255))
base_font = pygame.font.Font(None, 32)
user_text = ''
active = False
input_rect = pygame.Rect(310, 200, 140, 32)
node = None
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            if display_type != 0:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                posy = event.pos[1]
                if turn == 0 and posy < 700:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

                pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if display_type == 0:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                    pygame.quit()
                elif width / 2 - 60 <= mouse[0] <= width / 2 + 80 and height / 2 - 50 <= mouse[1] <= height / 2 - 10:
                    display_type = 1
                    algo = "alpha"
                elif width / 2 - 60 <= mouse[0] <= width / 2 + 80 and height / 2 - 100 <= mouse[1] <= height / 2 - 60:
                    display_type = 1
                    algo = "min"

                screen.fill(BLACK)
                draw_board(board)

                # pygame.draw.rect(screen, (100, 100, 100), [width / 2 - 300, 750, 140, 40])
                # pygame.draw.rect(screen, (100, 100, 100), [width / 2 + 160, 750 , 140, 40])
                # screen.blit(quit, (width / 2 + 200,750))
                # screen.blit(trace, (width / 2 - 270, 750))
                pygame.display.update()
            elif width / 2 - 300 <= mouse[0] <= width / 2 - 300 + 140 and 750 <= mouse[1] <= 750 + 40:
                if node:
                    save_tree(node)
            elif width / 2 + 160 <= mouse[0] <= width / 2 + 160 + 140 and 750 <= mouse[1] <= 750 + 40:
                pygame.quit()
            else:
                # playsound("SoundEffects/move.wav")
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                posy = event.pos[1]
                if posy < 700:
                    if turn == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx / SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)

                            # if winning_move(board, 1):
                            #     label = myfont.render("Player 1 Point!", 1, RED)
                            #     screen.blit(label, (40, 10))
                            scoreP = scores(board, turn)[0]
                            scoret = smallfont.render(str(scoreP), True, (255, 255, 255))
                            pygame.draw.rect(screen, color, [width / 2 - 270+60,820, 70,40])
                            screen.blit(scoret, (width / 2 - 270 + 85, 820))
                            pygame.display.flip()
                            turn += 1
                            turn = turn % 2
                            # playsound("SoundEffects/point.wav")

                    print_board(board)
                    draw_board(board)


                    # # Ask for Player 2 Input
                    if turn == 1:
                        # posx = event.pos[0]
                        if user_text.isdecimal() != True:
                            heuristic, col, node = getMove(board, algo)
                        else:
                            heuristic, col, node = getMove(board, algo, int(user_text))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 2)

                            # if winning_move(board, 2):
                            #     label = myfont.render("Player 2 Point!", 1, YELLOW)
                            #     screen.blit(label, (40, 10))
                            scoreAI = scores(board, turn)[1]
                            scorem = smallfont.render(str(scoreAI), True, (255, 255, 255))
                            pygame.draw.rect(screen, color, [width / 2 + 200+60,820, 70,40])
                            screen.blit(scorem, (width / 2 + 200+85, 820))
                            pygame.display.flip()
                            turn += 1
                            turn = turn % 2
                            # playsound("SoundEffects/point.wav")

                    print_board(board)
                    draw_board(board)

                    # turn += 1
                    # turn = turn % 2

                    if 0 not in board:
                        pygame.time.wait(3000)
                        pygame.quit()
        if event.type == pygame.KEYDOWN:
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
                # get text input from 0 to -1 i.e. end.
                user_text = user_text[:-1]
            else:
                user_text += event.unicode
        if display_type == 0:
            if active:
                color =  (170,170,170)
            else:
                color = (100,100,100)
            screen.fill((60, 25, 60))

            pygame.draw.rect(screen, color, input_rect)

            text_surface = base_font.render(user_text, True, (255, 255, 255))

            # render at position stated in arguments
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

            # set width of textfield so that text cannot get
            # outside of user's text input
            input_rect.w = max(100, text_surface.get_width() + 10)

            # stores the (x,y) coordinates into
            # the variable as a tuple
            mouse = pygame.mouse.get_pos()

            # if mouse is hovered on a button it
            # changes to lighter shade
            if width / 2 - 60 <= mouse[0] <= width / 2 + 80 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 width / 2 - 60, height / 2, 140, 40])

            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 width / 2 - 60, height / 2, 140, 40])

            if width / 2 - 60 <= mouse[0] <= width / 2 + 80 and height / 2 - 50 <= mouse[1] <= height / 2 - 10:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 width / 2 - 60, height / 2 - 50, 140, 40])

            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 width / 2 - 60, height / 2 - 50, 140, 40])

            if width / 2 - 60 <= mouse[0] <= width / 2 + 80 and height / 2 - 100 <= mouse[1] <= height / 2 - 60:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 width / 2 - 60, height / 2 - 100, 140, 40])

            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 width / 2 - 60, height / 2 - 100, 140, 40])

            # superimposing the text onto our button
            screen.blit(quit, (width / 2 + 50 - 70, height / 2))
            screen.blit(minmax, (width / 2 + 50 - 95, height / 2 - 100))
            screen.blit(alphabeta, (width / 2 + 50 - 110,  height / 2 - 50))

            # updates the frames of the game
            pygame.display.update()
        else:
            mouse = pygame.mouse.get_pos()
            if width / 2 - 300 <= mouse[0] <= width / 2 - 300 + 140 and 750 <= mouse[1] <= 750 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 width / 2 - 300, 750, 140, 40])

            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 width / 2 - 300, 750, 140, 40])

            if width / 2 + 160 <= mouse[0] <= width / 2 + 160 + 140 and 750 <= mouse[1] <= 750 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 width / 2 + 160, 750, 140, 40])

            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 width / 2 + 160, 750, 140, 40])

            screen.blit(quit, (width / 2 + 200, 750))
            screen.blit(trace, (width / 2 - 270, 750))
            screen.blit(scoreP1, (width / 2 - 270, 820))
            screen.blit(scoreP2, (width / 2 + 200, 820))
            pygame.display.update()
