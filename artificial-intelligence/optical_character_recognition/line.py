import matrix
import char


class line(matrix.matrix):

	__slots__ = ['chars']

	def __init__(self, list_mat):
		matrix.matrix.__init__(self, list_mat)
		self.chars = self.split_chars()


	def __iter__(self):
		return iter(self.chars)


	def __getitem__(self, key):
		return self.chars[key]

	def split_chars(self):

		def cut(flip):
			char_list = []
			char_mat  = []
			space = all(flip[0])
			for col in flip:
				empty = all(col)
				if space != empty:
					space = not space
					char_list.append(list(zip(*char_mat)))
					char_mat = []
				char_mat.append(col)
			if char_mat: char_list.append(list(zip(*char_mat)))
			return char_list

		def main(self):
			char_list = cut(self.flip)
			chars = [char.char(mat) for mat in char_list]
			return chars

		return main(self)




				








