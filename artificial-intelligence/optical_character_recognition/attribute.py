from PIL import Image as image
from PIL import ImageFilter
import PIL as pillow
import matrix
import math

blur = ImageFilter.GaussianBlur


def norm(l):
	return math.sqrt(sum(i**2 for i in l))


class attribute:

	__slots__ = [
		'_points',
		'char',
		'void',
		'size',
		'vect',
		'dens',
		'cent',
		'frac'
	]


	def __init__(self, character, nail_size, blur_fact):
		width, height = character.size
		self._points = tuple((i, j)
						for i in range(height)
						for j in range(width) 
						if not character.full[i][j])

		self.char = character
		self.void = character.void
		self.size = character.size
		self.dens = self.density()
		self.cent = self.centroid()
		self.vect = self.vector(nail_size, blur_fact)
		self.frac = character.width / character.height



	def vector(self, nail_size, blur_fact):
		"""
		returns its own thumbnail as a vector
		"""
		data = [i * 255 for i in self.char.flat]
		new = image.new('L', self.size)
		new.putdata(data)
		radius = nail_size/(blur_fact)
		new = new.resize([nail_size, nail_size], resample = image.LANCZOS)
		new = new.filter(blur(radius))
		return [i/255 for i in new.getdata()]
	

	def density(self):
		return len(self._points) / len(self.char.flat)


	def centroid(self):
		width, height = self.size
		x_center = sum(i for i, j in self._points) / width
		y_center = sum(j for i, j in self._points) / height
		return x_center, y_center

	
	def set_attr(self): 
		"""
		Ideas:
			points = [(i, j)
						for i in range(height)
						for j in range(width) 
						if not full[i][j]]


			density = len(points) / len(flat)
			x_coords = [i for i, j in points]
			y_coords = [j for i, j in points]
			centroid_mean 
			centroid_median
			centroid_mode
			x_hist
			y_hist
			bodies 
			size_ratio
		"""


