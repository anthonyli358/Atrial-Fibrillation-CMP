import numpy as np

test = np.array([1, 4])
if np.intersect1d(test, [3]):
    print("hi")
if np.any(test == 2):
    print("yes")

a, b = 1, 2
print(np.arange(*[1, 2, 1]))
