from PIL import Image as image
import random

def index_ends(flat, val):
	try: fore_index = flat.index(val)
	except ValueError: return -1, -1
	indices = reversed(range(len(flat)))
	for back_index in indices:
		if flat[back_index] == val:
			return fore_index, back_index


class matrix:

	__slots__ = [
		'width',  	# the width of the matrix
		'height', 	# the height of the matrix
		'list',		# the matrix as a one-d array
		'full',		# the matrix cropped
		'flip',		# the transpose of full
		'frac',		# how much that matrix was cropped
		'size',		# size = width, height
		'flat',		# full as a one-d array
		'void',		# whether or not the matrix is empty
	]

	@staticmethod
	def squeeze_thin(mat):
		flip 	= list(zip(*mat))	
		space 	= [all(col) for col in flip]
		l, r 	= index_ends(space, 0)
		dim 	= (l, r, len(flip))
		return dim, list(zip(*flip[l: r + 1]))

	@staticmethod
	def squeeze_flat(mat):
		space 	= [all(row) for row in mat]
		hi, lo 	= index_ends(space, 0)
		dim 	= (hi, lo, len(space))
		return dim, mat[hi: lo + 1]


	def __init__(self, mat):
		frac_v, full = matrix.squeeze_flat(mat)
		frac_h, full = matrix.squeeze_thin(full)
		if not full: full = mat

		self.void	= all(all(row) for row in mat)
		self.list 	= mat
		self.full 	= full
		self.width  = len(full[0])
		self.height = len(full)
		self.flip 	= list(zip(*full))
		self.frac	= frac_h, frac_v
		self.size	= self.width, self.height
		self.flat 	= [val 
						for row in full
						for val in row]



	def show(self, space = False, new = None):
		if not self.void or space:
			new = image.new('L', self.size)
			new.putdata([i * 255 for i in self.flat])
			new.show()
			#name = random.randint(0, 10**13)
			#new.save("sample_image/" + str(name) + ".jpg")












