
# a matrix is a list of list of numbers

mat_1 = [
	[1, 2, 3],
	[4, 5, 6],
	[7, 8, 9]
]

mat_2 = [
	[4, 2, 3],
	[1, 0, 3],
	[2, 8, 4]
]

# a vector is a list of numbers

vec_1 = [1, 2, 3]
vec_2 = [2, 3, 4]


"""
VECTOR_MATRICES
"""

import vector_matrices as vm

# dot two vector together
dot_value = vm.dot(vec_1, vec_2)
print("dot(vec_1, vec_2) ==", dot_value)


# to print matrices, do
vm.mat_print(mat_1)

# find the transpose of a matrix
transpose = vm.transposed(mat_1)
vm.mat_print(transpose)


# multiply two or more matrices together
# (cannot numtiply a vector and a matrix. 
# that needs a different function.)
product = vm.mat_mul(mat_1, mat_2, mat_1)
vm.mat_print(product)


# multiply a chain of matrices
chain = [mat_1, mat_2, mat_1, mat_2]
product = vm.mat_prod(chain)
vm.mat_print(product)

# add two or more matrices together
summation = vm.mat_add(mat_1, mat_2)
vm.mat_print(summation)


# sum over a chain of matrices
chain = [mat_1, mat_2, mat_1, mat_2]
summation = vm.mat_sum(chain)
vm.mat_print(summation)


# add two vectors or more vectors
summation = vm.vec_add(vec_1, vec_2, vec_1)
print("vector sum ==", summation)

# add a chain of vectors
chain = [vec_1, vec_2]
summation = vm.vec_sum(chain)
print("vector sum ==", summation)


# multiply a matrix to a vector
mapped = vm.map_vec(mat_1, vec_1)
print("mapped vec ==", mapped)

# multiply a matrix to a list of vectors
mapped = vm.map_veclist(mat_1, [vec_1, vec_2])
print("mapped vectors are")
for vector in mapped:
	print(vector)


# create an n x n identity matrix
n = 3
vm.mat_print(vm.idm(n))

# create an n x n zero matrix
n = 3
vm.mat_print(vm.zero(n))


# returns n-dimensional e_i
n = 5
e_vec = vm.elementary_vec(3, n)
print("e_3 == ", e_vec)



"""
GAUSSIAN ELIMINATION
"""

import gaussian_elimination as ge

# returns an row-reduced echelon form of a matrix
z_mat = ge.gauss_eliminate(mat_1)
vm.mat_print(z_mat)

# for full rank matrices, this becomes the identity matrix
z_mat = ge.gauss_eliminate(mat_2)
vm.mat_print(z_mat)


# finds the determinant of a matrix
det = ge.det(mat_2)
print("determinant ==",det)

# solve Ax = b
# returns a sample solution
# and the basis of the solution set
# returns None, kernel(A) if there is no solution
sample, sol_set = ge.solve(mat_1)
print("a solution is", sample)
print("any linear of combination of the following vectors")
print("added to the sample solution is another solution:")
# the vector has a fraction in it. This is needed
# to maintain exactness. Floating points dont work here.
for vec in sol_set:
	print(vec)
print()


#returns the kernel of a matrix as a list of vectors
null_space = ge.kernel(mat_1)
for vec in null_space:
	print("the null space is", vec)



#computes the inverse of a matrix
# returns None if matrix is not invertible
inv = ge.inverse(mat_2)
vm.mat_print(inv)

inv = ge.inverse(mat_1)
print(inv)


# returns the adjoint matrix of mat
adj = ge.adjoint(mat_2)
vm.mat_print(adj)


# returns the rank of mat
rank = ge.rank(mat_1)
print("rank is", rank)


"""
ORTHOGONAL PROJECTION
"""

import orthogonal_projection as op

# normalize a vector
normal = op.normalize(vec_1)
print('the normal of vec_1 is', normal)


# find an orthogonal basis of the span of vectors
basis = op.orthogonal_basis([vec_1, vec_2])
print("the orthogonal basis vectors are")
for i in basis:
	print(i)
print()



# find an orthonormal basis of the span of vectors
basis = op.orthonormal_basis([vec_1, vec_2])
print("the orthonormal basis vectors are")
for i in basis:
	print(i)
print()

# find the QR decomposition of mat
q, r = op.decompose_QR(mat_1)
print("Q matrix is")
vm.mat_print(q)
print("R matrix is")
vm.mat_print(r)

# find the determinant by QR decomposition
# more numerically stable
det = op.det_QR(mat_1)
print("determinant is", det)
print(ge.det(mat_1))

# find least squares
# solves Ax = b numerically

A = [
	[1, 2, 3],
	[4, 1, 4],
	[5, 2, 7],
	[1, 3, 9],
]

b = [1,2,7,3]

solution = [float(i) for i in op.least_squares(A, b)]
print(solution)
print("solution is", solution)
prediction = vm.map_vec(A, solution)
print([float(i) for i in prediction])




"""
BASIS MANIPULATION
"""

import basis_manipulation as bm

vectors_1 = [
	[1,2,3,4,5],
	[2,3,4,5,1],
	[0,0,0,0,2],
	[4,6,8,9,10]
]

vectors_2 = [
	[3,5,7,9,6],
	[2,3,4,5,1],
	[4,5,1,2,5]
]

# finds the basis of the orthogonal space 
# of a given set of vectors
org_space = bm.orthogonal_space(vectors_1)
print("the basis of the orthogonal space is")
for vec in org_space:
	print(vec)


# finds a basis of vectors
basis = bm.basis(vectors_1)
print("the basis is")
for vec in basis:
	print(vec)

# find a linearly independent subset of vectors
# that spans vectors
basis = bm.preserved_basis(vectors_1)
print("the basis is")
for vec in basis:
	print(vec)


# finds a basis for the intersection of
# two vector spaces
intersection = bm.basis_intersection(vectors_1, vectors_2)
print("the basis of intersection is:")
for i in intersection:
	print(i)

# extends basis of vectors of R^n
basis = bm.basis_extension_IA(vectors_1)
basis = bm.basis_extension_IB(vectors_2)
print("the basis is")
for vec in basis:
	print(vec)

# extends basis of vectors_1 to basis of vectors_2
basis = bm.basis_extension_II(vectors_1, vectors_2)
basis = bm.basis_extension_III(vectors_1, vectors_2)
print("the basis is")
for vec in basis:
	print(vec)


# note that each basis_extension variation
# has a basis_complement variation that does 
# the same thing, but does not include
# the original vectors in its return value
bm.basis_complement_IA(vectors_2)
bm.basis_complement_IB(vectors_2)
bm.basis_complement_II(vectors_1, vectors_2)
bm.basis_complement_III(vectors_1, vectors_2)




"""
EIGEN STUFF
"""
# used for spectral theory stuff
# a work in progress also
import eigen_stuff as es



val, vec = es.principal_eigenpair(mat_1)
print("eigenvector == ", [float(i) for i in vec])
print("eigen value == ", float(val))


# get all eigenpairs of mat
vals = es.eigenpairs(mat_1)
print(vals)



"""
JORDAN FORM
"""

# a work in progress
# only works for nilpotent matrices
import jordan_form as jf

nil_mat = [
	[ 0, 0, 0, 0],
	[ 1, 0, 0, 0],
	[ 1, 4, 0, 0],
	[ 3, 2, 7, 0]
]


# returns the jordan basis of mat
# as a list of vectors
basis = jf.jordan_basis(nil_mat)
vm.mat_print(basis)

# returns the transformation matrix T
# such that inv(T). mat .T = jordan_form(T) 
t_mat = jf.jordan_similar(nil_mat)
vm.mat_print(t_mat)

# returns the jordan form of mat
j_mat = jf.jordan_form(nil_mat)
vm.mat_print(j_mat)


# get a matrix q (unitary) and mat (triangular) such that 
# 		q . mat . q^(-1) = mat_1
q, mat = jf.triangularize(mat_1)
vm.mat_print(mat)
vm.mat_print(vm.smooth_zero(vm.mat_mul(q, vm.transposed(q))))
vm.mat_print(vm.mat_mul(q, mat, vm.transposed(q)))

