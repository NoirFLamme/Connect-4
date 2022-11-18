from const import *
from evaluation import evaluation


class State:
    def __init__(self):
        self.value = 0

    def __str__(self):
        value = ""
        board = [[0 for i in range(COLUMN_COUNT)] for j in range(ROW_COUNT)]
        for j in range(COLUMN_COUNT):
            for i in range(ROW_COUNT):
                board[i][j] = self.get(i, j)
        for i in board:
            value += '\t'.join(map(str, i))
            value += '\n'
        return value


    def map(self, board, turn):
        self.value = 0
        for j in range(7):
            stopped = False
            for temp_i in range(5, -1, -1):
                i = 5-temp_i
                if board[temp_i][j] == 0:
                    self.value |= i << ROW_COUNT + 9 * j
                    stopped = True
                    break
                if board[temp_i][j] == 2:
                    self.value |= 1 << i + 9 * j
            if not stopped:
                self.value |= ROW_COUNT << ROW_COUNT + 9 * j

        self.value |= (turn << 63)
        print("Resulted State: ", self.value)

    def move(self, colChosen):
        turn = self.checkTurn()
        requiredBlock = self.getLastColBlock(colChosen)
        if requiredBlock == ROW_COUNT:
            print("Invalid Move. Column is full!")
            return
        self.value |= turn << 9 * colChosen + requiredBlock
        requiredBlock += 1
        self.value &= ~(7 << 6 + 9 * colChosen)
        self.value |= requiredBlock << 6 + 9 * colChosen
        # isPoint = self.evaluate(ROW_COUNT-requiredBlock,colChosen)
        self.changeTurn()
        # print("Move Done")
        return 0

    def valid_move(self, i):
        return self.getLastColBlock(i) != ROW_COUNT

    def getLastColBlock(self, col):
        return (self.value & 7 << ROW_COUNT + 9 * col) >> ROW_COUNT + 9 * col

    def checkTurn(self):
        return self.value >> 63

    def changeTurn(self):
        self.value ^= 1 << 63

    def get(self, i, j):    
        if i < 0 or j < 0 or i > ROW_COUNT or j > COLUMN_COUNT:
            raise ValueError(
                "Index out of Bound. State.get(", i, ",", j, ") Failed.")
        thres = self.getLastColBlock(j)
        i = 5-i
        if (i < thres):
            return ((self.value & 1 << (i + 9 * j)) >> (i + 9 * j)) + 1
        return 0

    def cost(self, row, col):
        if (self.get(row, col) != 0):
            return 0
        return ROW_COUNT - row - self.getLastColBlock(col)

    def heuristic(self):
        WINDOW_SIZE = 4
        heuristic = 0

        # Check horizontal
        for row in range(ROW_COUNT):
            count = [0, 0, 0]
            cost = 0
            # Create window of size 4
            for col in range(WINDOW_SIZE):
                count[self.get(row, col)] += 1
                cost += self.cost(row, col)
            heuristic += evaluation(count, cost)
            # Slide the window
            colEnd = WINDOW_SIZE
            while colEnd < COLUMN_COUNT:
                count[self.get(row, colEnd-WINDOW_SIZE)] -= 1
                count[self.get(row, colEnd)] += 1
                cost -= self.cost(row, colEnd-WINDOW_SIZE)
                cost += self.cost(row, colEnd)
                colEnd += 1
                heuristic += evaluation(count, cost)

        # Check vertical
        for col in range(COLUMN_COUNT):
            count = [0, 0, 0]
            # Create window of size 4
            for row in range(WINDOW_SIZE):
                count[self.get(row, col)] += 1
            heuristic += evaluation(count, count[0])
            # Slide the window
            rowEnd = WINDOW_SIZE
            while rowEnd < ROW_COUNT:
                count[self.get(rowEnd-WINDOW_SIZE, col)] -= 1
                count[self.get(rowEnd, col)] += 1
                rowEnd += 1
                heuristic += evaluation(count, count[0])

        # Check diagonal

        # Check top left to bottom right
        start_row = ROW_COUNT - WINDOW_SIZE
        end_col = COLUMN_COUNT - WINDOW_SIZE
        start_col = 0
        while start_col <= end_col:
            count = [0, 0, 0]
            cost = 0
            row = start_row
            col = start_col
            # Create window
            for i in range(WINDOW_SIZE):
                count[self.get(row, col)] += 1
                cost += self.cost(row, col)
                row += 1
                col += 1
            heuristic += evaluation(count, cost)
            # slide window
            while row < ROW_COUNT and col < COLUMN_COUNT:
                count[self.get(row-WINDOW_SIZE, col-WINDOW_SIZE)] -= 1
                count[self.get(row, col)] += 1
                cost -= self.cost(row-WINDOW_SIZE, col-WINDOW_SIZE)
                cost += self.cost(row, col)
                heuristic += evaluation(count, cost)
                row += 1
                col += 1
            if start_row == 0:
                start_col += 1
            else:
                start_row -= 1

        # Check top right to bottom left
        start_col -= 1
        end_row = ROW_COUNT - WINDOW_SIZE
        while start_row <= end_row:
            count = [0, 0, 0]
            cost = 0
            row = start_row
            col = start_col
            # Create window
            for i in range(WINDOW_SIZE):
                count[self.get(row, col)] += 1
                cost += self.cost(row, col)
                row += 1
                col -= 1
            heuristic += evaluation(count, cost)

            # slide window
            while col >= 0 and row < ROW_COUNT:
                count[self.get(row-WINDOW_SIZE, col+WINDOW_SIZE)] -= 1
                count[self.get(row, col)] += 1
                cost -= self.cost(row-WINDOW_SIZE, col+WINDOW_SIZE)
                cost += self.cost(row, col)
                heuristic += evaluation(count, cost)
                row += 1
                col -= 1
            if start_col == COLUMN_COUNT-1:
                start_row += 1
            else:
                start_col += 1
        return heuristic

    def scores(self):
        scores = [0, 0]
        def update_scores(count):
            if count[PLAYER_PIECE] == 4:
                scores[0] += 1
            if count[AGENT_PIECE] == 4:
                scores[1] += 1

        # Check horizontal
        for row in range(ROW_COUNT):
            count = [0, 0, 0]
            # Create window of size 4
            for col in range(WINDOW_SIZE):
                count[self.get(row, col)] += 1
            update_scores(count)
            # Slide the window
            for col in range(WINDOW_SIZE, COLUMN_COUNT):
                count[self.get(row, col-WINDOW_SIZE)] -= 1
                count[self.get(row, col)] += 1
                update_scores(count)
        # Check vertical
        for col in range(COLUMN_COUNT):
            count = [0, 0, 0]
            # Create window of size 4
            for row in range(WINDOW_SIZE):
                count[self.get(row, col)] += 1
            update_scores(count)
            # Slide the window
            for row in range(WINDOW_SIZE, ROW_COUNT):
                count[self.get(row-WINDOW_SIZE, col)] -= 1
                count[self.get(row, col)] += 1
                update_scores(count)
        # Check top left to bottom right
        start_row = ROW_COUNT - WINDOW_SIZE
        end_col = COLUMN_COUNT - WINDOW_SIZE
        start_col = 0
        while start_col <= end_col:
            count = [0, 0, 0]
            row = start_row
            col = start_col
            # Create window
            for i in range(WINDOW_SIZE):
                count[self.get(row, col)] += 1
                row += 1
                col += 1
            update_scores(count)
            # slide window
            while row < ROW_COUNT and col < COLUMN_COUNT:
                count[self.get(row-WINDOW_SIZE, col-WINDOW_SIZE)] -= 1
                count[self.get(row, col)] += 1
                update_scores(count)
                row += 1
                col += 1
            if start_row == 0:
                start_col += 1
            else:
                start_row -= 1

        # Check top right to bottom left
        start_col -= 1
        end_row = ROW_COUNT - WINDOW_SIZE
        while start_row <= end_row:
            count = [0, 0, 0]
            row = start_row
            col = start_col
            # Create window
            for i in range(WINDOW_SIZE):
                count[self.get(row, col)] += 1
                row += 1
                col -= 1
            update_scores(count)

            # slide window
            while col >= 0 and row < ROW_COUNT:
                count[self.get(row-WINDOW_SIZE, col+WINDOW_SIZE)] -= 1
                count[self.get(row, col)] += 1
                update_scores(count)
                row += 1
                col -= 1
            if start_col == COLUMN_COUNT-1:
                start_row += 1
            else:
                start_col += 1
        return scores


def pb(num):
    if num >= 1:
        pb(num // 2)
    print(num % 2, end="")
