
"""
Elementary Operation on Matrices
"""

from fractions import Fraction as f


def smooth_zero(mat, tolerance = 10**-15):
	return [[ent if abs(ent) > tolerance else 0
				for ent in row] 
				for row in mat]

def to_fraction(mat):
	return [[f(i) for i in row] for row in mat]

def mat_print(mat):
	print()
	for i in mat:
		for j in i:
			print(j,end = "	")
		print()
	print()


def transposed(mat):
	return list(zip(*mat))

def dot(u, v):
	return sum(i*j for i, j in zip(u,v))
	

def mat_prod(iter_mat):

	def _mat_mul(mat_1, mat_2):
		mat_2 = transposed(mat_2)
		return [[dot(u, v)
					for v in mat_2]
					for u in mat_1]

	def main(iter_mat):
		iter_mat = iter(iter_mat)
		prod_mat = next(iter_mat, None)
		next_mat = next(iter_mat, None)
		while next_mat:
			prod_mat = _mat_mul(prod_mat, next_mat)
			next_mat = next(iter_mat, None)
		return prod_mat

	return main(iter_mat)


def mat_sum(iter_mat):
	return [[sum(ents) 
				for ents in zip(*rows)]
				for rows in zip(*iter_mat)]

def mat_mul(*iter_mat):
	return mat_prod(iter_mat)


def mat_add(*iter_mat):
	return mat_sum(iter_mat)


def mat_pow(mat, n):
	square = mat
	prod_list = []
	while n:
		if n&1:
			prod_list.append(square)
		square = mat_mul(square, square)
		n //= 2
	return mat_prod(prod_list)


def vec_sum(iter_vec):
	return [sum(row) for row in zip(*iter_vec)]


def vec_add(*iter_vec):
	return vec_sum(iter_vec)


def vec_mul(c, vec):
	return [c*ent for ent in vec]



def vec_sub(u, v):
	return [i - j for i, j in zip(u, v)]

def map_vec(*iter_mat):
	iter_mat = list(iter_mat)
	vec = iter_mat.pop()
	for mat in reversed(iter_mat):
		vec = [dot(row, vec) for row in mat]
	return vec



def map_veclist(mat, iter_vec):
	"""
	return [mat . v for v in iter(vec)]
	"""
	if not iter_vec: return []
	return [map_vec(mat, vec) 
				for vec in iter_vec]


def idm(n):
	return [[int(i == j) for i in range(n)]
						 for j in range(n)]

def elementary_vec(i, n):
	i -= 1
	return [int(j == i) for j in range(n)]

def zero(n):
	return [[ 0 for i in range(n)]
				for j in range(n)]

def numerical_kernel(mat, step = 10**(-12), threshold = 10**(-20)):

	def objective(mat, x):
		diff = map_vec(mat, x)
		return dot(diff, diff) / dot(x, x)

	def optimize(mat, x, ent):
		copy = x[:]
		old_val = objective(mat, copy)
		copy[ent] += step
		new_val = objective(mat, copy)
		return x[ent] - 0.5*(new_val - old_val)/step, min(old_val, new_val)

	def main(mat):
		mat = to_fraction(mat)
		x = [f(1) for i in mat[0]]
		score = 1
		for i in range(30000):
			if score < threshold:
				break
			for ent in range(len(x)):
				x[ent], score = optimize(mat, x, ent)

		return x

	return main(mat)
