import sys

def row(puzzle, x):
#This function takes the lines as a list and assigns them to numbers 1-9. Then makes them list of 9 numbers by splitting by the space between them.
    with open(puzzle, 'r') as file:
        rowvalue = file.readlines()
    rows = rowvalue[x-1].split()
    return rows

def column(puzzle, x):
#It function the row lists' xth element as an element of the column lists.
    columns = []
    for i in range(1, 10):
        columns.append(row(puzzle, i)[x-1])
    return columns

def subgrid(puzzle, subgridNum):
#This function makes the 3x3 subgrids' lists by their row and column number.
    rowStart = 3 * ((subgridNum - 1) // 3) + 1
    colStart = 3 * ((subgridNum - 1) % 3) + 1
    subgrids = []
    for i in range(rowStart, rowStart + 3):
        for j in range(colStart, colStart + 3):
            subgrids.append(row(puzzle, i)[j-1])
    return subgrids

def possible(puzzle, x, y):
#This function finds the possible values for the squares by comparing the lists.
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rowValues = [int(val) for val in row(puzzle, x)]
    columnValues = [int(val) for val in column(puzzle, y)]
    subgridValues = [int(val) for val in subgrid(puzzle, (x - 1) // 3 * 3 + (y - 1) // 3 + 1)]
    usedValues = rowValues + columnValues + subgridValues
    possibleNumbers = list(set(numbers) - set(usedValues))
    return possibleNumbers

def solvingAndWriting(puzzle, output):
#This function checks if the number is zero and if there is one possibility for that square then changes the list by that number.
#I couldn't make it work for 4 days.
    step = 1
    with open(output, 'w') as file:
        y = 1
        x = 1
        if y > 9:
            x += 1
            y = 1
        if len(possible(puzzle, x, y)) == 1 and row(puzzle, x)[y] == 0:
            puzzle_data = list(row(puzzle, x))
            puzzle_data[y] = str(possible(puzzle, x, y)[0])
            file.write("-" * 18 + "\n")
            file.write("Step " + str(step) + " - " + str(possible(puzzle, x, y)[0]) + " @ R" + str(x) + "C" + str(y) + "\n")
            for rowNumber in range(1, 10):
                file.write(str(row(puzzle, rowNumber)) + "\n")
            y += 1
            step += 1

def main():
    puzzle = sys.argv[1]
    output = sys.argv[2]
    solvingAndWriting(puzzle, output)

if __name__ == "__main__":
    main()