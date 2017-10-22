

import gaussian_elimination as ge
import vector_matrices as vm
import basis_manipulation as bm
import orthogonal_projection as op



def jordan_basis(mat):
	"""
	returns the jordan basis of mat
	as a list of vectors

	only works if mat is nilpotent
	"""

	def _exponentiate(mat):
		"""
		returns a list of matrices M
		such that M[i] = mat^i
		"""
		n = len(mat)
		prod = vm.idm(n)
		powers = []
		for i in range(n + 1):
			powers.append(prod)
			prod = vm.mat_mul(prod, mat)
		return powers

	def main(mat):
		mat = vm.to_fraction(mat)
		zero = vm.zero(len(mat))
		powers = _exponentiate(mat)
		kernels = [ge.kernel(mat) for mat in powers]
		_extend = bm.basis_complement_III
		betas = []
		alphas = []

		nilpotence = powers.index(zero) # guaranteed to exist
										# since mat is nilpotent
		for exp in range(nilpotence, 0, -1):
			new_alphas = _extend(kernels[exp-1] + betas, kernels[exp])
			alphas.extend(new_alphas)
			betas.extend(new_alphas)
			betas = vm.map_veclist(mat, betas)

		return alphas

	return main(mat)



def jordan_similar(mat):
	"""
	returns a matrix P such that P^(-1) A P
	is in jordan canonical form
	"""

	def jordan_reductor(mat, vectors):
		"""
		use this to create a new matrix
		from the jordan basis of mat

		vectors = jordan_basis(mat)
		"""
		basis = []
		zero = [0] * len(mat[0])
		for vec in vectors:
			while vec != zero:
				basis.append(vec)
				vec = vm.map_vec(mat, vec)
		return basis

	def main(mat):
		vectors = jordan_basis(mat)
		return vm.transposed(jordan_reductor(mat, vectors))

	return main(mat)


def jordan_form(mat):
	t_mat = jordan_similar(mat)
	inv = ge.inverse(t_mat)
	return vm.mat_mul(inv, mat, t_mat)



def _triangularize(mat, n = 20):
	for i in range(n):
		q, r = op.decompose_QR(mat)
		mat = vm.mat_mul(r, q)
	mat = vm.smooth_zero(mat)
	return mat


def triangularize(mat, n = 20):
	qs = []
	for i in range(n):
		q, r = op.decompose_QR(mat)
		qs.append(q)
		mat = vm.mat_mul(r, q)
	mat = vm.smooth_zero(mat)
	return vm.mat_prod(qs), mat
