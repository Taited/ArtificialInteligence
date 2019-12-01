from STATE import State

if __name__ == "__main__":
    initState = [[7, 5, 1], [4, 8, 3], [2, 6, ' ']]
    objState = [[' ', 1, 2], [3, 4, 5], [6, 7, 8]]
    state = State(initState, objState)
    path = []
    path = state.solveProblem(objState)

    j = 0
    k = 0
    len_1 = len(path) - 1

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
