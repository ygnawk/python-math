import numpy as np
import pca


def dot(tup1: tuple, tup2: tuple):
	return sum(i*j for i,j in zip(tup1, tup2))

def mmul(matrix1, matrix2):
	m = len(matrix1)
	n = len(matrix2[0])
	matrix2 = list(zip(*matrix2))
	return [[dot(matrix1[i], matrix2[j])
				for j in range(n)]
				for i in range(m)]


# set some transformation matrix
# to create a principal axis
data = [
	(1,0,50),
	(23,1.0,0),
	(0,12,1)
]

# randomize data
xs = np.random.normal(12, 3, 500)
ys = np.random.normal(3,  3, 500)
zs = np.random.normal(3,  1, 500)
base = list(zip(xs,ys,zs))
base = [(a,b,c) for a,b,c in base]

# transfrom data using the matirx
data = mmul(base, data)


# plot data
pca.plot3d(data)

# return the principal components
for value, vector in pca.principal_component(data):
	print(value, vector)