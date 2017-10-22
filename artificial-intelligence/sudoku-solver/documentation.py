import sudoku_solver as ss

# make a new board
# uses a list of lists as data structure
new = [
	[5, 0, 8, 0, 7, 3, 1, 9, 0],
	[9, 0, 0, 6, 0, 0, 4, 0, 8],
	[0, 0, 0, 9, 0, 8, 0, 3, 5],

	[0, 7, 0, 0, 0, 0, 0, 6, 0],
	[0, 0, 2, 0, 0, 0, 9, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 8, 0],

	[1, 9, 0, 3, 6, 0, 0, 0, 0],
	[2, 0, 3, 0, 0, 7, 0, 0, 9],
	[0, 8, 7, 1, 9, 0, 3, 0, 4],
]

# greate a new game
game = ss.board(new)

# return the solutions
solutions = game.solve()

#there may be multiple solutions
print("SOLUTIONS: ")
for solved in solutions:
	print(solved)