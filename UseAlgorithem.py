from STATE import State

if __name__ == "__main__":
    initState = [[2, 8, 3], [1, 6, 4], [7, ' ', 5]]
    objState = [[1, 2, 3], [7, 8, 4], [' ', 6, 5]]
    state = State(initState, objState)
    path = state.solveProblem(objState)
    j = 0
    k = 0
    for i in path:
        while j < 3:
            while k < 3:
                print(i.state[j][k], end=' ')
                k = k + 1
                if k == 3:
                    print('\n')
            k = 0
            j = j + 1
        print("\n\n\n")
        j = 0
        k = 0
