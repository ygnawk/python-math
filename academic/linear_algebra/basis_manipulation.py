"""
For extending basis of one space to another, etc.
"""

import gaussian_elimination as ge
import vector_matrices as vm



def orthogonal_space(vectors):
	"""
	returns a list of vectors [u] such that
	for vec in vectors dot(vec, u) == 0.
	"""

	return ge.kernel(vectors)



def basis(vectors):
	"""
	returns a basis that spans the given vectors
	"""
	basis = ge.gauss_eliminate(vectors)
	zero = [0]*len(vectors[0])
	if zero in basis:
		i = basis.index(zero)
		basis = basis[:i]
	return basis



def preserved_basis(vectors):	
	z_mat = ge.gauss_eliminate(vm.transposed(vectors))
	return [vectors[i] 
				for i in ge.get_pivots(z_mat) 
				if i != -1]


def basis_intersection(vectors_1, vectors_2):
	"""
	returns the basis of all vectors that
	are both in the span of vectors_1 and vectors_2
	"""
	kernel_1 = ge.kernel(vectors_1)	
	kernel_2 = ge.kernel(vectors_2)
	if kernel_1 or kernel_2:
		return ge.kernel(kernel_1 + kernel_2)
	else:
		return vm.idm(len(vectors_1[0]))



def basis_complement_IA(vectors):
	"""
	extends vectors to a basis of R^n
	"""
	return ge.kernel(vectors)


def basis_complement_IB(vectors):
	"""
	extends vectors to a basis of R^n
	"""
	l = len(vectors[0])
	basis = vm.idm(l)
	mat = vm.transposed(vectors + basis)
	z_mat = vm.transposed(ge.gauss_eliminate(mat))
	return [mat[col_num] 
				for col_num in ge.get_pivots(z_mat)
				if col_num != -1]




def basis_complement_II(vectors_1, vectors_2): 
	"""
	extends the basis of vectors_1 into a basis of vectors_2
	"""
	return basis_intersection(
				vectors_2, 
				ge.kernel(vectors_1))



def basis_complement_III(vectors_1, vectors_2): 
	"""
	extends the basis of vectors_1 into a basis of vectors_2
	"""
	n = len(vectors_1)
	combined = vectors_1 + vectors_2
	z_mat = ge.gauss_eliminate(vm.transposed(combined))
	pivots = ge.get_pivots(z_mat)
	return [combined[i] for i in pivots if i != -1 if i >= n]



def basis_extension_IA(vectors):
	"""
	extends vectors to a basis of R^n
	"""
	return vectors + basis_complement_IA(vectors)



def basis_extension_IB(vectors):
	"""
	extends vectors to a basis of R^n
	"""
	l = len(vectors[0])
	basis = vm.idm(l)
	mat = vm.transposed(vectors + basis)
	z_mat = ge.gauss_eliminate(mat)
	mat = vm.transposed(mat)
	return [mat[col_num] 
				for col_num in ge.get_pivots(z_mat)
				if col_num != -1]




def basis_extension_II(vectors_1, vectors_2): 
	"""
	extends the basis of vectors_1 into a basis of vectors_2
	"""
	return vectors_1 + basis_intersection(
							ge.kernel(vectors_1),
							vectors_2)



def basis_extension_III(vectors_1, vectors_2): 
	"""
	extends the basis of vectors_1 into a basis of vectors_2
	"""
	combined = vectors_1 + vectors_2
	z_mat = ge.gauss_eliminate(vm.transposed(combined))
	pivot = ge.get_pivots(z_mat)
	return [combined[i] for i in pivot if i != -1]

