import h5py
import matplotlib.pyplot as plt
import numpy as np


path = "new_risk_homogeneous/risk_curve_data, runs=100, repeats=1, time=100000"

nu_yz_val = np.arange(0.01, 1, 0.01)
nu_x_val = np.arange(0.01, 1, 0.01)
af_risk = np.zeros(shape=(len(nu_yz_val), len(nu_x_val)))

for l_z in [1]:
    for i, nu_yz in enumerate(nu_yz_val):
        for j, nu_x in enumerate(nu_x_val):
            try:
                with h5py.File('data_analysis/{}/l_z={}, nu_x={:.2f}, nu_yz={:.2f}'.format(
                        path, l_z, nu_x, nu_yz), 'r') as data_file:
                    risk_data = data_file['risk'][:]
                af_risk[i, j] = np.sum(risk_data[:, :, 1]) / risk_data[:, :, 1].size
            except OSError:
                pass

print(np.array(af_risk))
plt.imshow(af_risk, extent=(0, 1, 0, 1), origin='lower')
plt.xlabel("nu_x")
plt.ylabel("nu_yz")
plt.colorbar()
plt.show()
