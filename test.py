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
    while(True):
        i = int(input())
        myState.move(i)
        print("H: ",myState.getHeuristic())
        myState.showState()

test1()
# //-16-16-18-10-12
#  = -72
# -11-12

# //16+13+7
# +15+9 = 60
#+14+15+8+9
