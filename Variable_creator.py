import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0.1,1,.02)
yz = np.arange(0.1,1,.02)
grid = np.zeros((len(x),len(yz)))

list = []

for v, i in enumerate(x):
    for _, j in enumerate(yz):
        if 0.36*i*i - 0.79*i + 0.25 <= j <= 0.375*i*i - 0.825*i +0.65:
            list.append([i,j])
            grid[_,v] = True


variables = np.array(list)

np.save('nu_variables_low_res', variables)
