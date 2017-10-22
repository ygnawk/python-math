
class sudoku:

	def __init__(self, board):
		self.fixed = board
		self.board = [row[:] for row in board]
		self.solutions = []
		if not self.consistent:
			raise ValueError('board given inconsistent')

	def __str__(self):
		board = self.board
		end_line = "+" + "-------+" * 3
		lines = [end_line]
		for index, row in enumerate(board):
			left  = " ".join(str(i) for i in row[0:3])
			mid   = " ".join(str(i) for i in row[3:6])
			right = " ".join(str(i) for i in row[6:9])
			line = " | ".join([left, mid, right])
			lines.append("| " + line + " |")
			if index % 3 == 2: lines.append(end_line)
		ret_val = "\n".join(lines).replace("0", " ")
		return ret_val 

	@property
	def consistent(self):
		board = self.fixed
		for row in board:
			for i in range(1, 10):
				if row.count(i) > 1:
					return False

		for col in zip(*board):
			for i in range(1, 10):
				if col.count(i) > 1:
					return False
		head_xs = [0, 3, 6]
		head_ys = [0, 3, 6]
		for head_x in head_xs:
			for head_y in head_ys:
				taken = [False] * 10
				for ind_x in range(head_x, head_x + 3):
					for ind_y in range(head_y, head_y + 3):
						value = board[ind_x][ind_y] 
						if value and taken[value]:
							return False
						else:
							taken[value] = True
		return True


	def solve(self):


		def availables(board, i, j):
			avail = [True] * 10 # stores availability information
								# true at index i means that 
								# the number i can be filled in 
								# the box without causing an immediate contradiction
			head_x = 3 * (i // 3) # yields the top left corner 
			head_y = 3 * (j // 3) # of the box the entry is in
			for index in range(9):
				avail[board[i][index]] = False
				avail[board[index][j]] = False

			for ind_x in range(head_x, head_x + 3):
				for ind_y in range(head_y, head_y + 3):
					avail[board[ind_x][ind_y]] = False
			return avail

		def cycle(board):
			min_count = 10
			min_index = (10, 10)
			for i in range(9):
				for j in range(9):
					if not board[i][j]:
						avail = availables(board, i, j)
						count = avail.count(True)
						if min_count > count:
							min_count = count
							min_index = (i, j)
						if count == 1:   # if there is only one possibility
							board[i][j] = avail.index(True)
						elif count == 0: # there is no way the board can be filled
							return 0, min_index
			return min_count, min_index


		def complete(board):
			for row in board:
				for ent in row:
					if ent == 0:
						return False
			return True


		def master(stack, solutions):
			"""
			recursive methods would work but it's pretty inefficient
			stacks are much better
			"""
			while stack:
				board = stack.pop()
				min_count = 1
				while min_count == 1:
					min_count, min_index = cycle(board)

				if complete(board):
					solutions.append(board) # no need to make a copy
											# that is already done
											# when forked
				elif min_count > 0:
					i, j = min_index
					avail = availables(board, i, j)
					for value, free in enumerate(avail):
						if free:
							board_copy = [row[:] for row in board]
							board_copy[i][j] = value
							stack.append(board_copy)

		def main(self):
			stack = [self.board]
			master(stack, self.solutions)
			return [sudoku(i) for i in self.solutions]

		return main(self)


