import numpy as np


def newton(val, func, prime, n = 2, seed = None):
    """
    newton's method for root finding
    search for x such that func(x) = val
    """
    moved = lambda x: func(x) - val
    seed = seed if seed else val
    seed -= np.clip(moved(seed)/prime(seed), -0.3, 0.3)
    seed -= np.clip(moved(seed)/prime(seed), -0.3, 0.3)
    for i in range(n):
        seed -= np.clip(moved(seed)/prime(seed), -0.1, 0.1)
        seed -= np.clip(moved(seed)/prime(seed), -0.1, 0.1)
        seed -= np.clip(moved(seed)/prime(seed), -0.1, 0.1)
        seed -= np.clip(moved(seed)/prime(seed), -0.1, 0.1)
    return seed

def secant(val, func, n = 2, seed = None):
    """
    secant method for root finding
    search for x such that func(x) = val
    more stable but slower and does not require
    derivative
    """
    moved = lambda x: func(x) - val
    if not isinstance(seed, (tuple, list)):
        seed = seed - 0.1, seed + 0.1
    past, curr = seed if seed else (0, 1)
    for i in range(n):
        past, curr = curr, curr - moved(curr) * (curr - past) / (moved(curr) - moved(past))
        past, curr = curr, curr - moved(curr) * (curr - past) / (moved(curr) - moved(past))
        past, curr = curr, curr - moved(curr) * (curr - past) / (moved(curr) - moved(past))
        past, curr = curr, curr - moved(curr) * (curr - past) / (moved(curr) - moved(past))
    curr = curr, moved(curr) * (curr - past) / (moved(curr) - moved(past))
    return curr


