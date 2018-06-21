import matplotlib.pyplot as plt
import numpy as np
import glob
import os


def plot_risk_curve_data():
    """
    [runs [seed, AF?, x, y, z, time AF/end, conduction block?]]
    :return:
    """

    nu_yz_val = np.arange(0.005, 1, 0.01)
    nu_x_val = np.arange(0.005, 1, 0.01)
    X, Y = np.meshgrid(nu_x_val, nu_yz_val)
    Z = np.zeros(X.shape)
    time = np.zeros_like(Z)
    var = np.zeros_like(Z)
    wabwab = np.zeros(X.shape)
    avz = np.zeros_like(Z)
    varz = np.zeros_like(Z)
    end_time = np.zeros_like(Z)
    conduction_block = np.zeros_like(Z)
    non_zero_coordinates = np.zeros_like(Z)
    mask = np.load('nu_variables_exact_1821.npy')
    new_mask = []
    fib_check = 0

    for yi in range(len(nu_yz_val)):
        for xi in range(len(nu_x_val)):
            x = X[xi, yi]
            y = Y[xi, yi]
            try:
                path = "afinduced_data"
                file = 'risk_curve_data_1000_25_{:.3f}_{:.3f}*'.format(x, y).replace('.', '')
                filename = glob.glob("{path}/{file}".format(path=path, file=file))
                # check & move duplicate files
                if len(filename) > 1:
                    if not os.path.exists('{path}/duplicates'.format(path=path)):
                        os.makedirs('{path}/duplicates'.format(path=path))
                    for nfile in filename:
                        risk_data = np.load(nfile)
                        print(np.sum(risk_data[999, 1:6]))
                    os.rename(filename[1], filename[1].replace("{}".format(path), "{}/duplicates".format(path)))
                    filename = filename[0]
                else:
                    filename = filename[0]
                # print(filename)
                risk_data = np.load(filename)
                if np.sum(risk_data[:, 1]) > 0:
                    fib_check += 1

                ave = np.average(risk_data[:, 1])
                var[xi, yi] = np.std(risk_data[:, 1])
                fib = risk_data[risk_data[:, 1] == 1]
                no_fib = risk_data[(risk_data[:, 1] == 0) & (risk_data[:, -1] == 1)]
                time[xi, yi] = np.average(fib[:, 5])
                end_time[xi, yi] = np.average(no_fib[:, 5])
                normz = (np.absolute((fib[:, 2]).astype('int') - 12))
                avz[xi, yi] = np.average(normz)
                varz[xi, yi] = np.std(normz)
                conduction_block[xi, yi] = np.average(risk_data[:, -1])

            except:
                ave = 0
                pass
            Z[xi, yi] = ave - .5 * (ave == 0)

            # if ave:
            #     new_mask.append([x,y])
            #     non_zero_coordinates[yi, xi] = True
            if [x, y] in mask:
                non_zero_coordinates[xi, yi] = True
                # if 0.36 * x * x - 0.79 * x + 0.25 <= y <= 0.375 * x * x - 0.825 * x + 0.65:
                #     wabwab[xi,yi] = True

    # res = 0.36*X*X - 0.79*X +0.43 <= Y <= 0.375*X*X - 0.825*X +0.65
    plt.imshow(Z, extent=(0, 1, 0, 1), origin='lower', zorder=1)
    plt.title('Risk curve')
    # plt.contour(X,Y,Z, levels=[.1,.9], colors='w')
    grid_args = dict(color='w',
                     alpha=.4)
    plt.plot(nu_x_val, nu_x_val * np.tan(15 * np.pi / 180), **grid_args)
    plt.plot(nu_x_val, nu_x_val * np.tan(30 * np.pi / 180), **grid_args)
    plt.plot(nu_x_val, nu_x_val * np.tan(45 * np.pi / 180), **grid_args)
    plt.plot(nu_x_val, nu_x_val * np.tan(60 * np.pi / 180), **grid_args)
    plt.plot(nu_x_val, nu_x_val * np.tan(75 * np.pi / 180), **grid_args)
    plt.plot(3 * .5 - nu_yz_val * 2, nu_yz_val, **grid_args)
    plt.plot(3 * .4 - nu_yz_val * 2, nu_yz_val, **grid_args)
    plt.plot(3 * .3 - nu_yz_val * 2, nu_yz_val, **grid_args)
    plt.plot(3 * .2 - nu_yz_val * 2, nu_yz_val, **grid_args)
    plt.plot(3 * .1 - nu_yz_val * 2, nu_yz_val, **grid_args)
    plt.xlim((0, 1))
    plt.ylim((0, 1))

    plt.figure()
    plt.imshow(time, extent=(0, 1, 0, 1), origin='lower', zorder=3)
    plt.title('Time to fibrillation')
    plt.clim((50, 600))
    # plt.imshow(wabwab, extent=(0,1,0,1), origin='lower', alpha=.1,zorder=2)

    plt.figure()
    plt.imshow(avz, extent=(0, 1, 0, 1), origin='lower')
    plt.title('Averaege z')

    plt.figure()
    plt.imshow(avz, extent=(0, 1, 0, 1), origin='lower', vmin=5, vmax=10)
    plt.title('Averaege z')

    plt.figure()
    plt.imshow(conduction_block, extent=(0, 1, 0, 1), origin='lower')
    plt.title('Conduction Block')

# plt.figure()
# plt.imshow(non_zero_coordinates, extent=(0, 1, 0, 1), origin='lower')
# plt.title('Mask')

    plt.figure()
    plt.imshow(non_zero_coordinates, extent=(0, 1, 0, 1), origin='lower')
    plt.title('Mask')

    plt.show()

def plot_af_time_data():
    # (nu_x_val, nu_yz_val) = np.load('nu_variables_exact_1821.npy')[90:110].transpose()
    nu_yz_val = np.arange(0.035, .055, 0.01)
    nu_x_val = nu_yz_val + .39  # np.arange(0.005, 1, 0.01)
    X, Y = np.meshgrid(nu_x_val, nu_yz_val)
    Z = np.zeros(X.shape)
    time = np.zeros_like(Z)
    num = np.zeros_like(Z)
    ind_time = np.zeros_like(Z)

    for yi in range(len(nu_yz_val)):
        for xi in range(len(nu_x_val)):
            x = X[xi, yi]
            y = Y[xi, yi]
            print(x, y)
            try:
                start = 'af_time_data_25_5_{:.3f}_{:.3f}*'.format(y, x).replace('.', '')
                print(glob.glob(start))
                filename = glob.glob(start)[0]
                risk_data = np.load(filename).tolist()
                fibrillating = risk_data[[(i[1] != 0) for i in risk_data]]
                time[xi, yi] = np.average([i[1] for i in risk_data])
                num[xi, yi] = np.average([len(i) / 2 - 1 for i in fibrillating])
                print(np.average([np.average(np.array(i[3::2]) - np.array(i[2::2])) for i in risk_data]))
                ind_time[xi, yi] = np.average([np.average(np.array(i[3::2]) - np.array(i[2::2])) for i in risk_data])
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
    plt.plot(nu_x_val, nu_x_val * np.tan(15 * np.pi / 180), **grid_args)
    plt.plot(nu_x_val, nu_x_val * np.tan(30 * np.pi / 180), **grid_args)
    plt.plot(nu_x_val, nu_x_val * np.tan(45 * np.pi / 180), **grid_args)
    plt.plot(nu_x_val, nu_x_val * np.tan(60 * np.pi / 180), **grid_args)
    plt.plot(nu_x_val, nu_x_val * np.tan(75 * np.pi / 180), **grid_args)
    plt.plot(3 * .5 - nu_yz_val * 2, nu_yz_val, **grid_args)
    plt.plot(3 * .4 - nu_yz_val * 2, nu_yz_val, **grid_args)
    plt.plot(3 * .3 - nu_yz_val * 2, nu_yz_val, **grid_args)
    plt.plot(3 * .2 - nu_yz_val * 2, nu_yz_val, **grid_args)
    plt.plot(3 * .1 - nu_yz_val * 2, nu_yz_val, **grid_args)
    plt.xlim((0, 1))
    plt.ylim((0, 1))

    plt.figure()
    plt.imshow(num, extent=(0, 1, 0, 1), origin='lower', zorder=3)
    plt.title('Number of circuit restarts')
    # plt.imshow(wabwab, extent=(0,1,0,1), origin='lower', alpha=.1,zorder=2)
    plt.figure()
    plt.imshow(ind_time, extent=(0, 1, 0, 1), origin='lower', zorder=3)
    plt.title('Single circuit duration')

    plt.show()


def plot_con_vel_data():
    """
    [runs[seed, time, bulk (av, max, min), z=0 (av, max, min), z=24 (av, max, min)]]
    :return:
    """

    nu_yz_val = np.arange(0.2, 1.01, 0.2)
    nu_x_val = np.arange(0.2, 1.01, 0.2)
    X, Y = np.meshgrid(nu_x_val, nu_yz_val)
    Z = np.zeros(X.shape)

    for yi in range(len(nu_yz_val)):
        for xi in range(len(nu_x_val)):
            x = X[xi, yi]
            y = Y[xi, yi]
            try:
                path = "con_vel_data_test"
                file = 'con_vel_data_5_25_{:.3f}_{:.3f}*'.format(x, y).replace('.', '')
                filename = glob.glob("{path}/{file}".format(path=path, file=file))
                # check & move duplicate files
                if len(filename) > 1:
                    if not os.path.exists('{path}/duplicates'.format(path=path)):
                        os.makedirs('{path}/duplicates'.format(path=path))
                    for nfile in filename:
                        risk_data = np.load(nfile)
                        print(risk_data[-1, :])
                    os.rename(filename[1], filename[1].replace("{}".format(path), "{}/duplicates".format(path)))
                    filename = filename[0]
                else:
                    filename = filename[0]
                # print(filename)
                risk_data = np.load(filename)

                ave = np.average(risk_data[:, 2] / risk_data[:, 1])

            except OSError:
                ave = 0
                pass

            Z[xi, yi] = ave

    plt.imshow(Z, extent=(0, 1, 0, 1), origin='lower', zorder=1)
    plt.title('Conduction velocity')

    plt.show()


if __name__ == '__main__':
    # plot_risk_curve_data()
    plot_con_vel_data()
