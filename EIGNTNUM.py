from STATE2 import State2
from Astar import *
from BFS import *

# 判断是否有解
def hasSolve(target, origate):
    targetVer = getreVersNum(target)
    orinateVer = getreVersNum(origate)
    if (targetVer % 2 != orinateVer % 2):
        return False
    else:
        return True

# 获取逆序数
def getreVersNum(state):
    sum = 0
    for i in range(0, len(state)):
        if (state[i] == 0):
            continue
        else:
            for j in range(0, i):
                if (state[j] > state[i]):
                    sum += 1
    return sum


def transistion(matix):
    temp = []
    for i in range(3):
        for j in range(3):
            if matix[i][j] == ' ':
                temp.append(0)
            else:
                temp.append(matix[i][j])

    return temp


if __name__ == "__main__":
    ManhattanList = [[0, 1, 2, 1, 2, 3, 2, 3, 4], [1, 0, 1, 2, 1, 2, 3, 2, 3], [2, 1, 0, 3, 2, 1, 4, 3, 2],
                     [1, 2, 3, 0, 1, 2, 1, 2, 3], [2, 1, 2, 1, 0, 1, 2, 1, 2], [3, 2, 1, 2, 1, 0, 3, 2, 1],
                     [2, 3, 4, 1, 2, 3, 0, 1, 2], [3, 2, 3, 2, 1, 2, 1, 0, 1], [4, 3, 2, 3, 2, 1, 2, 1, 0]]
    temp1 = [2, 8, 3, 1, 6, 4, 7, 0, 5]
    temp2 = [1, 2, 3, 8, 0, 4, 7, 6, 5]
    initState = [[7, 5, 1], [4, 8, 3], [2, 6, ' ']]
    objState = [[4, ' ', 1], [3, 7, 5], [2, 6, 8]]
    stateList = transistion(objState)
    flag = 3
    path = []
    if hasSolve(transistion(initState), transistion(objState)):
        print("有解")
        if flag == 1:
            state = Astar(initState, objState, stateList=stateList, Manhattan=ManhattanList)
            path = state.solveproblemByAstar(objState)
        if flag == 2:
            state = BFS(initState, objState, stateList=stateList)
            path = state.solveProblemByBFS(objState)
        if flag == 3:
            state = State2(initState, objState, stateList=stateList)
            path = state.solveProblem(objState)
        j = 0
        k = 0
        len_1 = len(path) - 2

        while len_1 >= 0:
            i = path[len_1]
            while j < 3:
                while k < 3:
                    print(i[j][k], end=' ')
                    k = k + 1
                    if (k == 3):
                        print('\n')
                k = 0
                j = j + 1
            print("\n\n\n")
            j = 0
            k = 0
            len_1 = len_1 - 1
        print("使用的时间为：" + str(path[len(path) - 1]), "S")
    else:
        print("无解")
