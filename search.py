import copy
import math

from state import State


def minimax(depth, state: State, maxplayer: bool):
    if depth == 0:
        return state.heuristic(), 0
    moves = []
    for i in range(7):
        if state.valid_move(i):
            child = copy.deepcopy(state)
            child.move(i)
            moves.append((child, i))
    if maxplayer:
        maxEval = -math.inf
        maxEvalIndex = -1
        for move in moves:
            eval = minimax(depth - 1, move[0], False)[0]
            # if depth == 5:
            #     print(eval)
            #     print(move[0].showState())
            if (eval > maxEval):
                maxEval = eval
                maxEvalIndex = move[1]
        return maxEval, maxEvalIndex
    else:
        minEval = math.inf
        minEvalIndex = -1
        for move in moves:
            eval = minimax(depth - 1, move[0], True)[0]
            if (eval < minEval):
                minEval = eval
                minEvalIndex = move[1]
        return minEval, minEvalIndex


def minimaxAlphaBeta(depth, state: State, maxplayer, alpha, beta):
    if depth == 0:
        return state.heuristic(), 0
    moves = []
    for i in range(7):
        if state.valid_move(i):
            child = copy.deepcopy(state)
            child.move(i)
            moves.append((child, i))
    if maxplayer:
        maxEval = -math.inf
        maxEvalIndex = -1
        for move in moves:
            eval = minimaxAlphaBeta(depth - 1, move[0], False, alpha, beta)[0]
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
        for move in moves:
            eval = minimaxAlphaBeta(depth - 1, move[0], True, alpha, beta)[0]
            if eval < minEval:
                minEval = eval
                minEvalIndex = move[1]
            beta = min(beta, eval)
            if beta < alpha:
                return minEval, minEvalIndex
        return minEval, minEvalIndex
