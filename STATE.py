import copy


class State():
    def __init__(self, initState, objState, preDirection=None, depth=0):
        self.direction = ["up", "down", "left", "right"]
        if preDirection == "up":
            self.direction.remove("down")
        if preDirection == "down":
            self.direction.remove("up")
        if preDirection == "left":
            self.direction.remove("right")
        if preDirection == "right":
            self.direction.remove("left")
        self.state = initState
        self.subModeSum = 0
        self.close = []
        self.open = []
        self.depth = depth
        self.path = []
        self.Fvalue = self.getFvalue(objState)
        self.blankColumn = 0
        self.blanlRow = 0
        self.objState = objState
        k = self.getBlankpos()
        self.blanlRow = k[0]
        self.blankColumn = k[1]

    def printSelf(self):
        i = 0
        j = 0
        while i < 3:
            while j < 3:
                print(self.state[i][j])
                j = j + 1
                if j == 3:
                    print('\n')
            i = i + 1

    def getFvalue(self, objState):
        i = 0
        j = 0
        wValue = 0
        while i < 3:
            while j < 3:
                if (self.state[i][j] == objState[i][j]):
                    wValue = wValue + 1
                j = j + 1
            i = i + 1
            j = 0
        return wValue + self.depth

    def generateSubmode(self):
        self.getBlankpos()
        subModeCollection = []
        tempMartix = []
        for i in self.direction:
            if i == "up":
                if self.blanlRow == 0:
                    continue
                else:
                    tempMartix = copy.deepcopy(self.state)
                    j = tempMartix[self.blanlRow - 1][self.blankColumn]
                    tempMartix[self.blanlRow][self.blankColumn] = j
                    tempMartix[self.blanlRow - 1][self.blankColumn] = ' '
                    k = State(tempMartix, self.objState, "up", (self.depth) + 1)
                    subModeCollection.append(k)
                    self.subModeSum = self.subModeSum + 1

            if i == "down":
                if self.blanlRow == 2:
                    continue
                else:
                    tempMartix = copy.deepcopy(self.state)
                    j = tempMartix[self.blanlRow + 1][self.blankColumn]
                    tempMartix[self.blanlRow][self.blankColumn] = j
                    tempMartix[self.blanlRow + 1][self.blankColumn] = ' '
                    subModeCollection.append(State(tempMartix, self.objState, "down", (self.depth) + 1))
                    self.subModeSum = self.subModeSum + 1
            if i == "left":
                if self.blankColumn == 0:
                    continue
                else:
                    tempMartix = copy.deepcopy(self.state)
                    j = tempMartix[self.blanlRow][self.blankColumn - 1]
                    tempMartix[self.blanlRow][self.blankColumn] = j
                    tempMartix[self.blanlRow][self.blankColumn - 1] = ' '
                    subModeCollection.append(State(tempMartix, self.objState, "left", (self.depth) + 1))
                    self.subModeSum = self.subModeSum + 1
            if i == "right":
                if self.blankColumn == 2:
                    continue
                else:
                    tempMartix = copy.deepcopy(self.state)
                    j = tempMartix[self.blanlRow][self.blankColumn + 1]
                    tempMartix[self.blanlRow][self.blankColumn] = j
                    tempMartix[self.blanlRow][self.blankColumn + 1] = ' '
                    subModeCollection.append(State(tempMartix, self.objState, "right", (self.depth) + 1))
                    self.subModeSum = self.subModeSum + 1
        return subModeCollection

    def getBlankpos(self):
        i = 0
        j = 0
        k = []
        while i < 3:
            while j < 3:
                if self.state[i][j] == ' ':
                    k.append(i)
                    k.append(j)
                    return k
                j = j + 1
            i = i + 1
            j = 0

    def getTheSuitableOne(self):
        i = self.open[0].Fvalue
        suitableObject = self.open[0]
        for j in self.open:
            if (j.Fvalue > i):
                suitableObject = j
                i = j.Fvalue
            else:
                continue
        return suitableObject

    def updatePath(self, state, nowdepth):
        if state.depth < nowdepth:
            for i in self.path:
                if state.depth <= i.depth:
                    self.path.remove(i)
        self.path.append(state)

    def updateOpen(self, state):
        sumStateCollections = state.generateSubmode()
        for i in sumStateCollections:
            self.open.append(i)

    def solveProblem(self, objectState) -> object:
        nowDepth = self.depth
        self.open.append(self)
        temp = self.open.pop()
        self.close.append(temp)
        if self.state == objectState:
            self.path.append(self)
            return self.path
        else:
            self.path.append(self)
        self.updateOpen(self.path[0])
        while 1:
            mostSuitaleState = self.getTheSuitableOne()
            self.close.append(self.open.pop(self.open.index(mostSuitaleState)))
            if mostSuitaleState.state == objectState:
                self.updatePath(mostSuitaleState, nowDepth)
                return self.path
            else:
                self.updatePath(mostSuitaleState, nowDepth)
                self.updateOpen(mostSuitaleState)