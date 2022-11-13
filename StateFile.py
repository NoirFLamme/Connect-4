def pb(num):
    if num >= 1:
        pb(num // 2)
    print(num % 2, end = "")
COLUMN_COUNT = 7
ROW_COUNT = 6

class State:
    def __init__(self ,s):
        self.value = s

    def move(self ,colChosen):
        turn = self.checkTurn()
        requiredBlock = self.getLastColBlock(colChosen)
        if requiredBlock == ROW_COUNT:
            print("Invalid Move. Column is full!")
            return
        self.value |= turn << 9 * colChosen + requiredBlock
        requiredBlock += 1
        self.value &= ~(7 << 6 + 9 * colChosen)
        self.value |= requiredBlock << 6 + 9 * colChosen
        self.changeTurn()
        print("Move Done")

    def getLastColBlock(self,col):
        return (self.value & 7 << ROW_COUNT + 9 * col) >> ROW_COUNT + 9 * col

    def checkTurn(self):
        return self.value >> 64

    def changeTurn(self):
        self.value ^= 1 << 64

    def mapToState(self,board,turn):
        self.value = 0
        for j in range (7):
            stopped = False
            for temp_i in range (5,-1,-1):
                i = 5-temp_i
                if board[temp_i][j]==0:
                    self.value |= i << ROW_COUNT + 9 * j
                    stopped = True
                    break
                if board[temp_i][j]==2:
                    self.value |= 1 << i + 9 * j
            if not stopped:
                self.value |= ROW_COUNT << ROW_COUNT + 9 * j

        self.value |= (turn << 64)
        print("Resulted State: ", self.value)

    def showState(self):
        board = [[0 for i in range(COLUMN_COUNT)] for j in range(ROW_COUNT)]
        for j in range (COLUMN_COUNT):
            checkPoint = self.getLastColBlock(j)
            for temp_i in range (checkPoint):
                i = 5 - temp_i
                board[i][j] = ((self.value & 1 << (temp_i + 9 * j)) >> (temp_i + 9 * j)) + 1
        for i in board:
            print('\t'.join(map(str, i)))
        print("It's Player", self.checkTurn()+1,"'s turn")

    def get(self,i,j):
        thres = self.getLastColBlock(j)
        i = 5-i
        if (i<thres):
            return ((self.value & 1 << (i + 9 * j)) >> (i + 9 * j)) + 1
        return 0



    def getHeuristic(self):
        #TODO
        pass


board1 = [
        [0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 0, 1, 2],
        [1, 1, 2, 2, 0, 2, 1],
        [2, 2, 1, 1, 0, 1, 2],
        [1, 1, 1, 1, 0, 2, 1],
        [1, 2, 2, 2, 1, 2, 1],
]
board2 = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [2, 1, 1, 0, 0, 0, 0],
        [2, 2, 1, 1, 0, 0, 0],
        [2, 1, 2, 2, 1, 0, 0],
]
myState = State(18446744073709551616)
myState.mapToState(board2,1)
myState.showState()
