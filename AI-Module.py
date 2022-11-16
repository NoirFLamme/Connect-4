import copy
import sys
import math

from StateFile import State


def minimax(depth, initial_state, maxplayer:bool):
    if depth == 0:
        return initial_state.getHeuristic()
    if maxplayer:
        maxEval = -math.inf
        children = []
        for i in range(7):
            child = copy.deepcopy(initial_state)
            child.move(i)
            children.append(child.move(i))
        for child in children:
            eval = minimax(depth - 1, child, False)
            maxEval = max(maxEval, eval)
        return maxEval
    else:
        minEval = math.inf
        children = []
        for i in range(7):
            child = copy.deepcopy(initial_state)
            child.move(i)
            children.append(child)
        for child in children:
            eval = minimax(depth - 1, child, True)
            minEval = min(minEval, eval)
        return minEval


def minimaxAlphaBeta(depth, InitialState, maxplayer, alpha, beta):
    #TODO
    if depth == 0:
        return InitialState.getHeuristic()
    if maxplayer:
        maxEval = sys.maxsize
        children = []
        for i in range(7):
            children.append(copy.deepcopy(InitialState).move(i))
        for child in children:
            eval = minimax(depth - 1, child, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = -sys.maxsize - 1
        children = []
        for i in range(7):
            children.append(copy.deepcopy(InitialState).move(i))
        for child in children:
            eval = minimax(depth - 1, child, True)
            maxEval = min(maxEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval


board1 = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

myState = State()
myState.mapToState(board1, 0)
myState.move(2)
print(minimax(2,myState,True))
