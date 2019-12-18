import copy
import time
class BFS():
    def __init__(self, initState, objState, preDirection=None, depth=0,prestate=None,stateList=None):
        self.direction = ["up", "down", "left", "right"]
        if preDirection=="up":
            self.direction.remove("down")
        if preDirection == "down":
            self.direction.remove("up")
        if preDirection=="left":
            self.direction.remove("right")
        if preDirection=="right":
            self.direction.remove("left")
        self.state = initState;
        self.subModeSum = 0
        self.close = []
        self.open = []
        self.depth = depth
        self.path = []
        self.stateList = stateList
        self.Fvalue = self.getFvalue(objState)
        self.blankColumn=0
        self.blanlRow=0
        self.objState=objState
        k=self.getBlankpos()
        self.blanlRow=k[0]
        self.blankColumn=k[1]
        self.preState=prestate
        self.pathDepth=33

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
    def matixToList(self,matix):
        list=[]
        for i in range(0,3):
            for j in range(0,3):
                list.append(matix[i][j])
        return list

    def getFvalue(self, objState):
        # i = 0
        # j = 0
        # wValue = 0
        # while i < 3:
        #     while j < 3:
        #         if (self.state[i][j] != objState[i][j]):
        #             wValue = wValue + 1
        #         j=j+1
        #     i=i+1
        #     j=0
        # return wValue + self.depth
        list=self.matixToList(self.state)
        wValue = 0
        for i in range(0,9):
            for j in range(0,9):
                if(self.stateList[j]==list[i]):
                    if(j-i<0):
                        wValue=wValue+(j-i)*(-1)
                    else:
                        wValue = wValue + j - i
        return wValue + self.depth

    def genneratePath(self,finaState):
        path=[]
        temp = copy.deepcopy(finaState)
        while 1:
            if temp.state!=self.state:
                path.append(temp.state)
                temp=temp.preState
            else:
                path.append(temp.state)
                return path

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
                    j = tempMartix[self.blanlRow -1][self.blankColumn]
                    tempMartix[self.blanlRow][self.blankColumn] = j
                    tempMartix[self.blanlRow - 1][self.blankColumn] = ' '
                    k = BFS(tempMartix, self.objState, "up", (self.depth) + 1,stateList= self.stateList)
                    k.preState = self
                    subModeCollection.append(k)
                    self.subModeSum = self.subModeSum + 1
                    k.preState=self

            if i == "down":
                if self.blanlRow == 2:
                    continue
                else:
                    tempMartix = copy.deepcopy(self.state)
                    j = tempMartix[self.blanlRow + 1][self.blankColumn]
                    tempMartix[self.blanlRow][self.blankColumn] = j
                    tempMartix[self.blanlRow + 1][self.blankColumn] = ' '
                    k=BFS(tempMartix, self.objState, "down", (self.depth) + 1,stateList= self.stateList)
                    k.preState = self
                    subModeCollection.append(k)
                    self.subModeSum = self.subModeSum + 1
                    k.preState = self
            if i == "left":
                if self.blankColumn == 0:
                    continue
                else:
                    tempMartix = copy.deepcopy(self.state)
                    j = tempMartix[self.blanlRow][self.blankColumn - 1]
                    tempMartix[self.blanlRow][self.blankColumn] = j
                    tempMartix[self.blanlRow][self.blankColumn - 1] = ' '
                    k=BFS(tempMartix, self.objState, "left", (self.depth) + 1,stateList= self.stateList)
                    k.preState = self
                    subModeCollection.append(k)
                    self.subModeSum = self.subModeSum + 1

            if i == "right":
                if self.blankColumn == 2:
                    continue
                else:
                    tempMartix = copy.deepcopy(self.state)
                    j = tempMartix[self.blanlRow][self.blankColumn + 1]
                    tempMartix[self.blanlRow][self.blankColumn] = j
                    tempMartix[self.blanlRow][self.blankColumn + 1] = ' '
                    k=BFS(tempMartix, self.objState, "right", (self.depth) + 1,stateList= self.stateList)
                    k.preState = self
                    subModeCollection.append(k)
                    self.subModeSum = self.subModeSum + 1

        return subModeCollection

    def getBlankpos(self):
        i = 0
        j = 0
        k=[]
        while i < 3:
            while j < 3:
                if self.state[i][j] == ' ':
                    k.append(i)
                    k.append(j)
                    return k
                j=j+1
            i=i+1
            j=0
    def updateOpen(self, state):
        jump=0
        sumStateCollections = state.generateSubmode()
        for i in sumStateCollections:
            for k in self.close:
                if k.state==i.state:
                    jump=1;
                    break
            for k in self.open:
                if k.state == i.state:
                    jump = 1;
                    break
            if jump==1:
                jump=0
                continue
            self.open.append(i)

    def solveProblemByBFS(self, objectState):
        start = time.clock()
        nowDepth = self.depth
        self.close.append(self)
        if self.state == objectState:
            self.path.append(self)
            return self.path
        else:
            self.path.append(self)
        self.updateOpen(self.path[0])
        while 1:
            mostSuitaleState = self.open.pop(0)
            self.close.append(mostSuitaleState)
            if mostSuitaleState.state == objectState:
                processTime=time.clock()-start
                path = self.genneratePath(mostSuitaleState)
                path.append(processTime)
                return path
            else:
                self.updateOpen(mostSuitaleState)





