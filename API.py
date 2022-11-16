import copy
import math

import numpy as np

from StateFile import State
from AIModule import  minimax,minimaxAlphaBeta


def getMove(board, algo):
    ourboard = copy.deepcopy(board)
    for i in range(int(len(board) / 2)):
        ourboard[[i, len(board) - 1 - i]] = ourboard[[len(board) - 1 - i, i]]
    state = State()
    state.mapToState(ourboard, 1)
    if algo == "min":
        return minimax(5, state, True)[1]
    else:
        # print(minimaxAlphaBeta(5, state, True, -math.inf, math.inf)[1])
        return minimaxAlphaBeta(5, state, True, -math.inf, math.inf)[1]
