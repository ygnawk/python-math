
import random as r
import svm as s

# add data points
num_sample = 100
xs = ( [r.randrange(num_sample) + num_sample 	for i in range(num_sample)]
	 + [r.randrange(num_sample + 50) 				for i in range(num_sample)])
ys = ( [r.randrange(num_sample + 50) 				for i in range(num_sample)]
	 + [r.randrange(num_sample, 2*num_sample) for i in range(num_sample)])
data = list(zip(xs, ys))

#pick targets
target = [1 for i in range(num_sample)] + [-1 for i in range(num_sample)]

# create a new support vector machine
svm = s.support_vector_machine(data, target)

# train
svm.train()

# plot points
# note that plotting can only be done
# when the data set is two dimensional
svm.plot()

# classify data point. 
# A positive value means 1 a negative value means -1
point = (12, 12)
print("Score:", svm.classify(point))


#returns all significant alphas along with the associated points
for point, target, alphas in svm.support_vectors:
	print('Support Vector:', point, target, alphas)



