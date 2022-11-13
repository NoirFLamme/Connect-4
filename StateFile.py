def pb(num):
    if num >= 1:
        pb(num // 2)
    print(num % 2, end = "")
COLUMN_COUNT = 7
ROW_COUNT = 6

class State:

    def __init__(self ):
        self.value = 0

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
        isPoint = self.evaluate(ROW_COUNT-requiredBlock,colChosen)
        self.changeTurn()
        print("Move Done")
        return isPoint

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
        print("Getting: ",i,j)
        if i>5 or i<0 or j<0 or j>6:
            print("Index out of Bound. State.get(",i,",",j,") Failed.")
            return None
        thres = self.getLastColBlock(j)
        i = 5-i
        if (i<thres):
            return ((self.value & 1 << (i + 9 * j)) >> (i + 9 * j)) + 1
        return 0



    def getHeuristic(self):
        #TODO
        pass

    def evaluate(self, i, j):
        res = 0
        print("Checking",i,j)
        player = self.checkTurn() + 1
        print("Turn:",player)
        # Check horizontal locations for win
        leftBound = max(0,j-3)
        rightBound = min(COLUMN_COUNT - 4, j)
        for k in range(leftBound,rightBound+1):
            if self.get(i,k) == player and self.get(i,k+1) == player and self.get(i,k+2) == player and self.get(i,k+3) == player:
                print("hort")
                res += 1

        # Check vertical locations for win
        upperBound = max(0,i-3)
        lowerBound = min(ROW_COUNT - 4, i)
        for k in range(upperBound,lowerBound+1):
            if self.get(k,j) == player and self.get(k+1,j) == player and self.get(k+2,j) == player and self.get(k+3,j) == player:
                print("vert")
                res += 1

        # Check positively sloped diagonals
        topLeftNorm = min(i-upperBound,j-leftBound)
        bottomRightNorm = min(i-lowerBound,j-rightBound)
        print("TopLeft:",topLeftNorm,"\tBottomRight:",bottomRightNorm)
        for d in range(topLeftNorm-bottomRightNorm+1):
            if self.get(i-d,j-d) == player and self.get(i-d+1,j-d+1) == player and self.get(i-d+2,j-d+2) == player and self.get(i-d+3,j-d+3) == player:
                print("posi")
                res += 1

        # Check negatively sloped diagonals
        bottomLeftNorm = min(i-lowerBound+3,j-leftBound)
        topRightNorm = min(upperBound-i+3,j-rightBound)
        print("BottomLeft:",bottomLeftNorm,"\tTopRight:",topRightNorm)
        for d in range(bottomLeftNorm-topRightNorm+1):
            if self.get(i+d,j-d) == player and self.get(i+d-1,j-d+1) == player and self.get(i+d-2,j-d+2) == player and self.get(i+d-3,j-d+3) == player:
                print("nega")
                res += 1
        return res


board1 = [
        [0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 2, 0, 1, 2],
        [1, 1, 2, 2, 0, 2, 1],
        [2, 2, 1, 1, 0, 1, 2],
        [1, 1, 1, 1, 0, 2, 1],
        [1, 2, 2, 2, 1, 2, 1],
]
board2 = [
        [0	,0	,0	,0	,0	,1	,1],
        [0	,0	,0	,0	,1	,2	,2],
        [0	,0	,0	,1	,2	,1	,1],
        [0	,1	,0	,1	,1	,2	,2],
        [0	,1	,1	,2	,2	,1	,1],
        [1	,2	,2	,1	,1	,2	,2],
]

myState = State()
myState.mapToState(board2,0)
trues = 0
# for i in range (1,8):
#     for j in range (i):
#         if myState.move(i-1):
#             trues +=1

# if myState.move(0):
#     trues += 1
# if myState.move(3):
#     trues += 1
trues += myState.move(2)
print("Trues: ",trues)
myState.showState()
