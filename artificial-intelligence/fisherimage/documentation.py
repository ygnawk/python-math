
import random
import fisherimage as fi



# create pseudodata
one = [(random.randrange(100),
		random.randrange(100)) for i in range(100)]
two = [(random.randrange(80, 180),
		30+random.randrange(80, 180)) for i in range(100)]
three =[(random.randrange(180, 260),
		random.randrange(180, 260)) for i in range(100)]
target = ([1 for i in range(100)]
		 + [2 for i in range(100)]
		 + [3 for i in range(100)])

data = one + two + three

# initialize a new linear_discriminant
linear_dis = fi.linear_discriminant(data, target)


# train the structure
linear_dis.train()


# get the notmal to the dividing plane 
print(linear_dis.principal_vec)

# plot stuff
import matplotlib.pyplot as plt

x,y = linear_dis.principal_vec

plt.scatter(*zip(*one), color = 'r')
plt.scatter(*zip(*two), color = 'b')
plt.scatter(*zip(*three), color = 'g')

plt.plot(*[(a*x, a*y) for a in range(250)])

plt.show()



