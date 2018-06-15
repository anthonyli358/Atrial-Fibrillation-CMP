import h5py
import matplotlib.pyplot as plt
import numpy as np
import glob


nu_yz_val = np.arange(0.1, 1, 0.02)
nu_x_val = np.arange(0.1, 1, 0.02)
X,Y = np.meshgrid(nu_x_val,nu_yz_val)
Z = np.zeros(X.shape)
wabwab = np.zeros(X.shape)

example = 'risk_curve_data_5_0100_0500_False_10000_eb8610e35046e63f'
files = glob.glob('risk_curve_data_5_*')

for yi in range(len(nu_yz_val)):
    for xi in range(len(nu_x_val)):
        x = X[xi,yi]
        y = Y[xi,yi]
        try:
            start = 'risk_curve_data_25_{:.3f}_{:.3f}*'.format(x,y).replace('.', '')
            filename = glob.glob(start)[0]
            # print(filename)
            risk_data = np.load(filename)
            Z[xi,yi] = np.sum(risk_data[:, 1]) / risk_data[:, 1].size
        except:
            pass
        if 0.36 * x * x - 0.79 * x + 0.25 <= y <= 0.375 * x * x - 0.825 * x + 0.65:
            wabwab[xi,yi] = True

# res = 0.36*X*X - 0.79*X +0.43 <= Y <= 0.375*X*X - 0.825*X +0.65
plt.imshow(Z, extent=(0,1,0,1), origin='lower')
plt.imshow(wabwab, extent=(0,1,0,1), origin='lower', alpha=.1,zorder=2)
plt.show()
