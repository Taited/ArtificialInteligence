from STATE import State

if __name__ == "__main__":
    initState = [[7, 5, 1], [4, 8, 3], [2, 6, ' ']]
    objState = [[' ', 1, 2], [3, 4, 5], [6, 7, 8]]
    state = State(initState, objState)
    path = state.solveProblem(objState)
    counter = 0
    route = []
    for mat in path:
        route.append(mat.state)
        for i in range(3):
            for j in range(3):
                print(route[counter][i][j], end=' ')
                if j == 2:
                    print('\n')
        print("\n\n\n")
        counter = counter + 1
    qwq = 1
