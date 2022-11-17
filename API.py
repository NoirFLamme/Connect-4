import copy
import math

from state import State
from search import minimax, minimaxAlphaBeta
from const import *

def parse_np_board(np_board):
    board = copy.deepcopy(np_board)
    for i in range(int(len(np_board) / 2)):
        board[[i, len(np_board) - 1 - i]] = board[[len(np_board) - 1 - i, i]]
    return board

def getMove(np_board, algo, depth=4):
    state = State()
    board = parse_np_board(np_board)
    state.map(board, AGENT_PIECE)
    if algo == "min":
        return minimax(depth, state, True)[1]
    else:
        return minimaxAlphaBeta(depth, state, True, -math.inf, math.inf)[1]


def scores(np_board, turn):
    state = State()
    board = parse_np_board(np_board)
    state.map(board, turn)
    return state.scores()
