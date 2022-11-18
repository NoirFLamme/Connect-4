import copy
import math

from state import State
from anytree import Node

def is_leaf(state):
    for i in range(7):
        if state.valid_move(i):
            return False
    return True

def minimax(depth, state: State, maxplayer: bool):
    rootNode = Node(str(state), parent=None)
    rootNode.best = False

    if depth == 0 or is_leaf(state):
        heuristic = state.heuristic()
        rootNode.name += f'\nH: {heuristic}'
        return heuristic, 0, rootNode
    moves = []
    for i in range(7):
        if state.valid_move(i):
            child = copy.deepcopy(state)
            child.move(i)
            moves.append((child, i))
    if maxplayer:
        maxEval = -math.inf
        maxEvalIndex = -1
        maxNode = None
        for move in moves:
            eval, evalIndex, childNode = minimax(depth - 1, move[0], False)
            childNode.parent = rootNode
            if (eval > maxEval):
                maxEval = eval
                maxEvalIndex = move[1]
                maxNode = childNode
        maxNode.best = True
        rootNode.name += f'\nH: {maxEval}'
        return maxEval, maxEvalIndex, rootNode
    else:
        minEval = math.inf
        minEvalIndex = -1
        minNode = None
        for move in moves:
            eval, evalIndex, childNode = minimax(depth - 1, move[0], True)
            childNode.parent = rootNode
            if (eval < minEval):
                minEval = eval
                minEvalIndex = move[1]
                minNode = childNode
        minNode.best = True
        rootNode.name += f'\nH: {minEval}'
        return minEval, minEvalIndex, rootNode


def minimaxAlphaBeta(depth, state: State, maxplayer, alpha, beta):
    rootNode = Node(str(state), parent=None)
    rootNode.best = False

    if depth == 0 or is_leaf(state):
        heuristic = state.heuristic()
        rootNode.name += f'\nH: {heuristic}'
        return heuristic, 0, rootNode
    moves = []
    for i in range(7):
        if state.valid_move(i):
            child = copy.deepcopy(state)
            child.move(i)
            moves.append((child, i))

    if maxplayer:
        maxEval = -math.inf
        maxEvalIndex = -1
        maxNode = None
        for move in moves:
            eval, evalIndex, childNode = minimaxAlphaBeta(depth - 1, move[0], False, alpha, beta)
            childNode.parent = rootNode
            if eval > maxEval:
                maxEval = eval
                maxEvalIndex = move[1]
                maxNode = childNode
            alpha = max(alpha, eval)
            if beta < alpha:
                rootNode.name += f'\nH: {maxEval}'
                return maxEval, maxEvalIndex, maxNode
        maxNode.best = True
        rootNode.name += f'\nH: {maxEval}'
        return maxEval,  maxEvalIndex, maxNode
    else:
        minEval = math.inf
        minEvalIndex = -1
        minNode = None
        for move in moves:
            eval, evalIndex, childNode = minimaxAlphaBeta(depth - 1, move[0], True, alpha, beta)
            childNode.parent = rootNode
            if eval < minEval:
                minEval = eval
                minEvalIndex = move[1]
                minNode = childNode
            beta = min(beta, eval)
            if beta < alpha:
                rootNode.name += f'\nH: {minEval}'
                return minEval, minEvalIndex, minNode
        minNode.best = True
        rootNode.name += f'\nH: {minEval}'
        return minEval, minEvalIndex, minNode
