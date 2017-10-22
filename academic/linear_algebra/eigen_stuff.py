
import vector_matrices as vm
import orthogonal_projection as op
import gaussian_elimination as ge
import jordan_form as jf

import math

def eigen_norm(mat, eigen_vec):
	bot = vm.dot(eigen_vec, eigen_vec)
	top = vm.map_vec(mat, eigen_vec)
	top = vm.dot(top, eigen_vec)
	return top/bot


def principal_eigenpair(mat, n = 64):
	"""
	using power iteration,
	computes the largest eigenvalue of mat
	and returns an eigenvector corresponding to it.
	"""
	vec_len = lambda v: vm.dot(v, v)

	mat = vm.to_fraction(mat)
	powered_mat = vm.mat_pow(mat, n)
	col_vecs = vm.transposed(powered_mat)

	eigenvec = max(col_vecs, key = vec_len)
	s = sum(eigenvec)

	eigenvec = [ent/s for ent in eigenvec]
	long_vec = vm.map_vec(mat, eigenvec)
	eigenval = vm.dot(long_vec, eigenvec) / vm.dot(eigenvec, eigenvec)
	return eigenval, eigenvec



def eigenpairs(mat):
	"""
	returns all eigenvalues, and eigenvectors of mat of mat
	"""

	def eigenvals(mat):
		qs, mat = jf.triangularize(mat)
		return [mat[i][i] for i in range(len(mat))]

	vals = eigenvals(mat)
	print(vals, flush = True)
	vecs = []
	for eigenval in vals:

		mat_copy = [row[:] for row in mat]
		for i in range(len(mat_copy)):
			mat_copy[i][i] -= eigenval
		kern = vm.numerical_kernel(mat_copy)
		vecs.append(kern)
		print(kern, flush = True)
	return vals, vecs

def eigenvals(mat):
	qs, mat = jf.triangularize(mat)
	vm.mat_print(qs)
	return [mat[i][i] for i in range(len(mat))]
