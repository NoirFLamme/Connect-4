import math

from StateFile import State
from AIModule import  minimax,minimaxAlphaBeta


def getMove(board, algo):
    state = State()
    state.mapToState(board, 1)
    if algo == "min":
        return minimax(5, state, True)[1]
    else:
        return minimaxAlphaBeta(5, state, True, -math.inf, math.inf)[1]
