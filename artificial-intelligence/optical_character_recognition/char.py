import attribute
import matrix


class char(matrix.matrix):
	__slots__ = ['_attr']

	def __init__(self, char_mat):
		matrix.matrix.__init__(self, char_mat)
