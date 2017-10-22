import functools
import random

import attribute
import math


queue_char = list("1234567890-=!@#$%^&*()_+`~qwertyuiop[]\QWERTYUIOP{}|asdfghjkl;'ASDFGHJKL:\"ZXCVBNM<>?zxcvbnm,./" * 300)
# random.shuffle(queue_char)
#[i for i in reversed(range(100000))]
#queue_char = list("?thisnobadrgh000")



def dot(u, v):
	return sum(i * j for i, j in zip(u, v))


def mean_std(l):
	if not l:
		return 0, 0
	mean = sum(l)/len(l)
	var = sum((i - mean)**2 for i in l)
	var /= len(l) - 1
	return mean, math.sqrt(var)


class char_class(attribute.attribute):

	def __init__(self, attr):
		self.char = attr.char
		self.void = attr.void
		self.size = attr.size
		self.dens = attr.dens
		self.cent = attr.cent[:]
		self.vect = attr.vect[:]
		self.frac = attr.frac


		self.attr_list = [attr]
		self.char_list = [attr.char]
		self.count = 1
		self.code = queue_char.pop()



	def recalculate(self):
		vectors = [attr.vect for attr in self.attr_list]
		self.vect = sum(row for row in zip(*vectors)) / len(vectors)


	def add(self, attr):

		self.char_list.append(attr)
		self.attr_list.append(attr.char)
		new_count = self.count / (self.count + 1)
		self.count += 1

		self.vect = [(old + new/self.count)*new_count
						for old, new in 
						zip(self.vect, attr.vect)]


	def disparity(self, attr):
		diff = (self.frac - attr.frac) / self.frac
		if abs(diff) > 0.25:
			return 200
		return (sum((i - j)**2
					for i, j 
					in zip(self.vect, attr.vect)))


class classifier:

	@staticmethod
	def min_dist(symb_list, attr):
		curr_index = ''
		curr_dist = 100000.0
		for index, class_attr in enumerate(symb_list):
			dist = class_attr.disparity(attr)
			if dist < curr_dist:
				curr_dist = dist
				curr_index = index
		return curr_index, curr_dist

	def get_attr(nail_size, blur_fact):

		def _get_attr(character):
			return attribute.attribute(
					character = character, 
					nail_size = nail_size, 
					blur_fact = blur_fact)
		return _get_attr


	def __init__(self, char_list, nail_size, blur_fact, tolerance):
		self.symb_list = []
		self.char_list = char_list
		
		self.blur_fact = blur_fact
		self.nail_size = nail_size
		self.attribute = classifier.get_attr(nail_size, blur_fact)

		self.attr_list = [self.attribute(character) 
							for character in char_list]
		self.tolerance = (self.get_tolerance() 
							if tolerance == None
							else tolerance)
		self.symb_list = self.train()
		self.space_len = self.space_ratio()

	def train(self):
		queue = self.attr_list[:]
		last = queue.pop()
		symb_list = [char_class(last)]

		for attr in queue:
			if attr.void:
				continue
			index, dist = classifier.min_dist(symb_list, attr)
			print(len(symb_list), dist)
			if dist > self.tolerance:
				new_symb = char_class(attr)
				symb_list.append(new_symb)
			else:
				symb_list[index].add(attr)
		return symb_list

	def get_tolerance(self):
		queue = self.attr_list[:1000]
		last = queue.pop()
		symb_list = [char_class(last)]
		dist_list = []
		for attr in queue:
			if attr.void:
				continue
			index, dist = classifier.min_dist(symb_list, attr)
			new_symb = char_class(attr)
			symb_list.append(new_symb)
			dist_list.append(dist)
		mean, stdev = mean_std(dist_list) 

		return mean + 0.17 * stdev

	def space_ratio(self):
		space_span = [char.width / char.height 
							for char in self.char_list 
							if char.void]
		mean, std = mean_std(space_span)
		return mean + 0.5 * std

	def classify(self, char):
		if char.void:
			is_space = char.width / char.height > self.space_len
			return " " * is_space

		index, dist = classifier.min_dist(self.symb_list, self.attribute(char))
		return self.symb_list[index].code



