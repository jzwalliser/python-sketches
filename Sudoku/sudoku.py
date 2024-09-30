def dfs(sudoku):
    pos = sudoku.find("0")
    #print(sudoku)
    if pos == -1:
        print(sudoku)
        return
    else:
        row = pos // 9
        column = pos % 9
        blkrow = row // 3 * 3
        blkcol = column // 3 * 3
        candidate = [True] * 10
        for i in range(9):
            candidate[int(sudoku[row * 9 + i])] = False
        for i in range(9):
            candidate[int(sudoku[i * 9 + column])] = False
            #print(i * 9 + column)
            #print(candidate)
        for i in range(3):
            for j in range(3):
                candidate[int(sudoku[blkrow * 9 + blkcol + i * 9 + j])] = False
        for i in range(1,10):
            if candidate[i] == True:
                dfs(sudoku[0:pos] + str(i) + sudoku[pos + 1:])

#dfs("412560879086472500053001024075249386029605140364718290530900760008127450247056918")

dfs("0"*81)

def print_sud(string):
    for i in range(9):
        print(string[i * 9:i * 9 + 9])
