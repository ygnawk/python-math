from fractions import Fraction as f

def gradient(f, step = 10**-15):
	def derivative_at(x):
		return (f(x + step) - f(x)) / step
	return derivative_at

def find_root(f, x = 0.1, n = 12, threshold = 0.00000001):
	grad = gradient(f)
	new = x
	for i in range(n):
		print(new)
		old = new
		grad_old = grad(old)
		new = old - f(old)/ (grad_old if grad_old else threshold)
	return new

def find_extremum(f, x = 0.1, n = 12, threshold = 0.0000001):
	grad = gradient(f)
	return find_root(grad, x, n, threshold)




sample = lambda x : (x + 4) ** 2 + 3
driv = gradient(sample)



