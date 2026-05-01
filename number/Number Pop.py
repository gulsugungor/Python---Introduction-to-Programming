import sys

game = sys.argv[1]

def editGame(filename):
    #Splits the txt file to rows and columns.
    with open(filename, 'r') as file:
        return [list(map(int, line.split())) for line in file.readlines()]

def printGame(board):
    #Prints every element in the rows one by one.
    for row in board:
        print(" ".join(map(str, row)))

def checkNeighbors(board, row, col):
    #Takes the value in the cell and checks if the neighbor cells has the same value with the cell.
    value = board[row][col]
    neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

    for r, c in neighbors:
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == value:
            return True

    return False

def deleteColumns(board):
    #When a column is empty, deletes the column.
    emptyColumn = [all(row[c] == ' ' for row in board) for c in range(len(board[0]))]
    for c in reversed(range(len(board[0]))):
        if emptyColumn[c]:
            for r in range(len(board)):
                del board[r][c]

def editBoard(board, row, col):
    value = board[row][col]
    cellsWillBeDeleted = set([(row, col)])

    def selectCells(r, c):
        #Selects the neighbors.
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and (r, c) not in cellsWillBeDeleted and board[r][c] == value:
            cellsWillBeDeleted.add((r, c))
            selectCells(r-1, c)
            selectCells(r+1, c)
            selectCells(r, c-1)
            selectCells(r, c+1)

    for c in range(len(board[0])):
        selectCells(row, c)

    for r in range(len(board)):
        selectCells(r, col)

    if len(cellsWillBeDeleted) >= 2:
        #If there are two neighbors that has the same value, deletes the cells.
        for r, c in cellsWillBeDeleted:
            board[r][c] = ' '

        for c in range(len(board[0])):
            #Counts the cells that will be deleted in one movement.
            otherCells = [board[r][c] for r in range(len(board) - 1, -1, -1) if board[r][c] != ' ']
            cellCount = len(board) - len(otherCells)

            for r in range(len(board) - 1, -1, -1):
                if r < cellCount:
                    board[r][c] = ' '
                else:
                    board[r][c] = otherCells[len(board) - 1 - r]

        deleteColumns(board)

def scoring(value, deletedCells):
    #Calculates the score with the count of the deleted cells and the cell value.
    return value * deletedCells

def gameOver(board):
    for r in range(len(board)):
        for c in range(len(board[0])):
            value = board[r][c]

            if value != ' ':
                neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                for row, col in neighbors:
                    if 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == value:
                        return False

    return True

board = editGame(game)
score = 0

printGame(board)
print("Score:", score)

while not gameOver(board):

    rowIndex, colIndex = map(int, input("Please enter a row and a column number: ").split())

    if 0 <= rowIndex - 1 < len(board) and 0 <= colIndex - 1 < len(board[0]):
        value = board[rowIndex - 1][colIndex - 1]
        editBoard(board, rowIndex - 1, colIndex - 1)

        deletedCells = sum(1 for row in board for cell in row if cell == ' ')
        score += scoring(value, deletedCells)
        deleteColumns(board)
        deletedCells = 0

    else:
        print("Please enter a correct size!")

    if not any(cell == ' ' for row in board for cell in row):
        print("No movement happened, try again")

    #Prints the board after the move.
    printGame(board)
    print("Score:", score)

print("Game over!")

