import h5py
import matplotlib.pyplot as plt
import numpy as np


af_risk = []
for l_z in [1]:
    for i, nu_x in enumerate([0.1, 0.3, 0.5, 0.7, 0.9]):
        af_risk.append([])
        for nu_yz in [0.9, 0.7, 0.5, 0.3, 0.1]:
            with h5py.File('data_analysis/new_risk_homogeneous/risk_curve_data, l_z={}, nu_x={}, nu_yz={}'.format(
                    l_z, nu_x, nu_yz), 'r') as data_file:
                risk_data = data_file['risk'][:]
            af_risk[i].append(np.sum(risk_data[:, :, 1]) / risk_data[:, :, 1].size)

print(af_risk)
plt.imshow(af_risk, extent=(0, 1, 0, 1))  # imshow plots left to right, top to bottom
plt.xlabel("nu_x")
plt.ylabel("nu_yz")
plt.colorbar()
plt.show()
