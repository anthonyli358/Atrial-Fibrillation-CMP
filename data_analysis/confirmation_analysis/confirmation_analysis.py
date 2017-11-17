import numpy as np
import matplotlib.pyplot as plt
import glob

files = {}
for file_name in glob.glob('data/0.*.txt'):
    files[float(file_name[5:-4])] = np.genfromtxt(file_name, delimiter=',', unpack=True,
                                                  skip_header=1, skip_footer=2)[0]

data = []
datapoints = []
for nu in files:
    w = np.percentile(files[nu], [5, 25, 50, 75, 95])
    data.append([nu] + list(w))
    for file in files[nu]:
        datapoints.append([nu, file])

datapoints = np.transpose(datapoints)

print(datapoints)
plt.plot(datapoints[0], datapoints[1], '.')

data = np.array(data)
data = data[np.argsort(data[:, 0])]
print(data)
plt.plot(data[:, 0], data[:, 1:], )

# nu,p,err = np.genfromtxt('data/summary.txt', delimiter=',', unpack=True)
# nu2,p2,err2 = np.genfromtxt('data/risk_curve_data.txt', delimiter=',', unpack=True)
#
# plt.errorbar(nu,p,yerr=err/np.sqrt(48), fmt='k.', capsize=3)
# plt.errorbar(nu2,p2,yerr=err2, fmt='b.', capsize=3)

plt.show()
