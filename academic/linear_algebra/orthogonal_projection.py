
import math

import vector_matrices as vm
import gaussian_elimination as ge
import basis_manipulation as bm



def proj(x, vectors):
	"""
	return the projection x onto vectors
	"""
	vectors = orthonormal_basis(vectors)
	coefficients = [vm.vec_mul(vm.dot(x, v)/vm.dot(y, v), y)
											for y in vectors]
	return vec_sum(coefficients)


def normalize(x):
	size = math.sqrt(vm.dot(x, x))
	return vm.vec_mul(1/size, x)


def orthogonal_basis(vectors):
	"""
	returns an orthogonal basis of the span of vectors
	"""

	def _proj(x, vectors):
		"""
		returns the projection of x onto the orthogonal space of
		vectors assuming that vectors form an orthogonal set
		"""
		coefficients = [vm.vec_mul(-vm.dot(x, y)/vm.dot(y, y), y)
							for y in vectors]
		coefficients.append(x)
		return vm.vec_sum(coefficients)

	def main(vectors):
		vectors = vm.to_fraction(vectors)
		vectors = bm.basis_extension_IB(vectors)
		basis = []
		for vec in vectors:
			b = _proj(vec, basis)
			basis.append(b)
		return basis

	return main(vectors)


def orthonormal_basis(vectors):
	"""
	returns an orthogonal basis of the span of vectors
	"""
	basis = orthogonal_basis(vectors)
	return [normalize(i) for i in basis]



def decompose_QR(mat):
	"""
	returns a unitary matrix q and an upper trinagular matrix r
	such that vm.mat_mul(q, r) = mat
	"""
	n = len(mat)
	mat = vm.transposed(mat)
	q = orthonormal_basis(mat)
	r = [[vm.dot(u, v)
			for v in mat]
			for u in q]
	return vm.transposed(q), vm.smooth_zero(r)


def det_QR(mat):
	"""
	returns the determinant of mmat
	"""
	s = 1
	r = decompose_QR(mat)[1]
	for i in range(len(r)):
		s *= r[i][i]
	return s


def least_squares(data, target):
	"""
	find a vector x that minimizes
		|| data x - target ||^2
	"""
	trans = vm.transposed(data)
	covar = ge.inverse(vm.mat_mul(trans, data))


	vec = vm.map_vec(trans, target)
	vec = vm.map_vec(covar, vec)
	return vec


def reflect(x, v):
	vec = [ normalize(x) ] + [0] * (len(x) - 1)
	return vec_sub(x, vec)
