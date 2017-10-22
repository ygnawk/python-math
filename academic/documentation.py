"""
NUMBER THEORY
"""

import number_theory as nt

# find an integer root of n assuming that n is a perfect square
root = nt.root(64)
print(root)

# returns -1 if n is not
root = nt.root(63)
print(root)


# finds the gcd of a and b
a = 12
b = 18
gcd = nt.gcd(a,b)
print(gcd)
print()
# finds all integers relatively prime to n
# returns as an iterator
iterator = nt.totient_set(30)
for i in iterator:
	print(i)
print()


# finds the number of numbers less than n
# and relatively prime to n using factorization

totient = nt.totient(30)
print(totient)


# find the order of a mod n
order = nt.order(12, 13)
print(order)

# returns -1 if ordeeer doesnt exist
order = nt.order(12, 14)
print(order)

# find all primitive roots mod p
print()
iterator = nt.primitive_root(7)
for i in iterator:
	print(i)
print()


# finds the d, x, y such that ax + by = d where d == gcd(a, b)
d, x, y = nt.extended_euclid(13, 7)
print("a%s + b%s = %s" %(x, y, d))


# finds the inverse of a mod n assuming gcd(a, n) == 1
inv = nt.inv_mod(14, 19)
print(inv)

# sieve of erathostheses
primes = nt.sieve(10**5)
print(primes[-12:])

# check primality using trial division
a = 13
print(nt.prime(a))


# factorize an integer
a = 123124
print(nt.factor(a))
# a = a**2 * 30781**1


# shor factorization algorithm
# returns two potential factors
a = 150
print(nt.shor_factor(a))


# check if a is a residue mod p
residue = nt.residue(6, 13)
print(residue)


# solve ax = b mod n
a = 13
b = 12
n = 29
print(nt.linear_congruence(a,b,n))


# reduces a mod p to its chinese remainder representation
l = nt.chinese_remainder(13, 120)
print(l)


# simultaneously solves x = b1 mod n1 and x = b2 mod n2
b1 = 13
b2 = 21
n1 = 29
n2 = 41
print(nt.simultaneous_equation(b1, b2, n1, n2))


# finds the lcm of two or more numbers
print(nt.lcm(1,2,23,12))


# miller rabin primality test with base b
b = 12
p = 297
print(nt.miller_rabin(12, 297))
print(nt.factor(297))


# fast primality testing using miller rabin algorithm
# 50 digit prime
n = 758365936693560365693659025601840367164603656936591
print(nt.fast_prime(n))


"""
CIPHERS
"""
import ciphers as c


# converts a string to integer
message = c.string_to_int("I am the greatest.")

# goldwasser micali ciphers
# takes primes p and q and a non-residue mod p and q
encrypt, decrypt = c.goldwasser_micali(13, 17, 5)

# encrypt
code = encrypt(message)
print(code)
#decrypt
decrypted = decrypt(code)

# converts an integer back to string
print(c.int_to_string(decrypted))


# RSA encryption, takes two primes and and some number 
# relatively prime to both
encrypt, decrypt = c.rsa(99999989, 99999971, 15485867)

message = c.string_to_int("text")
# encrypt
code = encrypt(message)

print(code)
# decrypt
decrypted = decrypt(code)

# converts an integer back to string
print(c.int_to_string(decrypted))


# one time pad, takes any random number
encrypt = c.one_time_pad(1231241824124102912312312)
message = c.string_to_int("one time pad is effective, somewhat")
code = encrypt(message)
print(code)

# one time pad is symmetric key. Encryption and decryption algorithms 
# are the same
decrypted = encrypt(code)
print(c.int_to_string(decrypted))


"""
DISCRETE MATHEMATICS
# in progress
"""

import math
import discrete_mathematics as dm

# get the continued fraction representation of a float
conf = [i for i in dm.to_cf(math.pi)]
print(conf)


# get the float from the continued fraction representation
print(float(dm.from_cf(conf)))


# random walk on dim-dimensional integer lattice
# starting at the origin
walk = dm.random_walk(2)
for i in range(10):
	print(next(walk))
