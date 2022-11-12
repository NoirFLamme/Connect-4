
class State:
    def __init__(self ,s):
        self.stateCarrier = s

    def move(self ,colChosen):
        turn = self.checkTurn()
        requiredBlock = (self.stateCarrier & 7 << 6+9*colChosen) >> 6+9*colChosen
        if requiredBlock==6:
            print("Invalid Move. Column is full!")
            return
        self.stateCarrier |= turn << 9*colChosen + requiredBlock
        requiredBlock += 1
        self.stateCarrier &= ~(7 << 6+9*colChosen)
        self.stateCarrier |= requiredBlock << 6+9*colChosen
        self.changeTurn()

    def checkTurn(self):
        return self.stateCarrier >> 64

    def changeTurn(self):
        self.stateCarrier ^= (1 << 64)




myState = State(18446744073709551616)
myState.move(1)
myState.move(2)
myState.move(1)
print(myState.stateCarrier)
