from StateFile import State, pb


def test1():
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
    myState.move(3)
    myState.move(3)
    myState.move(3)
    myState.move(3)
    myState.move(3)
    # myState.move(4)
    print(myState.getHeuristic())

    print()
    myState.showState()

test1()
