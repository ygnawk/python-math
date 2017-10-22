import functools

def all_list(size, p):

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



def index_permute(n):

	def _permute(l, index):
		if index == len(l): return [l[:]]
		solutions = []
		for i in range(index, len(l)):
			l[index], l[i] = l[i], l[index]
			# no need to copy l 
			# since the entries after index
			# remain after index
			solutions.extend(_permute(l, index+1))
		return solutions

	return _permute([i for i in range(n)], 0)


def permute(n):

	def _permute(l, index):
		if index == len(l): 
			yield l[:]
			return
		solutions = []
		for i in range(index, len(l)):
			l[index], l[i] = l[i], l[index]
			for i in _permute(l, index+1):
				yield i

	return _permute([i for i in range(n)], 0)


@functools.lru_cache(None)
def fact(n):

	return fact(n-1) * n

def prod(l):
	p = 1
	for i in l:
		p *= i
	return p

def choose(n, k):
	return fact(n)/(fact(n-k)*fact(k))

def permute(n, k):
	return fact(n)/fact(n-k)


def count_multiset(n, k):
	return choose(n+k-1, n)



