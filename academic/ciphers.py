import random
import math


def extended_euclid(a, b):
	"""
	returns triplets of integers
	gcd(a,b), x, y such that ax + by = gcd(a,b)
	"""
	(x1, y1), (x2, y2) = (1, 0), (0, 1)
	r = 1
	while r != 0:
		q, r = a // b, a % b
		(x1, y1), (x2, y2) = (x2, y2), (x1 - q * x2, y1 - q * y2)
		a, b = b, r
	return a, x1, y1


def string_to_int(string):
	"""
	converts a string to an integer 
	using byte concatenation
	"""
	ord_list = [ord(letter) for letter in string]
	ret_val = 0
	for letter in string:
		ret_val <<= 8
		order = ord(letter)
		ret_val |= order
	return ret_val


def int_to_string(n: int):
	"""
	converts an integer to string
	"""
	text = []
	while n:
		letter = chr(n & 255)
		text.append(letter)
		n >>= 8
	return str.join('', reversed(text))


def shuffle(word):
	"""
	switch around the letters in the middle a word
	"""
	word = list(word)
	shuffled = word[1:-1]
	random.shuffle(shuffled)
	word[1:-1] = shuffled
	return "".join(word)


def scramble(string):
	"""
	shuffle each word in the string
	"""
	words = string.split(" ")
	scrambled = (shuffle(i) for i in words)
	return " ".join(scrambled)



def goldwasser_micali(p, q, non_res):
	"""
	returns a GM encryptor and decryptor using
	primes p, q and a non-residue mod p and q
	"""

	def iter_coprime(a, condition=lambda x: True):
		"choose a random integer coprime to a less than a"
		while True:
			n = random.randrange(1, a)
			if math.gcd(n, a) == 1 and condition(n):
				yield n


	def bit_stream(n: int):
		while n:
			yield n&1
			n //= 2

	def from_binary(l: list):
		summed = 0
		for bit in reversed(l):
			summed <<= 1
			if bit:
				summed |= bit
		return summed

	def main(p, q, non_res):
		a = (p - 1) // 2
		b = (q - 1) // 2
		n = p * q

		lower = int(math.sqrt(n))
		upper = n - lower

		condition = lambda x: lower <= x <= upper
		residue = lambda m: (pow(m, a, p) == 1 
						 and pow(m, b, q) == 1)

		def encrypt(message: int):
			stream = bit_stream(message)
			primes = iter_coprime(n, condition)
			return [(coprime * coprime) % n if bit
					else (coprime * coprime * non_res) % n
					for bit, coprime in zip(stream, primes)]

		def decrypt(message: int):
			decoded = [residue(x) for x in message]
			return from_binary(decoded)

		assert pow(non_res, a, p) == p - 1 
		assert pow(non_res, b, q) == q - 1
		return encrypt, decrypt

	
	return main(p, q, non_res)



def rsa(p, q, e):
	"""
	p and q are large primes
	e is a positive integer relatively prime to p and q

	returns an encrypter and a decryptor that
	takes in a number and returns another number.
	"""
	prod_num = p * q
	prod_pow = prod_num - p - q + 1
	test, _, d = extended_euclid(prod_pow, e)
	d %= prod_pow
	encrypt = lambda i: pow(i, e, prod_num)
	decrypt = lambda i: pow(i, d, prod_num)

	# sanity check
	assert math.gcd(e, prod_num) == 1

	return encrypt, decrypt


def one_time_pad(key: int):
	"""
	returns a one time pad encryptor (decryptor) given a key
	"""
	def bit_count(message):
		length = 0
		while message:
			length += 1
			message >>= 1
		return length

	def enlongate(key, bits):
		copy = key
		length = bit_count(key)
		while key < bits:
			key = (key << length) + copy
		return key

	def encrypt(message):
		bits = bit_count(message)
		copy = enlongate(key, bits)
		return message ^ copy

	return encrypt, encrypt


