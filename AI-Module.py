import copy
import sys

from Stack import Stack
from StateFile import State


class AIModule:
    def minimax(self,depth, InitialState, maxplayer):
        #TODO
        if depth == 0:
            return InitialState.getHeuristic()
        if maxplayer:
            maxEval = sys.maxsize
            children = []
            for i in range(7):
                temp = copy.deepcopy(InitialState)
                temp.move(i)
                children.append(temp)
            for child in children:
                eval = self.minimax(depth - 1, child, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = -sys.maxsize - 1
            children = []
            for i in range(7):
                children.append(copy.deepcopy(InitialState).move(i))
            for child in children:
                eval = self.minimax(depth - 1, child, True)
                maxEval = min(maxEval, eval)
            return minEval


    def minimaxAlphaBeta(self,depth, InitialState, maxplayer, alpha, beta):
        #TODO
        if depth == 0:
            return InitialState.getHeuristic()
        if maxplayer:
            maxEval = sys.maxsize
            children = []
            for i in range(7):
                children.append(copy.deepcopy(InitialState).move(i))
            for child in children:
                eval = self.minimax(depth - 1, child, False)
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
                eval = self.minimax(depth - 1, child, True)
                maxEval = min(maxEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
        pass


board1 = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

yes = AIModule()
myState = State()
myState.mapToState(board1, 0)
myState.move(2)
print(AIModule.minimax(yes,5,myState,True))
