import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.special
import numpy as np

def posterior(priors, likelihoods):
    unnormalized = priors * likelihoods
    return unnormalized / unnormalized.sum()

def plot(distribution, label = None):
    x_axis = range(len(distribution))
    plt.bar(x_axis, distribution, align = 'center', alpha = 0.7)
    if label: plt.xticks(x_axis, label)
    plt.show()

def normalize(vec):
    return vec / vec.sum()


def newton(val, func, prime, n = 2, seed = None):
    """
    newton's method for root finding
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
    newton's method for root finding
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


class continuous_distribution:

    def __init__(self, domain):
        self.domain = domain

    def plot(self, length = 1000, domain = None):
        length = 1000
        if not domain: domain = self.domain
        domain = np.linspace(*domain, length)
        plt.plot(domain, self(domain))
        plt.show()

    def confidence_interval(self, alpha, n = 2):
        back_alpha = 0.5 - alpha / 2
        fore_alpha = 0.5 + alpha / 2
        prime = self.__call__
        func = self.cumulative
        seed = self.mode if self.mode else self.mean
        back = search(back_alpha, func, prime, n = n, seed = seed)
        fore = search(fore_alpha, func, prime, n = n, seed = seed)
        return back, fore

    @property
    def mode(self):
        return None

    @property
    def mean(self):
        return None

    @property
    def variance(self):
        return None

    @property
    def mode(self):
        return None

class beta(continuous_distribution):
    
    def __init__(self, alpha = 2, beta = 2):   
        continuous_distribution.__init__(self, (0,1))
        self.alpha = alpha
        self.beta = beta
    
    def update(self, n_heads, n_tails):
        self.alpha += n_heads
        self.beta  += n_tails

    def __call__(self, theta):
        return stats.beta.pdf(theta, self.alpha, self.beta)

    def cumulative(self, theta):
        return stats.beta.cdf(theta, self.alpha, self.beta)

    @property
    def mean(self):
        return self.alpha / (self.alpha + self.beta)

    @property
    def mode(self):
        return (self.alpha - 1) / (self.alpha + self.beta - 2)

    @property
    def variance(self):
        a = self.alpha
        b = self.beta
        return a*b / ((a + b)**2 * (a + b + 1))



def normal(x, space):
    return np.exp(-((x - space)**2/(2 * 14.2396**2)))

def grid_method(likelihood, prior, data, space):
    for point in data:
        likel = likelihood(point, space)
        prior = prior * likel
        prior /= prior.sum()
    return prior


space = np.linspace(0, 0.5, 1000)

prior = np.array([1 for i in range(1000)])
#prior = np.array([1 for i in range(1000)])

likelihood = lambda head, pred : pred if head else 1 - pred

data = [1] * 14 + [0] * 86

test = grid_method(likelihood, prior, data, space)


print(test[-500:].sum() / test.sum())
print(len(test), flush = True)

plt.plot(space, test)
plt.show()








