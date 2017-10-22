import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



def centroid(data):
	return tuple(sum(i)/len(i) for i in zip(*data))


def translate(data):
	# translate all data points to its centroid
	cent = centroid(data)
	diff = (lambda tup1, tup2:
				tuple(i - j for i, j in zip(tup1, tup2)))
	return [diff(i, cent) for i in data]


def dot(tup1: tuple, tup2: tuple):
	return sum(i*j for i,j in zip(tup1, tup2))


def mat_mul(mat_1, mat_2):
	m = len(mat_1)
	n = len(mat_2[0])
	mat_2 = list(zip(*mat_2))
	return [[dot(u, v)
				for v in mat_2]
				for u in mat_1]


def covariance_matrix(data):
	matrix = mat_mul(list(zip(*data)), data)
	n = len(matrix)
	l = len(data)
	return [[matrix[i][j]/l
				for j in range(n)]
				for i in range(n)]

def idm(n):
	# returns an n x n identity matrix
	return [[int(i == j) 
				for j in range(n)] 
				for i in range(n)]


def matrix_pow(matrix, times):
	result = idm(len(matrix))
	while times:
		if (times % 2):
			result = mat_mul(result, matrix)
		matrix = mat_mul(matrix, matrix)
		times //= 2
	return matrix


def map_matrix(matrix, vector):
	#map a vector using a matrix map (matrix multiplication)
	n = len(matrix)
	return tuple(dot(matrix[i], vector)
					for i in range(n))


def normalize(vector):
	length = sum(i**2 for i in vector) ** 0.5
	return tuple(i/length for i in vector)


def principal_component(data):
	#returns eigen pairs of the data
	data = np.array(translate(data))
	cov = np.array(covariance_matrix(data))
	vals, vecs = np.linalg.eig(cov)
	indexed_vals = sorted( ((val,index) 
							for index, val in enumerate(vals)), 
							reverse = True)
	vec_list = np.transpose(vecs)
	return [(val, vec_list[i]) for val,i in indexed_vals]


def raw_pca(data):
	cov = np.array(covariance_matrix(data))
	vals, vecs = np.linalg.eig(cov)
	indexed_vals = sorted(((val, index) 
							for index,val in enumerate(vals)), 
							reverse = True)
	vec_list = np.transpose(vecs)
	return [(val, vec_list[i]) for val,i in indexed_vals]


def plot3d(data):
	
	fig = plt.figure()
	ax = Axes3D(fig)
	i, j, k = centroid(data)
	eigenpairs = principal_component(data)

	for val, eigenvec in eigenpairs:
		line = np.linspace(-np.sqrt(val), np.sqrt(val), 3)
		x, y, z = eigenvec
		ax.plot(i + x*line,
				j + y*line,
				k + z*line, 
				label = 'principal_component', 
				color = 'Blue',
				linewidth = 1.2, 
				linestyle = '-')
	xs, ys, zs = list(zip(*data))
	ax.scatter(xs, ys, zs, c = 'c', marker = 'x')
	scale = 2*np.sqrt(max(val for val, row in eigenpairs))
	ax.set_xlim3d(i - scale, i + scale)
	ax.set_ylim3d(j - scale, j + scale)
	ax.set_zlim3d(k - scale, k + scale)
	plt.show()


def raw_plot(data):
	fig = plt.figure()
	ax = Axes3D(fig)
	i, j, k = centroid(data)
	eigenpairs = raw_pca(data)

	for val, eigenvec in eigenpairs:
		line = np.linspace(-np.sqrt(val), np.sqrt(val), 3)
		x, y, z = eigenvec
		ax.plot(i + x*line,
				j + y*line,
				k + z*line, 
				label = 'principal_component', 
				color = 'Blue',
				linewidth = 1.2,
				linestyle = '-')

	xs, ys, zs = list(zip(*data))
	ax.scatter(xs, ys, zs, c = 'c', marker = 'x')
	scale = 2*np.sqrt(max(val for val, row in eigenpairs))

	ax.set_xlim3d(i - scale, i + scale)
	ax.set_ylim3d(j - scale, j + scale)
	ax.set_zlim3d(k - scale, k + scale)
	plt.show()

