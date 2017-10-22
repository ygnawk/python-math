
import numpy.random as rand
import numpy as np

def anneal(func, x, sigma, iterations, rate = 0.999):
    val = func(*x)
    dim = len(x)
    best, best_val = pin, pin_val
    for i in range(iterations):
        sigma *= rate
        
        new = rand.normal(x, sigma, dim)
        new_val = func(new)

        if new_val < val and new_val < val * rand.unif(): 
            x, val = new, new_val
            if new_val > best_val:
                best, best_val = x, val





