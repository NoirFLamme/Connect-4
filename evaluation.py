from const import *


def evaluation(count, cost):
    empty = count[0]
    player = count[1]
    agent = count[2]

    if (player > 0 and agent > 0) or empty >= 4:
        return 0

    # pieces are either player's or computer's
    playerSign = -1 if player > 0 else 1
    index = 1 if player > 0 else 2

    if count[index] == 4:
        return 100 * playerSign

    return (22 - (cost + count[0]) + 2**count[index]) * playerSign