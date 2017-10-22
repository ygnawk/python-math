import numpy.core.umath_tests as umath
import numpy.random as rand
import numpy as np

from sklearn import datasets


def euclidean(x, y):
    diff = x - y
    return np.dot(diff, diff)

def stochastic_cluster(data_points, n_clusters = 2, n = 100, l_rate = 0.01, dist = euclidean):

    def initialize(data_points, n_clusters):
        data = [np.array(i) for i in data_points]
        rand.shuffle(data)
        means = data[:n_clusters]
        return data, means

    def update(point, means, l_rate):
        dist_point = lambda x: dist(point, x)
        minimum = min(means, key = dist_point)
        minimum *= (1 - l_rate)
        minimum += l_rate * point


    def main(data, means, l_rate):
        for i in range(n):
            rand.shuffle(data)
            for point in data:
                update(point, means, l_rate)


    def partition(data, means):
        clusters = [[] for i in means]
        for point in data:
            dist_point = lambda x: dist(point, x)
            minimum = min(means, key = dist_point)
            for index, mean in enumerate(means):
                if mean is minimum:
                    break
            clusters[index].append(point)
        return clusters


    def master(data_points, n_clusters, n, l_rate):
        data, means = initialize(data_points, n_clusters)
        main(data, means, 0.1)
        main(data, means, l_rate)
        return partition(data, means), means

    return master(data_points, n_clusters, n, l_rate)



def scanner(data, epsilon, density):
    
    def cluster(ball, data):
        queue = [point for point in ball]
        visit = []
        while queue:
            point = queue.pop()
            visit.append(point)
            ball, data = take_ball(point, data)
            queue.extend(point for point in ball)
        return visit, data


    def take_ball(point, data):
        diff = data - point
        dots = umath.inner1d(diff, diff)
        ball = data[dots <= epsilon]
        data = data[dots >  epsilon]
        return ball, data


    def main(data):
        clusters = []
        data = data.copy()
        i = 0
        while data:
            diff = data - data[i]
            dots = umath.inner1d(diff)
            ball = data[dots <= epsilon]
            if len(ball) > density:
                data = data[dots > epsilon]
                group, data = cluster(ball, data)
                clusters.append(group)
                i = 0
            else:
                i += 1



    def master(data):
        data = [list(point) for point in data]






import matplotlib.pyplot as plt
#plt.scatter(data.data[:,2], data.data[:,1])
#plt.show()
data = datasets.load_iris()
data = list(zip(data.data[:,2], data.data[:,0]))
(a, b, c), means = stochastic_cluster(data, 3)
data_1 = list(zip(*a))
data_2 = list(zip(*b))
data_3 = list(zip(*c))
plt.scatter(*means[0], s = 100, c = 'y')
plt.scatter(*means[1], s = 100, c = 'y')
plt.scatter(*means[2], s = 100, c = 'y')
plt.scatter(*data_1, c = 'b')
plt.scatter(*data_2, c = 'r')
plt.scatter(*data_3, c = 'g')
plt.show()


