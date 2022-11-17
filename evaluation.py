from const import *


def evaluation(count, cost):
    empty = count[0]
    player = count[1]
    agent = count[2]

    if (player > 0 and agent > 0) or empty >= 4:
        return 0

    # pieces are either player's or computer's
    sign = -1 if player > 0 else 1
    index = PLAYER_PIECE if player > 0 else AGENT_PIECE
    values = [2, 3, 8, 15]

    if empty == 0:
        factor = 1
    else:
        factor = empty/cost

    return factor * values[count[index-1]] * sign
