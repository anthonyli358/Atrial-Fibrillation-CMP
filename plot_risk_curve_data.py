import h5py
import numpy as np


path = "new_risk_homogeneous/l_z=1, nu_x=1.0, nu_yz=0"

af_risk = []
for l_z in [1]:
    for nu_x in [1.0]:
        for nu_yz in [0.1, 0.2]:
            with h5py.File('data_analysis/new_risk_homogeneous/l_z={}, nu_x={}, nu_yz={}'.format(l_z, nu_x, nu_yz),
                           'r') as data_file:
                risk_data = data_file['risk'][:]
            af_risk.append([nu_x, nu_yz, np.sum(risk_data[:, :, 1]) / len(risk_data[:, :, 1])])

print(af_risk)
