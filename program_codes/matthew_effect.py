import numpy as np
import matplotlib.pyplot as plt

N = np.arange(1, 20)
max_capacity = []
p = 0.5

for length in N: # take a particular length
    capacity = p # initiate with BEC's transition probability.
    for i in range(length):
        capacity = 2*capacity - capacity**2 # iteratively update capacity as per Arikkan's formula
    max_capacity.append(capacity)

plt.stem(N, max_capacity)
plt.xlabel('Codeword length')
plt.ylabel('Maximum Capacity')
plt.show()
