import h5py
import matplotlib.pyplot as plt
import numpy as np
import glob

# (nu_x_val, nu_yz_val) = np.load('nu_variables_exact_1821.npy')[90:110].transpose()
nu_yz_val = np.arange(0.035, .055, 0.01)
nu_x_val = nu_yz_val +.39 #np.arange(0.005, 1, 0.01)
X, Y = np.meshgrid(nu_x_val, nu_yz_val)
Z = np.zeros(X.shape)
time = np.zeros_like(Z)
num = np.zeros_like(Z)
ind_time = np.zeros_like(Z)


# seed, AF?, (AF on, AF off),etc.

for yi in range(len(nu_yz_val)):
    for xi in range(len(nu_x_val)):
        x = X[xi, yi]
        y = Y[xi, yi]
        print(x,y)
        try:
            start = 'af_time_data_25_5_{:.3f}_{:.3f}*'.format(y, x).replace('.', '')
            print(glob.glob(start))
            filename = glob.glob(start)[0]
            risk_data = np.load(filename).tolist()
            time[yi,xi] = np.average([i[1] for i in risk_data])
            num[yi,xi] = np.average([len(i)/2 - 1 for i in risk_data])
            print(np.average([np.average(np.array(i[3::2])-np.array(i[2::2])) for i in risk_data]))
            ind_time[yi,xi] = np.average([np.average(np.array(i[3::2])-np.array(i[2::2])) for i in risk_data])
            # ave = np.average(risk_data[:, 1])
            # var[yi, xi] = np.std(risk_data[:, 1])
            # fib = risk_data[risk_data[:, 1] == 1]
            # no_fib = risk_data[(risk_data[:, 1] == 0) & (risk_data[:, -1] == 1)]
            # time[yi, xi] = np.average(fib[:, 5])
            # end_time[yi, xi] = np.average(no_fib[:, 5])
            # normz = (np.absolute((fib[:, 2]).astype('int') - 12))
            # avz[yi, xi] = np.average(normz)
            # varz[yi, xi] = np.std(normz)
            # conduction_block[yi, xi] = np.average(risk_data[:, -1])


        except:
            ave = 0
            pass

        Z[yi, xi] = ave - .5 * (ave == 0)


# res = 0.36*X*X - 0.79*X +0.43 <= Y <= 0.375*X*X - 0.825*X +0.65
plt.imshow(time, extent=(0, 1, 0, 1), origin='lower', zorder=1)
plt.title('Risk curve')
# plt.contour(X,Y,Z, levels=[.1,.9], colors='w')
grid_args = dict(color='w',
                 alpha=.4)
# plt.plot(nu_x_val, nu_x_val * np.tan(15 * np.pi / 180), **grid_args)
# plt.plot(nu_x_val, nu_x_val * np.tan(30 * np.pi / 180), **grid_args)
# plt.plot(nu_x_val, nu_x_val * np.tan(45 * np.pi / 180), **grid_args)
# plt.plot(nu_x_val, nu_x_val * np.tan(60 * np.pi / 180), **grid_args)
# plt.plot(nu_x_val, nu_x_val * np.tan(75 * np.pi / 180), **grid_args)
# plt.plot(nu_x_val, 3 * .5 - nu_x_val * 2, **grid_args)
# plt.plot(nu_x_val, 3 * .4 - nu_x_val * 2, **grid_args)
# plt.plot(nu_x_val, 3 * .3 - nu_x_val * 2, **grid_args)
# plt.plot(nu_x_val, 3 * .2 - nu_x_val * 2, **grid_args)
# plt.plot(nu_x_val, 3 * .1 - nu_x_val * 2, **grid_args)
# plt.xlim((0, 1))
# plt.ylim((0, 1))


plt.figure()
plt.imshow(num, extent=(0, 1, 0, 1), origin='lower', zorder=3)
plt.title('Number of circuit restarts')
# plt.imshow(wabwab, extent=(0,1,0,1), origin='lower', alpha=.1,zorder=2)
plt.figure()
plt.imshow(ind_time, extent=(0, 1, 0, 1), origin='lower', zorder=3)
plt.title('Single circuit duration')

plt.show()
