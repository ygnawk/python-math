import numpy as np
import math


def centralize(data):
	c = centroid(data)
	return [vec(point, c) for point in data]


def centroid(data):
	n = len(data)
	return [sum(row)/n for row in zip(*data)]


def dot(tup1: tuple, tup2: tuple):
	return sum(i*j for i,j in zip(tup1, tup2))


def vec_sum(vec_seq):
	return [sum(row) for row in zip(*vec_seq)]


def mat_mul(*mat_seq):

	def mul(matrix1, matrix2):
		m = len(matrix1)
		n = len(matrix2[0])

		matrix2 = zip(*matrix2)
		return [[dot(row_1, row_2)
					for row_1 in matrix1]
					for row_2 in matrix2]


	def main(mat_seq):
		iterator = (i for i in mat_seq)
		ret = next(iterator)
		for mat in iterator:
			ret = mul(ret, mat)
		return ret

	return main(mat_seq)



def mat_inv(matrix):
	inv = np.linalg.inv(matrix)
	return [[ent for ent in row] 
				 for row in inv]


def covariance_matrix(data):
	transposed = list(zip(*list(data)))
	div = len(data)**2
	return [[dot(row_1, row_2) / div
				for row_1 in transposed]
				for row_2 in transposed]


def eigenpairs(matrix):
	vals, vecs = np.linalg.eig(matrix)
	pairs = sorted(((c,v)
					for c, v in zip(vals, vecs)), 
					reverse = True)
	vals = [vals for vals, vec in pairs]
	vecs = [[ent for ent in row] 
				 for vals, row in pairs]
	return vals, vecs


def mat_sqrt(mat):
	vals, vecs = eigenpairs(mat)
	dim = len(vals)
	vecs = list(vecs)
	svals = [math.sqrt(i) for i in vals]
	sigma = [[svals[i] if i == j else 0 
				for i in range(dim)]
				for j in range(dim)]
	transposed = list(zip(*vecs))

	return mat_mul(vecs, sigma, transposed)


def mat_add(mat_1, mat_2):
	return [[ent_1 + ent_2
				for row_1, row_2 in zip(mat_1, mat_2)]
				for ent_1, ent_2 in zip(row_1, row_2)]


def mat_sum(mat_seq):
	mat_seq = list(mat_seq)
	return [vec_sum(row_seq) for row_seq in zip(*mat_seq)]


def vec(vec_1, vec_2):
	return [i - j for i, j in zip(vec_1, vec_2)]



def normalize(vec):
	l = math.sqrt(sum(i*i for i in vec))
	return [i/l for i in vec]

class linear_discriminant:
	"supervised dimensionality reduction"

	def __init__(self, data, target):
		self.data = data
		self.target = set(target)
		self.trained = False
		self.centroid = centroid(data)
		self.data_dict = {data_type : [x for x, y in zip(data, target) 
							if y == data_type]
							for data_type in self.target}



	def train(self):
		centroids_centralized = [vec(centroid(data), self.centroid)
									for key, data 
									in dict.items(self.data_dict)]
		b_matrix = covariance_matrix(centroids_centralized)
		w_matrix = mat_sum(covariance_matrix(centralize(data)) 
						for key, data 
						in dict.items(self.data_dict))

		sqrt_mat = mat_sqrt(b_matrix)
		inv_mat  = mat_inv(w_matrix)
		main_mat = mat_mul(sqrt_mat, inv_mat, sqrt_mat)

		vals, vecs = eigenpairs(main_mat)
		principal_vec = vecs[0]

		inverse = mat_inv(sqrt_mat)
		normal_vec = [dot(row, principal_vec) for row in inverse]
		
		self.trained = True
		self.normal = normal_vec
		x,y = normal_vec
		if x < 0:
			x, y = -x, -y

		self.principal_vec = normalize([x,y])


	def project_data(self):

		def orthogonal_project(vector, axis):
			length = dot(vector, axis)
			projection = [length*i for i in axis]
			return projection# vec(projection, vector)


		def main(self):
			if not self.trained:
				raise ValueError(
					'linear discriminant not trained')

			axis = self.principal_vec

			self.target = [
					orthogonal_project(vector, axis)
					for vector in self.data]
			return self.target

		return main(self)












