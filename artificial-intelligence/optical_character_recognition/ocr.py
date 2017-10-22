from PIL import Image as image
import math


import matrix
import document
import classifier

def dot(u, v):
	return sum(i * j for i, j in zip(u,v))


# @decorator.memoize
def phi(a, b = None, sqrt_2 = math.sqrt(2.0)):
	if b == None:
		erf = math.erf(a / sqrt_2)
		return (1 + erf) / 2.0
	else:
		erf_a = math.erf(a / sqrt_2)
		erf_b = math.erf(b / sqrt_2)
		return (erf_b - erf_a) / 2


# @decorator.memoize
def gaussian_kernel(std, length):
	even = length + 1
	half =  std/2
	pair = [i*std + half for i in range(even // 2)]
	pair = [-i for i in reversed(pair)] + pair

	gaussian = [phi(a, b) 
					for a, b 
					in zip(pair, pair[1:])]

	sum_blur = sum(gaussian)
	return [i/sum_blur for i in gaussian]


class ocr:

	__slots__ = [
		'size',
		'pict',
		'data',
		'document',
		'classifier',
		'parameters'

	]

	def __init__(self, pict, nail_size = 10, blur_fact = 120, tolerance = None):
		
		
		pict = pict.convert('L')
		self.size 	= pict.size
		self.pict 	= pict
		self.data 	= list(pict.getdata())		
		
		width  	= pict.width
		length 	= len(self.data)
		back 	= self.convert()
		docu_mat = [back[i: i + width] 
					for i in range(0, length, width)]

		self.document = document.document(docu_mat)

		self.parameters = (nail_size, blur_fact, tolerance)
		self.classifier = self.get_classifier()
		




	def convert_adaptive(self):
		print(self.pict.getextrema.__doc__)


	def convert(self):

		def histogram(self):
			# hist = [self.data.count(i) for i in range(256)]
			return self.pict.histogram()

		def blur_gaussian(hist):
			gaussian = gaussian_kernel(1, 7)
			zero_val = [hist[ 0 ] for i in range(3)]
			coda_val = [hist[255] for i in range(3)]
			extended = zero_val
			extended.extend(hist)
			extended.extend(coda_val)
			blurred = [dot(extended[i:i + 6], gaussian)
									for i in range(256)]
			return blurred


		def find_back(hist):
			hist_key	= lambda i: hist[i]
			mode_key 	= lambda i:((i == 0   or hist[i] > hist[i - 1])
								and (i == 255 or hist[i] > hist[i + 1]))

			modes 		= [i for i in range(256) if mode_key(i)]
			back_value 	= max(modes, key = hist_key)
			modes 		= [-modes[0]] + modes + [-modes[-1] + 510] 
			back_index 	= modes.index(back_value)

			hi_bound	= (back_value + modes[back_index + 1]) / 2
			lo_bound	= (back_value + modes[back_index - 1]) / 2
			return lo_bound, hi_bound


		def main(self):
			hist = histogram(self)
			hist = blur_gaussian(hist)
			lo_bound, hi_bound = find_back(hist)
			background = [lo_bound <= val <= hi_bound
								for val in self.data]
			return background

		return main(self)


	def get_classifier(self):
		char_list = [char 
						for line in self.document 
						for char in line]
		return classifier.classifier(char_list, *self.parameters)



	def get_attr_list(self):
		return [[ self.classifier.classify(char) 
						for char in line]
						for line in self.document]


	def spit_text(self):
		text = []
		for line in self.document:
			for char in line:
				symb = self.classifier.classify(char)
				if symb:
					text.append(symb)
			text.append("\n")
		return "".join(text)






