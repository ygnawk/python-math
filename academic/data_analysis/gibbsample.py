
import numpy.random as rand
import matplotlib.pyplot as plt
import scipy.stats as stats
import scipy.special
import numpy as np



import bayesian


def gibbs_sampler():
    """
        likelihood -> Func[real,...,real][real]
            returns the likelihood of the vector

        prior -> Func[real,...,real][real]
            returns the prior of the vector

        in_range -> Func[real,...,real][bool]
            checks if the vecor is in range or not

        std_jump -> real
            standard deviation of jump
    """

    def __init__(self, likelihood, prior, in_range, std_jump = 0.1):
        self.likelihood = likelihood
        self.std_jump = std_jump
        self.in_range = in_range
        self.samples = []
        self.prior = prior

    def run(self, iterations, point):
        n = point.size
        new_samples = []
        dim_data = point.size
        in_range = self.in_range
        std_jump = self.std_jump
        likelihood, prior = self.likelihood, self.prior
        density = prior(*point) * likelihood(*point)
        for i in range(iterations):
            if not i % 3000: print(i, flush = True)
            for i in range(n):
                new_samples.append(point)
                new = point + rand.normal(0, std_jump)
                if not in_range(*new): continue
                new_density = prior(*new) * likelihood(*new)
                if rand.random() < new_density/density:
                    density = new_density
                    point = new 

        self.samples.extend(new_samples)
        return new_samples

    def hist(self, granularity = 200):
        plt.hist(*zip(*self.samples), bins = 200)
        plt.show()

    def plot(self):
        plt.plot(*zip(*self.samples))
        plt.show()



class metropolis_sampler:
    """
        likelihood -> Func[real,...,real][real]
            returns the likelihood of the vector

        prior -> Func[real,...,real][real]
            returns the prior of the vector

        in_range -> Func[real,...,real][bool]
            checks if the vecor is in range or not

        std_jump -> real
            standard deviation of jump
    """

    def __init__(self, likelihood, prior, in_range, std_jump = 0.01):
        self.likelihood = likelihood
        self.prior = prior
        self.std_jump = std_jump
        self.in_range = in_range
        self.samples = []

    def run(self, iterations, point):
        new_samples = []
        dim_data = point.size
        mean = [0] * dim_data
        in_range = self.in_range
        std_jump = self.std_jump
        likelihood, prior = self.likelihood, self.prior
        density = prior(*point) * likelihood(*point)

        for i in range(iterations):
            if not i % 3000: print(i, flush = True)
            new_samples.append(point)
            new = point + rand.normal(mean, std_jump, size = dim_data)
            if not in_range(*new): continue
            new_density = prior(*new) * likelihood(*new)
            if rand.random() < new_density/density:
                density = new_density
                point = new 

        self.samples.extend(new_samples)
        return new_samples

    def hist(self):
        plt.hist(*zip(*self.samples), bins = 100)
        plt.show()

    def plot(self):
        plt.plot(*zip(*self.samples))
        plt.show()



import scipy.stats as stats
likelihood = lambda x: np.exp(-x**2/2)
prior = lambda x: 1

def in_range(theta): return True


a = metropolis_sampler(likelihood, prior, in_range, std_jump = 3)
a.run(50000, np.array([0.5]))
a.hist()
a.plot()

