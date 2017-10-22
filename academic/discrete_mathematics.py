"""
A Discrete Mathematics Module

By Kwang Yi Jie
"""

from fractions import Fraction as f
import random


def random_walk(dim):
    """
    random walk on dim-dimensional integer lattice
    starting at the origin
    """
    coordinate = [0 for i in range(dim)]
    while True:
        yield coordinate
        index = random.randrange(dim)
        change = random.choice([-1, 1])
        coordinate[index] += change


def from_cf(conf):
    """
    returns a fraction from 
    a continued fraction representation conf
    """
    summed = f(conf.pop())
    for conv in reversed(conf):
        summed = conv + (1 / summed)
    return summed


def to_cf(real):
    """
    converts real to its continued fraction representation
    """
    real = f(real)
    convergent = int(real)
    rep = []
    while real != convergent:
        real = 1 / (real - convergent)
        rep.append(convergent)
        convergent = int(real)
    return rep
