def pb(num):
    if num >= 1:
        pb(num // 2)
    print(num % 2, end = "")

class State:
    def __init__(self ,s):
        self.stateCarrier = s

    def move(self ,colChosen):
        turn = self.checkTurn()
        requiredBlock = self.getLastColBlock(colChosen)
        if requiredBlock==6:
            print("Invalid Move. Column is full!")
            return
        self.stateCarrier |= turn << 9*colChosen + requiredBlock
        requiredBlock += 1
        self.stateCarrier &= ~(7 << 6+9*colChosen)
        self.stateCarrier |= requiredBlock << 6+9*colChosen
        self.changeTurn()

    def getLastColBlock(self,col):
        var = (self.stateCarrier & 7 << 6 + 9 * col)
        return var >> 6 + 9 * col

    def checkTurn(self):
        return self.stateCarrier >> 64

    def changeTurn(self):
        self.stateCarrier ^= (1 << 64)

    def mapToState(self,board,turn):
        self.stateCarrier = 0
        for j in range (7):
            stopped = False
            for temp_i in range (5,-1,-1):
                i = 5-temp_i
                if board[temp_i][j]==0:
                    self.stateCarrier |= i << 6 + 9 * j
                    stopped = True
                    break
                if board[temp_i][j]==2:
                    self.stateCarrier |= 1 << i + 9 * j
            if not stopped:
                self.stateCarrier |= 6 << 6 + 9 * j

        self.stateCarrier |= (turn << 64)
        print("Resulted State: ",self.stateCarrier)

    def showState(self):
        board = [[0 for i in range(7)] for j in range(6)]
        for j in range (7):
            checkPoint = self.getLastColBlock(j)
            for temp_i in range (checkPoint):
                i = 5 - temp_i
                board[i][j] = ((self.stateCarrier & 1 << (temp_i + 9 * j)) >> (temp_i+9*j)) + 1
        for i in board:
            print('\t'.join(map(str, i)))
        print("It's Player", self.checkTurn()+1,"'s turn")

board1 = [
        [1, 1, 1, 1, 0, 1, 2],
        [2, 2, 2, 2, 1, 1, 2],
        [1, 1, 2, 2, 1, 2, 1],
        [2, 2, 1, 1, 2, 1, 2],
        [1, 1, 1, 1, 2, 2, 1],
        [1, 2, 2, 2, 1, 2, 1],
]
board2 = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
]
myState = State(18446744073709551616)
myState.mapToState(board1,0)
myState.move(4)
pb(myState.stateCarrier)
print()
print(myState.stateCarrier)
myState.showState()
