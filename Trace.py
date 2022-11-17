import os

import copy
from anytree import Node, RenderTree
from anytree.exporter import DotExporter, UniqueDotExporter

from StateFile import State


def viewTree(board):
    ourboard = copy.deepcopy(board)
    for i in range(int(len(board) / 2)):
        ourboard[[i, len(board) - 1 - i]] = ourboard[[len(board) - 1 - i, i]]
    parent = Node(board,parent=None)
    state = State()
    state.mapToState(ourboard, 1)



    for i in range(7):
        if state.valid_move(i):
            child = copy.deepcopy(state)
            child.move(i)
            childNode = Node(child.showState(), parent=parent)
        for j in range(7):
            if state.valid_move(j):
                child2 = copy.deepcopy(child)
                child2.move(j)
                childNode1 = Node(child2.showState(), parent=childNode)
            for k in range(7):
                if state.valid_move(k):
                    child3 = copy.deepcopy(child2)
                    child3.move(k)
                    childNode2 = Node(child3.showState(), parent=childNode1)
                for x in range(7):
                    if state.valid_move(x):
                        child4 = copy.deepcopy(child3)
                        child4.move(x)
                        childNode3 = Node(child4.showState(), parent=childNode2)
    UniqueDotExporter(parent).to_picture("udo.pdf")
    path = 'udo.pdf'
    os.system(path)