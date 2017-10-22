import matrix
import line


class document(matrix.matrix):

	__slots = ['lines']

	def __init__(self, docu_mat): # I deserve punishment for this
		matrix.matrix.__init__(self, docu_mat)
		self.lines  = self.split_lines()


	def __iter__(self):
		return iter(self.lines)

	def __getitem__(self, key):
		return self.lines[key]

	def split_lines(self):

		def cut(full):
			line_list = []
			line_mat = []
			for row in full:
				if not all(row):
					line_mat.append(row)
				elif line_mat:
					line_list.append(line_mat)
					line_mat = []
			if line_mat: line_list.append(line_mat)
			return line_list

		def main(self):
			line_list = cut(self.full)
			lines = [line.line(mat) for mat in line_list]
			return lines

		return main(self)










