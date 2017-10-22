import pylab
import matplotlib.pyplot as plt


def dot(v, w):
	return sum(i*j for i,j in zip(v,w))

def vec_sum(iterable_vec):
	sum_v = [0 for i in iterable_vec[0]]
	for i in iterable_vec:
		for index,j in enumerate(i):
			sum_v[index] += j
	return sum_v

def high_dot(v,w,n = 2):
	return (dot(v, w) + 1)**n


class support_vector_machine:

	__slots__ = ('trained', 'c', 'data', 'target', 'kernel', 'tolerance', 'trained',
				'b', 'w', 'dim', 'alphas', 'error', 'support_vectors')

	def __init__(self, data, target, kernel = dot, c = 1, tolerance = 0.000000001):
		# kernel takes two vectors and returns their dot product
		# in some n-dimensional plane
		self.c = c
		self.data = data
		self.target = target
		self.kernel = kernel
		self.tolerance = tolerance * c
		self.trained = False


		self.b = 0
		self.dim = len(data[0])
		self.alphas = [0 for i in data]
		self.error = [-y for y in target]


	def solve_lagrange(self, index_1, index_2):
		a_1_old = self.alphas[index_1]
		a_2_old = self.alphas[index_2]
		y_1 = self.target[index_1]
		y_2 = self.target[index_2]
		x_1 = self.data[index_1]
		x_2 = self.data[index_2]
		kernel = self.kernel
		C = self.c

		if y_1 == y_2:
			lower_bound_a_2 = max(0, a_2_old + a_1_old - C)
			upper_bound_a_2 = min(C, a_2_old + a_1_old)
		else: # y_1 != y_2
			lower_bound_a_2 = max(0, a_2_old - a_1_old)
			upper_bound_a_2 = min(C, a_2_old - a_1_old + C)

		eta = 2*kernel(x_1, x_2) - kernel(x_1, x_1) - kernel(x_2, x_2)

		if abs(eta) < self.tolerance:
			a_2_new = upper_bound_a_2
			a_2_new_clipped = a_2_new

		else:
			error_1 = self.error[index_1]
			error_2 = self.error[index_2]
			a_2_new = a_2_old - (y_2*(error_1 - error_2))/eta

			# clip a_2 to be with in the inequality constraints
			if a_2_new >= upper_bound_a_2:
				a_2_new_clipped = upper_bound_a_2
			elif a_2_new <= lower_bound_a_2:
				a_2_new_clipped = lower_bound_a_2
			else:
				a_2_new_clipped = a_2_new


		a_1_new = a_1_old + y_1*y_2*(a_2_old - a_2_new_clipped)

		delta_a_1 = a_1_new - a_1_old
		delta_a_2 = a_2_new_clipped - a_2_old
		if abs(delta_a_1) > self.tolerance:
			self.alphas[index_1] = a_1_new
		else:
			delta_a_1 = 0

		if abs(delta_a_2) > self.tolerance:
			self.alphas[index_2] = a_2_new_clipped
		else:
			delta_a_2 = 0

		#"""


		return delta_a_1, delta_a_2



	def update_error(self, index_1, index_2, delta_a_1, delta_a_2):
		x_1 = self.data[index_1]
		x_2 = self.data[index_2]
		y_1 = self.target[index_1]
		y_2 = self.target[index_2]
		a_1 = self.alphas[index_1]
		a_2 = self.alphas[index_2]
		C = self.c

		if 0 < a_1 < C:
			x_change = x_1
			index_change = index_1
			delta_b = (self.error[index_change]
					+ delta_a_1 * y_1 * self.kernel(x_1, x_change)
					+ delta_a_2 * y_2 * self.kernel(x_2, x_change))
		elif 0 < a_2 < C:
			x_change = x_2
			index_change = index_2
			delta_b = (self.error[index_change]
					+ delta_a_1 * y_1 * self.kernel(x_1, x_change)
					+ delta_a_2 * y_2 * self.kernel(x_2, x_change))
		else:
			val_1 = (self.error[index_1]
					+ delta_a_1 * y_1 * self.kernel(x_1, x_1)
					+ delta_a_2 * y_2 * self.kernel(x_2, x_1))
			val_2 = (self.error[index_2]
					+ delta_a_1 * y_1 * self.kernel(x_1, x_2)
					+ delta_a_2 * y_2 * self.kernel(x_2, x_2))
			delta_b = (val_1 + val_2)/2

		self.b += delta_b

		for index, (x_i, y_i) in enumerate(zip(self.data, self.target)):
			self.error[index] += (
					+ delta_a_1 * y_1 * self.kernel(x_1, x_i)
					+ delta_a_2 * y_2 * self.kernel(x_2, x_i)
					- delta_b)

	def smooth_alphas(self):
		for index, i in enumerate(self.alphas):
			if abs(i) < self.tolerance:
				self.alphas[index] = 0
			elif abs(i - self.c) < self.tolerance:
				self.alphas[index] = self.c

	def train(self):
		def pairs(num):
			for i in range(num):
				for j in range(i):
					yield (i+j)%num, j

		# do the first iteration
		changed_set = set(i for i in range(len(self.alphas)))
		changed_list = sorted(changed_set)
		past_alphas = self.alphas[:]
		self.smooth_alphas()

		for i_1, i_2 in pairs(len(changed_set)):
			index_1, index_2 = changed_list[i_1], changed_list[i_2]
			delta_a_1, delta_a_2 = self.solve_lagrange(index_1, index_2)
			if delta_a_1 or delta_a_2:
				self.update_error(index_1, index_2, delta_a_1, delta_a_2)

		for i in reversed(range(len(changed_set))):
			index = changed_list[i]
			if past_alphas[index] == self.alphas[index]:
				changed_set.remove(index)

		# begin loop
		while changed_set:
			while changed_set:
				changed_list = sorted(changed_set)
				past_alphas = self.alphas[:]
				self.smooth_alphas()
				for i_1, i_2 in pairs(len(changed_set)):
					index_1, index_2 = changed_list[i_1], changed_list[i_2]
					delta_a_1, delta_a_2 = self.solve_lagrange(index_1, index_2)
					if delta_a_1 or delta_a_2:
						self.update_error(index_1, index_2, delta_a_1, delta_a_2)

				for i in reversed(range(len(changed_set))):
					index = changed_list[i]
					if past_alphas[index] == self.alphas[index]:
						changed_set.remove(index)

			# do the first iteration again
			self.smooth_alphas()
			past_alphas = self.alphas[:]
			changed_set = set(i for i in range(len(self.alphas)))
			changed_list = sorted(changed_set)
			for i_1, i_2 in pairs(len(changed_set)):
				index_1, index_2 = changed_list[i_1], changed_list[i_2]
				delta_a_1, delta_a_2 = self.solve_lagrange(index_1, index_2)
				if delta_a_1 or delta_a_2:
					self.update_error(index_1, index_2, delta_a_1, delta_a_2)

			for i in reversed(range(len(changed_set))):
				index = changed_list[i]
				if past_alphas[index] == self.alphas[index]:
					changed_set.remove(index)


		# calculate w
		scale = lambda a, v: [a*i for i in v]
		scaled = [scale(a_i*y_i, x_i)
					for a_i, y_i, x_i
					in zip(self.alphas, self.target, self.data)
					if a_i > 0]
		w = vec_sum(scaled)
		self.w = w

		# calculate b
		projected_data = [(dot(i, w), j)
							for i,j in zip(self.data, self.target)]
		high = min([i for i,j in projected_data if j == 1])
		low = max([i for i,j in projected_data if j == -1])
		self.b = -(high + low)/2
		self.trained = True

		# set support vectors
		self.support_vectors = [(x,y,a)
								for (x,y,a)
								in zip(self.data, self.target, self.alphas)
								if a > 0]

	def classify(self, z):
		return sum(a_i * y_i * self.kernel(x_i, z)
					for (x_i, y_i, a_i)
					in self.support_vectors) - self.b

	def check_trained(self):
		if not self.trained:
			raise ValueError('support vector machine not trained')

	def plot(self):
		self.check_trained()
		if self.dim != 2 or self.kernel != dot:
			raise ValueError('can only plot two dimensional points')



		(a, b), c = self.w, self.b
		m = -a/b
		i = -c/b

		right = [x for x,y in zip(self.data, self.target) if y == 1]
		wrong = [x for x,y in zip(self.data, self.target) if y == -1]

		xs, ys = zip(*right)
		plt.scatter(xs, ys, color = 'blue')
		xs, ys = zip(*wrong)
		plt.scatter(xs, ys, color = 'red')

		maximum = max(a for a,b in self.data)
		minimum = min(a for a,b in self.data)



		plt.plot([m*x + i for x in range(minimum, maximum)])
		plt.show()
