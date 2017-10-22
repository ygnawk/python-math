import gaussian_elimination as ge

def recurse(size, p):

	def _recurse(ent_list, pos):
		if pos == size:
			yield ent_list
			return
		for ent in range(p):
			ent_list[pos] = ent
			for i in _recurse(ent_list.copy(), pos + 1):
				yield i

	def main(size, p):
		ent_list = [0]*size
		pos = 0
		return _recurse(ent_list, pos)

	return main(size, p)


def recurse_matrix(dim, p):
	length = dim*dim
	for tup in recurse(dim*dim, p):
		yield [tup[i:i+dim] for i in range(0, length, dim)]

dim = 2
for p in range(2,12):
	a = sum(1 for mat in recurse_matrix(dim, p) if ge.det(mat)%p == 1)
	b = sum(1 for mat in recurse_matrix(dim, p) if ge.det(mat)%p != 0)
	print(p, b/a, a, b, flush = True)


print(7*23/24)