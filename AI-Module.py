import copy
import sys
import math

from StateFile import State


def minimax(depth, state: State, maxplayer:bool):
    if depth == 0:
        return state.getHeuristic(),0
    if maxplayer:
        maxEval = -math.inf
        maxEvalIndex = -1
        moves = []
        for i in range(7):
            if state.valid_move(i):    
                child = copy.deepcopy(state)
                child.move(i)
                moves.append((child,i))
        for move in moves:
            eval = minimax(depth - 1, move[0], False)[0]
            if (eval > maxEval):
                maxEval = eval
                maxEvalIndex = move[1]
        return maxEval, maxEvalIndex
    else:
        minEval = math.inf
        minEvalIndex = -1
        moves = []
        for i in range(7):
            if state.valid_move(i): 
                child = copy.deepcopy(state)
                child.move(i)
                moves.append((child, i))
        for move in moves:
            eval = minimax(depth - 1, move[0], True)[0]
            if (eval < minEval):
                minEval = eval
                minEvalIndex = move[1]
        return minEval, minEvalIndex


def minimaxAlphaBeta(depth, state: State, maxplayer, alpha, beta):
    #TODO
    if depth == 0:
        return state.getHeuristic(), 0
    if maxplayer:
        maxEval = -math.inf
        maxEvalIndex = -1
        moves = []
        for i in range(7):
            if state.valid_move(i):
                child = copy.deepcopy(state)
                child.move(i)
                moves.append((child, i))
        for move in moves:
            eval = minimax(depth - 1, move[0], False)[0]
            if eval > maxEval:
                maxEval = eval
                maxEvalIndex = move[1]
            alpha = max(alpha, eval)
            if beta < alpha:
                return maxEval, maxEvalIndex
        return maxEval,  maxEvalIndex
    else:
        minEval = math.inf
        minEvalIndex = -1
        moves = []
        for i in range(7):
            if state.valid_move(i):
                child = copy.deepcopy(state)
                child.move(i)
                moves.append((child, i))
        for move in moves:
            eval = minimax(depth - 1, move[0], False)[0]
            if eval < minEval:
                minEval = eval
                minEvalIndex = move[1]
            beta = min(beta, eval)
            if beta < alpha:
                return minEval, minEvalIndex
        return minEval, minEvalIndex


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
myState.move(3)
depth = int(input())
print(minimax(depth,myState,True))
print(minimaxAlphaBeta(depth, myState, True, -math.inf, math.inf))
