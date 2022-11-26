import numpy as np
import pygame
import sys
import math
from API import getMove, scores
from trace import save_tree
from itertools import chain


BLUE = (0, 139, 139)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7



def truncline(text, font, maxwidth):
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


def wrapline(text, font, maxwidth):
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)


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

    scoret = numFont.render(str(scoreP), True, RED)
    pygame.draw.rect(screen, (0, 0, 0), [75, 585, 70, 40])
    screen.blit(scoret, (75 + 18, 585))
    scorem = numFont.render(str(scoreAI), True, YELLOW)
    pygame.draw.rect(screen, (0, 0, 0), [width - 150, 585, 70, 40])
    screen.blit(scorem, (width - 150 + 28, 585))
    pygame.display.update()




# initalize pygame
pygame.init()
board = create_board()
print_board(board)
game_over = False
turn = 0
display_type = 0
scoreAI = 0
scoreP = 0
user_text = ''
active = False
node = None
algo = "min"
isReset = False
isAgain = False

# define our screen size
SQUARESIZE = 75

# define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height + 200)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)


myfont = pygame.font.SysFont("monospace", 75)
myfont2 = pygame.font.SysFont("monospace", 40)
smallfont = pygame.font.SysFont('Corbel', 30)
minifont = pygame.font.SysFont('Corbel', 20)
numFont = pygame.font.SysFont('Roboto Condensed', 30)



# rendering a text written in
# this font
quit = smallfont.render('Quit', True, (255, 255, 255))
alphabeta = minifont.render('Alphabeta', True, (255, 255, 255))
minmax = minifont.render('Minmax', True, (255, 255, 255))
trace = smallfont.render('Trace', True, (255, 255, 255))
youLabel = smallfont.render('You', True, RED)
aiLabel = smallfont.render('AI', True, YELLOW)
startGame = smallfont.render('Start Connecting', True, (255, 255, 255))
enterDepth = smallfont.render('Enter Depth:', True, (255, 255, 255))
chooseAI = smallfont.render('Choose AI:', True, (255, 255, 255))
base_font = pygame.font.Font(None, 32)
title = myfont.render('CONNECT 4\'Z',True,(128, 98, 68))
input_rect = pygame.Rect(300, 120 + 340, 140, 32)
img = pygame.image.load("Giant-LED-Connect-4.jpg").convert()
img = pygame.transform.scale(img, (280, 280))
backToMenu = smallfont.render('Back To Menu', True, (255, 255, 255))
playAgain = smallfont.render('Play Again', True, (255, 255, 255))

while not game_over:
    if isReset:
        board = create_board()
        print_board(board)
        game_over = False
        turn = 0
        display_type = 0
        scoreAI = 0
        scoreP = 0
        user_text = ''
        active = False
        node = None
        algo = "min"
        isReset = False
        isAgain = False

    if isAgain:
        board = create_board()
        print_board(board)
        screen.fill(BLACK)
        game_over = False
        turn = 0
        display_type = 1
        scoreAI = 0
        scoreP = 0
        draw_board(board)
        active = False
        node = None
        isReset = False
        isAgain = False
        pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            if display_type == 1:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                posy = event.pos[1]
                if turn == 0 and posy < 700:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

                pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if display_type == 0:
                active = input_rect.collidepoint(event.pos)
                if width / 2 - 40 <= mouse[0] <= width / 2 + 40 and height / 2 + 300 <= mouse[1] <= height / 2 + 300 + 40:
                    pygame.quit()
                elif width / 2 + 20 <= mouse[0] <= width / 2 + 100 and height / 2 + 252 <= mouse[1] <= height / 2 + 252 + 25:
                    algo = "min"
                elif width / 2 + 120 <= mouse[0] <= width / 2 + 220 and height / 2 + 252 <= mouse[1] <= height / 2 + 252 + 25:
                    algo = "alpha"
                if width / 2 - 115 <= mouse[0] <= width / 2 + 125 and height / 2 + 145 <= mouse[1] <= height / 2 + 145 + 40:
                    display_type = 1
                    screen.fill(BLACK)
                    draw_board(board)
                    pygame.display.update()
            elif display_type==1:
                #trace clicked
                if 60 <= mouse[0] <= 60 + 100 and 544 + 100 <= mouse[1] <= 544 + 100 + 40:
                    if node:
                        save_tree(node)
                #quit clicked
                elif width -165+ 30 <= mouse[0] <= width - 165+ 30 + 80 and 544 + 100 <= mouse[1] <= 544 + 100 + 40:
                    pygame.quit()
                elif 185 <= mouse[0] <= 185 + 185 and 544 + 100 <= mouse[1] <= 544 + 100 + 40:
                    isReset = True
                else:
                    # playsound("SoundEffects/move.wav")
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    # Ask for Player 1 Input
                    posy = event.pos[1]
                    if posy < 700:
                        if turn == 0:
                            posx = event.pos[0]
                            col = int(math.floor(posx / SQUARESIZE))

                            if is_valid_location(board, col):
                                row = get_next_open_row(board, col)
                                drop_piece(board, row, col, 1)
                                scoreP = scores(board, turn)[0]
                                scoret = numFont.render(str(scoreP), True, RED)
                                pygame.draw.rect(screen, (0, 0, 0), [75, 585, 70, 40])
                                screen.blit(scoret, (75 + 18, 585))
                                pygame.display.flip()
                                turn += 1
                                turn = turn % 2
                                # playsound("SoundEffects/point.wav")
                        print_board(board)
                        draw_board(board)


                        # Ask for Player 2 Input
                        if turn == 1:
                            # posx = event.pos[0]
                            if user_text.isdecimal() != True:
                                heuristic, col, node = getMove(board, algo)
                            else:
                                heuristic, col, node = getMove(board, algo, int(user_text))

                            if is_valid_location(board, col):
                                row = get_next_open_row(board, col)
                                drop_piece(board, row, col, 2)

                                scoreAI = scores(board, turn)[1]
                                scorem = numFont.render(str(scoreAI), True, YELLOW)
                                pygame.draw.rect(screen, (0,0,0), [width - 150,585, 70,40])
                                screen.blit(scorem, (width - 150 + 28, 585))
                                pygame.display.flip()
                                turn += 1
                                turn = turn % 2

                        print_board(board)
                        draw_board(board)

                        if 0 not in board:
                            display_type = 2
            #display 3 clicks
            else:
                if width / 2 - 60 - 10 <= mouse[0] <= width / 2 - 60 - 10 + 140 and margin + 44 <= mouse[
                    1] <= margin + 44 + 40:
                    isAgain = True
                elif width / 2 - 80 - 10 <= mouse[0] <= width / 2 - 80 - 10 + 185 and margin + 144 <= mouse[
                    1] <= margin + 144 + 40:
                    isReset = True
                elif width / 2 - 45 <= mouse[0] <= width / 2 - 30 + 80 and margin + 244 <= mouse[1] <= margin + 244 + 40:
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
            screen.fill((44, 62, 80))

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

            #quit
            if width / 2 - 40 <= mouse[0] <= width / 2 + 40 and height / 2 + 300 <= mouse[1] <= height / 2 + 300 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 width / 2 - 40, height / 2 + 300, 80, 40])
            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 width / 2 - 40, height / 2 + 300, 80, 40])
            #start
            if width / 2 - 115 <= mouse[0] <= width / 2 + 125 and height / 2 + 145 <= mouse[1] <= height / 2 + 145 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 width / 2 - 115, height / 2 + 145, 240, 40])
            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 width / 2 - 115, height / 2 + 145, 240, 40])
            #choose
            if algo=="min":
                pygame.draw.rect(screen, (170, 170, 170), [
                    width / 2 + 20, height / 2 + 252, 80, 25])
                pygame.draw.rect(screen, (100, 100, 100), [
                    width / 2 + 120, height / 2 + 252, 100, 25])
            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                    width / 2 + 20, height / 2 + 252, 80, 25])
                pygame.draw.rect(screen, (170, 170, 170), [
                    width / 2 + 120, height / 2 + 252, 100, 25])
            # superimposing the text onto our button
            screen.blit(startGame, (width / 2 - 100, height / 2 + 150))
            screen.blit(enterDepth, (width / 2 + 50 - 180, height / 2 + 200))
            screen.blit(chooseAI, (width / 2 + 50 - 180, height / 2 + 250))
            screen.blit(minmax, (width / 2 + 30, height / 2 + 255))
            screen.blit(alphabeta, (width / 2 + 130, height / 2 + 255))
            screen.blit(quit, (width / 2 - 25, height / 2 + 306))
            screen.blit(title,(20,0))
            screen.blit(img,(width/2-140,100))
            # updates the frames of the game
            pygame.display.update()
        elif display_type==1:
            mouse = pygame.mouse.get_pos()
            #quit
            if width -165+ 30 <= mouse[0] <= width - 165+ 30 + 80 and 544 + 100 <= mouse[1] <= 544 + 100 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 width -165+ 30, 544 + 100, 80, 40])
            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 width -165 + 30, 544 + 100, 80, 40])
            #trace
            if 60 <= mouse[0] <= 60 + 100 and 544 + 100 <= mouse[1] <= 544 + 100 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 60, 544 + 100, 100, 40])
            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 60, 544 + 100, 100, 40])
            #main menu
            if 185 <= mouse[0] <= 185 + 185 and 544 + 100 <= mouse[1] <= 544 + 100 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 185, 544 + 100, 185, 40])
            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 185 , 544 + 100, 185, 40])
            screen.blit(aiLabel, (width - 125, 550))
            screen.blit(youLabel, (75, 550))
            screen.blit(quit, (width - 150 + 30, 650))
            screen.blit(trace, (75, 650))
            screen.blit(backToMenu, (195, 650))
            pygame.display.update()
        #display 2
        else:
            mouse = pygame.mouse.get_pos()
            screen.fill(BLACK)
            if (scoreP>scoreAI):
                msg = wrap_multi_line('Congrats !!!'
                                           ' You defeated our enhanced AI.'
                                           ' That makes you ... '
                                           ' THE BEST CONNECT 4\'Z PLAYER EVER EXISTED'
                                           , myfont2, width-2)
                color = RED

            elif (scoreP<scoreAI):
                msg = wrap_multi_line('You have been defeated !!!'
                                        ' We\'re not surprised.'
                                        ' Our AI is unbeatable. '
                                        ' Try again .. or don\'t .. you\'re not gonna win anyway'
                                        , myfont2, width-5)
                color = YELLOW
            else:
                msg = wrap_multi_line('Draw with the AI !!!'
                                       ' Impressive ...'
                                       ' But just know that this is probably as far as you can get.'
                                       ' Feel free to try again but have no high expectations'
                                       , myfont2, width-15)
                color = (255,255,255)
            margin = 2
            for line in msg:
                x = myfont2.render(line,True,color)
                screen.blit(x,(15,margin))
                margin += 40 + 4
            #play again
            if width / 2 - 60 - 10 <= mouse[0] <= width / 2 - 60 - 10 + 140 and margin + 44 <= mouse[1] <= margin + 44 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                    width / 2 - 60 - 10, margin + 44, 140, 40])
            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                    width / 2 - 60 - 10, margin + 44, 140, 40])
            #back to main menu
            if width/2-80-10  <= mouse[0] <= width/2-80-10  + 185 and margin+144 <= mouse[1] <=margin+144 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 width/2-80-10 , margin+144, 185, 40])
            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 width/2-80-10  , margin+144, 185, 40])
            #quit
            if width/2 - 45 <= mouse[0] <= width/2 - 30 + 80 and margin + 244 <= mouse[1] <= margin + 244 + 40:
                pygame.draw.rect(screen, (170, 170, 170), [
                                 width/2 - 45, margin + 244, 80, 40])
            else:
                pygame.draw.rect(screen, (100, 100, 100), [
                                 width/2 - 45 , margin + 244, 80, 40])
            #blitting
            screen.blit(playAgain,(width/2 - 60,margin + 50))
            screen.blit(backToMenu,(width/2 - 80,margin + 50 + 100))
            screen.blit(quit,(width/2 - 30,margin + 250))
            pygame.display.update()


