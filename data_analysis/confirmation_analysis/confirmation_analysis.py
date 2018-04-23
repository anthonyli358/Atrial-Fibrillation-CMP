import numpy as np
import matplotlib.pyplot as plt
import glob
files = {}
for y in np.arange(0.02,0.30,0.01):
    try:
        file_name = '{}.txt'.format(str(y))
        files[y] = np.genfromtxt(file_name, delimiter=',', unpack=True,
                                skip_header=1,skip_footer=2)[0]
    except:
        pass

# data = []
# datapoints = []
# for nu in files:
#     w = np.percentile(files[nu], [5, 25, 50, 75, 95])
#     data.append([nu] + list(w))
#     for file in files[nu]:
#         datapoints.append([nu, file])
#
# datapoints = np.transpose(datapoints)
#
# print(datapoints)
# plt.plot(datapoints[0], datapoints[1], '.')
#
# data = np.array(data)
# data = data[np.argsort(data[:, 0])]
# print(data)
# plt.plot(data[:, 0], data[:, 1:], )

nu,p,err = np.genfromtxt('summary.txt', delimiter=',', unpack=True)
nu2,p2,err2 = np.genfromtxt('risk_curve_data.txt', delimiter=',', unpack=True)

# plt.errorbar(nu,p,yerr=err/np.sqrt(48), fmt='k.', capsize=3, label='Model Implementation')
# plt.errorbar(nu2,p2,yerr=err2, fmt='b.', capsize=3, label='Previous CMP Data ')
# plt.legend(loc=0)
# plt.ylabel('Mean risk')
# plt.xlabel('y connectivity')
plt.errorbar(nu, p, yerr=err / np.sqrt(48), fmt='k.', color='r', capsize=3, label='Numerical')
plt.plot(nu, theor, color='b', label="Theoretical")
plt.xlabel(r"Fraction of transverse connections $\nu$")
plt.ylabel("Mean time in AF / AF risk probability")
plt.legend(loc=0, fontsize=12)
plt.show()

plt.show()
