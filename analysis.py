import numpy as np
import matplotlib.pyplot as plt


nu,p,err = np.genfromtxt('data/summary.txt', delimiter=',', unpack=True)
nu2,p2,err2 = np.genfromtxt('data/risk_curve_data.txt', delimiter=',', unpack=True)

plt.errorbar(nu,p,yerr=err, fmt='k.')
plt.errorbar(nu2,p2,yerr=err2, fmt='b.')

plt.show()

