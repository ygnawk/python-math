"""
Number Theoretic Functions

By Kwang Yi Jie
"""
#import random

import math

def root(n: int):
    """
    return the root of the perfect square n 
    or return 0 if n is not a perfect square
    using newton's method
    """
    x = n//2
    seen = set([x])
    while x * x != n:
        x = (x + (n // x)) // 2
        if x in seen:
            return -1
        seen.add(x)
    return x


def gcd(a: int, b: int):
    "returns the gcd of a and b"
    while a % b != 0:
        a, b = b, a % b
    return b


def totient_set(n: int):
    "returns all integers less than n relatively prime to n"
    return (i for i in range(1, n) if gcd(i, n) == 1)


def totient(n: int):
    "returns the number of integers less than n that is relatively prime to n"
    if n == 1:
        return 1
    factors = factor(n)
    for a, _ in factors:
        n = n // a * (a - 1)
    return n


def order(a: int, n: int):
    "find the order of a modulo n, returns -1 "
    "is a is not relatively prime to n"
    if gcd(a, n) != 1:
        return -1
    for i in range(1, n):
        if (a**i) % n == 1:
            return i
    return 1


def primitive_root(p: int):
    "yields all primitive roots mod p -- sorted"
    return (a for a in range(1, p) if order(a, p) == p - 1)


def extended_euclid(a: int, b: int):
    "returns triplets of integers gcd(a, b), x, y "
    "such that ax + by = gcd(a, b)"
    (x1, y1), (x2, y2) = (1, 0), (0, 1)
    r = 1
    while r != 0:
        q, r = a // b, a % b
        (x1, y1), (x2, y2) = (x2, y2), (x1 - q * x2, y1 - q * y2)
        a, b = b, r
    return a, x1, y1


def inv_mod(a: int, n: int):
    "returns the inverse of a mod n."
    inv = extended_euclid(a, n)[1]
    return inv


def sieve_set(n: int):
    "returns all primes less than n"
    p_sieve = {i for i in range(3, n + 1, 2)}
    ceil = round(n**0.5) + 1
    for i in range(1, ceil, 2):
        if i in p_sieve:
            p_sieve -= {n for n in range(i * i, n + 1, i)}
    return p_sieve | {2}


def oddsieve(n):
    primes = [True] * n
    ceil = int(n**0.5) + 1
    for p in range(3,ceil,2):
        if primes[p]:
            primes[p*p:n:2*p] = [False] * len(range(p*p,n,2*p))
    return [i for i in range(3,n,2) if primes[i]]


def setsieve(n):
    primes = []
    multiples = set()
    ceil = int(n**0.5) + 1
    for i in range(3,ceil,2):
        if i not in multiples:
            multiples.update(range(i*i, n, 2*i))
    return [i for i in range(3,n,2) if i not in multiples]



def sieve(n: int):
    """
    The most efficient sieve 
    you've ever seen in your life
    """
    primes = [True] * n
    ceil = int(n**0.5) + 1
    for p in range(3,ceil,2):
        if primes[p]:
            primes[p*p:n:2*p] = [False] * len(range(p*p,n,2*p))
    result = [2]
    for i in range(3,n,2):
        if primes[i]:
            result.append(i)
    return result


def iterator_sieve(n: int):
    "returns an iterator of all primes less than n"
    n += 1
    p_sieve = [True] * n
    ceil = int(n**0.5) + 1
    for i in range(2, ceil):
        if p_sieve[i]:
            yield i
            for j in range(i * i, n, i):
                p_sieve[j] = False
    for i in range(ceil, n):
        if p_sieve[i]:
            yield i


def prime(n: int):
    "checks if n is a prime"
    ceil = round(n**0.5) + 1
    for i in range(2, ceil):
        if n % i == 0:
            return False
    return True


def factor(n: int):
    "returns factors of n as a list of tuples containing each factor and their multiplicity"
    k = n
    factors = []
    count = 0
    for i in range(2, n):
        if n % i == 0:
            while n % i == 0:
                n //= i
                count += 1
            factors.append((i, count))
            count = 0
        if n == 1:
            return factors
        elif i * i > n:
            factors.append((n, 1))
            return factors
    return [(k, 1)]


def shor_factor(n: int):
    "shor's factorization algorithm. Useless in a classical computer."
    if n == 1:
        return (1, 1)
    if n == 2:
        return (1, 2)
    for i in range(2, n):
        if gcd(i, n) != 1:
            continue
        d = order(i, n)
        if d % 2 == 0:
            a = i
            x = a**(d // 2)
            return gcd(x + 1, n), gcd(x - 1, n)


def prod(l: list):
    "returns a product over an iterable"
    a = 1
    for i in l:
        a *= i
    return a


def factorial(n: int):
    "returns n factorial"
    return prod(i for i in range(n))


def residue(a: int, p: int):
    "checks if a is a quadratic residue mod p"
    return pow(a, (p - 1) // 2, p) == 1


def quadratic_residues(p: int):
    "returns all quadratic residues mod p"
    return sorted(i*i % p for i in range(1, (p + 1 // 2)))


def intersect(l1, l2):
    "returns an iterator representing the intersection of two iterables."
    set_l = set(l2)
    return (i for i in l1 if i in set_l)


def linear_congruence(a: int, b: int, n: int):
    "solve ax = b mod n"
    d = gcd(a, b)
    return (inv_mod(a, n) * b // d) % n


def chinese_remainder(a: int, n: int):
    "reduces a congruence to its chinese remainder "
    "representation as a list of tuples."
    return [(a % p, p) for p, multplicity in factor(n)]


def simultaneous_equation(b1: int, b2: int, n1: int, n2: int):
    "solves x = b1 mod n1 and x = b2 mod n2"
    if gcd(n1, n2) != 1:
        raise ValueError(
            "no solution for x = %s (%s) and x = %s (%s)" 
            % (b1, n1, b2, n2))
    _, x, y = extended_euclid(n1, n2)
    return (y * n2  * b1 + x * n1 * b2) % (n1 * n2)


def lcm(*l):
    "finds the least common multiple of integers in l"
    init = 1
    for n in l:
        init *= n // gcd(init, n)
    return init


def miller_rabin(base, p):
    "does a miller-rabin prime verification"
    phi = val = p - 1
    two = 0
    while val % 2 == 0:
        val //= 2
        two += 1
    powered = pow(base, val, p)
    if powered == 1:
        return True
    for i in range(two):
        powered = pow(powered, 2, p)
        if powered == 1:
            return True
    return False


def fast_prime(p):
    "fast prime check for large primes"
    if p == 1:
        return False
    if p in [2, 3, 5, 7]:
        return True
    k = gcd(p, 210) # 210 = 2*3*5*7
    if k > 1:
        return False
    logp = int(math.log(p))**2
    smallprimes = sieve(logp)
    for base in smallprimes:
        if not miller_rabin(base, p):
            return False

    return True

