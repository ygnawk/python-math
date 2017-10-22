

FULL_ROW = [i for i in range(1, 10)]
FULL_SET = set(FULL_ROW)


def iterable(obj):
	return '__iter__' in dir(obj)

def flatten(self):
	flat = []
	for item in self:
		if iterable(item):
			flat.extend(flatten(item))
		else:
			flat.append(item)
	return flat


def has_duplicates(check_list, exceptions = [0]):
	new = [i for i in check_list
			  if i not in exceptions]
	return len(set(new)) != len(new)


class board:

	__slots__ = ('board', 'fixed')

	def __init__(self, nested_list):
		self.board = [row[:] for row in nested_list]
		self.fixed = nested_list
		if not self.consistent:
			raise ValueError('board given is not consistent')


	def __str__(self):
		end_line = "+" + "-------+" * 3
		lines = [end_line]
		for index, row in enumerate(self.board):
			left  = " ".join(str(i) for i in row[0:3])
			mid   = " ".join(str(i) for i in row[3:6])
			right = " ".join(str(i) for i in row[6:9])
			line = " | ".join([left, mid, right])
			lines.append("| " + line + " |")
			if index % 3 == 2: lines.append(end_line)
		ret_val = "\n".join(lines).replace("0", " ")
		return ret_val + "\n\n\n"


	@property
	def consistent(self):
		for row in self.board:
			if has_duplicates(row):
				return False
		for col in list(zip(*self.board)):
			if has_duplicates(col):
				return False
		for i in range(0, 9, 3):
			for j in range(0, 9 ,3):
				if has_duplicates(self.box(i, j)):
					return False
		return True


	@property
	def solved(self):
		for row in self.board:
			if set(row) != FULL_SET:
				return False
		for col in list(zip(*self.board)):
			if set(col) != FULL_SET:
				return False
		for i in range(0, 9, 3):
			for j in range(0, 9 ,3):
				if set(self.box(i, j)) != FULL_SET:
					return False
		return True


	def box(self, i, j):
		h_r, h_c = 3*(i//3), 3*(j//3)
		nested = [self.board[row][h_c: h_c + 3]
				 for row in range(h_r, h_r + 3)]
		return flatten(nested)


	def poss(self, i, j):
		row = self.board[i]
		col = list(zip(*self.board))[j]
		box = self.box(i, j)
		joined = row + box + list(col)
		return [ i for i in FULL_ROW 
					if i not in joined]


	def ent_reduce(self, i, j):
		poss = self.poss(i, j)
		if len(poss) == 1:
			self.board[i][j] = poss[0]
			return True
		elif len(poss) == 0:
			return None
		return False


	def reduce(self):
		changed = False
		for i in range(9):
			for j in range(9):
				if self.board[i][j] != 0: continue
				new_change = self.ent_reduce(i, j)
				if new_change == None: return None
				changed = new_change or changed
		return changed


	@property
	def min_poss(self):
		"""
		return the index of minimum possibility
		"""
		min_len = 10
		min_ind = 0,0
		for i in range(9):
			for j in range(9):
				if self.board[i][j] != 0: continue
				poss = self.poss(i, j)
				if len(poss) < min_len:
					min_len = len(poss)
					min_ind = i, j
		return min_ind


	def fork(self):
		i, j = self.min_poss
		poss = self.poss(i, j)
		solutions = []
		for ent in poss:
			new = [row[:] for row in self.board]
			new[i][j] = ent
			new_board = board(new)
			solutions.extend(new_board.solve())
		return solutions


	def solve(self):
		"""
		return a list of solutions
		"""
		changed = self.reduce()
		while changed:
			changed = self.reduce()
			if changed == None: return [] # there is no solution
		if changed == None: return []
		if self.solved: return [board(self.board)]
		return self.fork() 			# there may be many solutions
									# god bless mutual recursions






