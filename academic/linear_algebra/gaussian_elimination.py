
from fractions import Fraction as f
import vector_matrices as vm



def _gauss_eliminate(mat):

	def inversions(permutation):
		"""
		returns the number of inversions in permutation
		"""
		n = len(permutation)
		return sum (1  
				for index, val_1 in enumerate(permutation)
				for val_2 in permutation[:index]
				if val_2 > val_1)
	 
	def sign(permutation):
		"""
		returns the sign of permuation
		"""
		even = lambda x: 1 if x&1 else -1
		return even(inversions(permutation))

	def first_non_zero(row):
		for index, val in enumerate(row):
			if val != 0:
				return index
		return 0

	def make_pivot(mat, r):
		for i in mat[r]:
			if i:
				mat[r] = vm.vec_mul(1 / i, mat[r])
				return i
		return 0

	def make_elementary_row(array, r):
		for index, row in enumerate(array):
			if index == r:
				continue
			scale = row[first_non_zero(array[r])]
			scaler = vm.vec_mul(-scale, array[r])
			array[index] = vm.vec_add(row, scaler)

	def main(mat):
		mat_det = 1
		mat = vm.to_fraction(mat)	
		for r in range(len(mat)):
			scale = make_pivot(mat, r)
			make_elementary_row(mat, r)
			mat_det *= scale
		return sorted(mat, reverse=True), -mat_det * sign(mat)

	return main(mat)



def det(mat):
	return _gauss_eliminate(mat)[1]


def gauss_eliminate(mat):
	return _gauss_eliminate(mat)[0]



def first_non_zero(row):
	for index, val in enumerate(row):
		if val != 0:
			return index
	return -1


def get_pivots(z_mat):
	return [first_non_zero(row) for row in z_mat]



def solve(mat, b = None):
	"""
	solves mat x = b. If b = None, solves mat x = 0.

	returns a sample solution, and the kernel of the matrix
	"""

	def find_base_sol(col, pivots, sol_dim):
		"""
		col is not a pivot
		pivots[i] = z_mat.index(e_i)

		returns v such that 
				z_mat . v = col
		"""

		sol = [0] * len(mat[0])
		for index, col_num in enumerate(pivots):
			if col_num != -1:
				sol[col_num] = col[index]
		return sol

	def find_kernel_vector(col, c, pivots, sol_dim):
		"""
		pivots[i] = z_mat.index(e_i)
		col is not a pivot
		z_mat[c] == col
		"""
		basis = find_base_sol(col, pivots, sol_dim)
		basis = [-ent for ent in basis]
		basis[c] = 1
		return basis


	def _kernel(z_mat, pivots):
		"""
		z_mat = gauss_eliminate(mat)
		"""
		sol_dim = len(z_mat[0])
		nonpivs = [c for c in range(sol_dim) 
							if c not in pivots]
		z_mat = vm.transposed(z_mat)
		return [find_kernel_vector(
					z_mat[col_num], col_num, pivots, sol_dim) 
					for col_num in nonpivs]

	def _solve(mat, b):
		"""
		solves mat x = b. 
		returns a sample solution and the kernel of mat

		any linear combination of kernel added to sample solution
		is another solution

		returns None, kernel(mat) if there is no solution
		"""
		for index, ent in enumerate(b):
			mat[index].append(ent)
		z_mat = gauss_eliminate(mat)
		target = [row.pop() for row in z_mat]
		pivots = get_pivots(z_mat)
		null_space = _kernel(z_mat, pivots)

		if -1 in pivots and pivots.index(-1) <= first_non_zero(col):
			return None, []

		return find_base_sol(target, pivots), null_space

	def main(mat, b):
		mat = vm.to_fraction(mat)
		if not b:
			z_mat = gauss_eliminate(mat)
			pivots = get_pivots(z_mat)
			return [0]*len(z_mat), _kernel(z_mat, pivots)
		return _solve(mat, b)

	return main(mat, b)


def kernel(mat):
	"""
	return the kernel of mat
	"""
	return solve(mat)[1]


def inverse(mat):
	"""
	computes exact inverse. No floating point shenanigans.
	"""
	def idm(n):
		return [tuple(int(i == j) 
					for i in range(n))
					for j in range(n)]

	def main(mat):
		n = len(mat)
		augmented_mat = gauss_eliminate(vm.transposed(mat + idm(n)))
		augmented_mat = vm.transposed(augmented_mat)
		# for a square matrix
		# this occurs if and only if 
		# idm(n) != augmented_mat[:n]
		# when there is no inverse
		if augmented_mat[n - 1][n - 1] == 0:
			return None
		return augmented_mat[n:]

	return main(mat)

def cofactor(mat, x, y):
	"""
	returns the cofactor matrix of mat at point x, y
	"""
	n = len(mat)
	return [[mat[i][j] 
				for j in range(n) if j != y]
				for i in range(n) if i != x]


def adjoint(mat):
	"""
	returns the classical adjoint matrix of mat
	"""
	n = len(mat)
	even = lambda x: 1 if x&1 else -1
	return [[even(i+j) * det(cofactor(mat,j,i))
				for j in range(n)]
				for i in range(n)]


def rank(mat):
	z_mat = gauss_eliminate(mat)
	pivots = get_pivots(z_mat)
	return sum(1 for i in pivots if i != -1)

