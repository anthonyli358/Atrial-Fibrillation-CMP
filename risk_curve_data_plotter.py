import matplotlib.pyplot as plt
import numpy as np
import glob
import os


def plot_risk_curve_data(path=None):
    """
    data structure = [runs [seed, AF?, x, y, z, time AF/end, conduction block?]]
    :param path: folder path
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
    fib_check = 0

    for yi in range(len(nu_yz_val)):
        for xi in range(len(nu_x_val)):
            x = X[xi, yi]
            y = Y[xi, yi]
            try:
                file = 'risk_curve_data_1000_25_{:.3f}_{:.3f}*'.format(x, y).replace('.', '')
                if path:
                    filename = glob.glob("{path}/{file}".format(path=path, file=file))
                else:
                    filename = glob.glob("{}".format(file))
                # check & move duplicate files
                if len(filename) > 1:
                    if not os.path.exists('{path}/duplicates'.format(path=path)):
                        os.makedirs('{path}/duplicates'.format(path=path))
                    for nfile in filename:
                        risk_data = np.load(nfile)
                        print("duplicate found, last array value is: {risk_data}".format(risk_data=risk_data[-1, :]))
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

            except OSError:
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

    plt.figure()
    plt.imshow(non_zero_coordinates, extent=(0, 1, 0, 1), origin='lower')
    plt.title('Mask')

    plt.show()


def plot_af_time_data(path=None):
    """
    data structure = [runs [seed, AF?, {AF_on, AF_off},etc.]]
    :param path: folder path
    """
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
                file = 'af_time_data_1000_25_{:.3f}_{:.3f}*'.format(x, y).replace('.', '')
                if path:
                    filename = glob.glob("{path}/{file}".format(path=path, file=file))
                else:
                    filename = glob.glob("{}".format(file))
                # check & move duplicate files
                if len(filename) > 1:
                    if not os.path.exists('{path}/duplicates'.format(path=path)):
                        os.makedirs('{path}/duplicates'.format(path=path))
                    for nfile in filename:
                        risk_data = np.load(nfile)
                        print("duplicate found, last array value is: {risk_data}".format(risk_data=risk_data[-1, :]))
                    os.rename(filename[1], filename[1].replace("{}".format(path), "{}/duplicates".format(path)))
                    filename = filename[0]
                else:
                    filename = filename[0]
                # print(filename)
                risk_data = np.load(filename).tolist()

                fibrillating = risk_data[[(i[1] != 0) for i in risk_data]]
                time[xi, yi] = np.average([i[1] for i in risk_data])
                num[xi, yi] = np.average([len(i) / 2 - 1 for i in fibrillating])
                print(np.average([np.average(np.array(i[3::2]) - np.array(i[2::2])) for i in risk_data]))
                ind_time[xi, yi] = np.average([np.average(np.array(i[3::2]) - np.array(i[2::2])) for i in risk_data])

            except OSError:
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


def plot_con_vel_data(path=None):
    """
    data structure = [runs[seed, time, bulk (av, max, min), z=0 (av, max, min), z=24 (av, max, min)]]
    :param path: folder path
    """
    nu_yz_val = np.arange(0.2, 1.01, 0.2)
    nu_x_val = np.arange(0.2, 1.01, 0.2)
    X, Y = np.meshgrid(nu_x_val, nu_yz_val)
    Z = np.zeros(X.shape)
    time = np.zeros_like(Z)
    Z_range = np.zeros_like(Z)
    z_0 = np.zeros_like(Z)
    z_0_range = np.zeros_like(Z)
    z_24 = np.zeros_like(Z)
    z_24_range = np.zeros_like(Z)

    for yi in range(len(nu_yz_val)):
        for xi in range(len(nu_x_val)):
            x = X[xi, yi]
            y = Y[xi, yi]
            try:
                file = 'con_vel_data_5_25_{:.3f}_{:.3f}*'.format(x, y).replace('.', '')
                if path:
                    filename = glob.glob("{path}/{file}".format(path=path, file=file))
                else:
                    filename = glob.glob("{}".format(file))
                # check & move duplicate files
                if len(filename) > 1:
                    if not os.path.exists('{path}/duplicates'.format(path=path)):
                        os.makedirs('{path}/duplicates'.format(path=path))
                    for nfile in filename:
                        risk_data = np.load(nfile)
                        print("duplicate found, last array value is: {risk_data}".format(risk_data=risk_data[-1, :]))
                    os.rename(filename[1], filename[1].replace("{}".format(path), "{}/duplicates".format(path)))
                    filename = filename[0]
                else:
                    filename = filename[0]
                # print(filename)
                risk_data = np.load(filename)

                time[xi, yi] = np.average(risk_data[:, 1])
                Z[xi, yi] = np.average(risk_data[:, 2] / risk_data[:, 1])
                Z_range[xi, yi] = np.average((risk_data[:, 3] - risk_data[:, 4]) / risk_data[:, 1])
                z_0[xi, yi] = np.average(risk_data[:, 5] / risk_data[:, 1])
                z_0_range[xi, yi] = np.average((risk_data[:, 6] - risk_data[:, 7]) / risk_data[:, 1])
                z_24[xi, yi] = np.average(risk_data[:, 8] / risk_data[:, 1])
                z_24_range[xi, yi] = np.average((risk_data[:, 9] - risk_data[:, 10]) / risk_data[:, 1])

            except OSError:
                Z[xi, yi] = 0
                pass

    plt.figure()
    plt.imshow(time, extent=(0, 1, 0, 1), origin='lower', zorder=1)
    plt.title('Conduction time')

    plt.figure()
    plt.subplot(121)
    plt.imshow(Z, extent=(0, 1, 0, 1), origin='lower', zorder=1)
    plt.title('Conduction velocity')
    plt.subplot(122)
    plt.imshow(Z_range, extent=(0, 1, 0, 1), origin='lower', zorder=1)
    plt.title('Conduction velocity range')

    plt.figure()
    plt.subplot(221)
    plt.imshow(z_0, extent=(0, 1, 0, 1), origin='lower', zorder=1)
    plt.title('z=0 conduction velocity')
    plt.subplot(222)
    plt.imshow(z_24, extent=(0, 1, 0, 1), origin='lower', zorder=1)
    plt.title('z=24 conduction velocity')
    plt.subplot(223)
    plt.imshow(z_0_range, extent=(0, 1, 0, 1), origin='lower', zorder=1)
    plt.title('z=0 conduction velocity range')
    plt.subplot(224)
    plt.imshow(z_24_range, extent=(0, 1, 0, 1), origin='lower', zorder=1)
    plt.title('z=24 conduction velocity range')

    plt.show()


def plot_con_data(path=None):
    """
    data structure = [runs [seed, dys_seed, conduction?]]
    :param path: folder path
    """
    nu_yz_val = np.arange(0.005, 1, 0.01)
    nu_x_val = np.arange(0.005, 1, 0.01)
    X, Y = np.meshgrid(nu_x_val, nu_yz_val)
    Z = np.zeros(X.shape)
    conduction = np.zeros_like(Z)

    for yi in range(len(nu_yz_val)):
        for xi in range(len(nu_x_val)):
            x = X[xi, yi]
            y = Y[xi, yi]
            # print(x, y)
            try:
                file = 'conduction_1000_25_{:.3f}_{:.3f}*'.format(x, y).replace('.', '')
                if path:
                    filename = glob.glob("{path}/{file}".format(path=path, file=file))
                else:
                    filename = glob.glob("{}".format(file))
                # check & move duplicate files
                if len(filename) > 1:
                    if not os.path.exists('{path}/duplicates'.format(path=path)):
                        os.makedirs('{path}/duplicates'.format(path=path))
                    for nfile in filename:
                        risk_data = np.load(nfile)
                        print("duplicate found, last array value is: {risk_data}".format(risk_data=risk_data[-1, :]))
                    os.rename(filename[1], filename[1].replace("{}".format(path), "{}/duplicates".format(path)))
                    filename = filename[0]
                else:
                    filename = filename[0]
                # print(filename)
                risk_data = np.load(filename)

                conduction[xi, yi] = np.average(risk_data[:, -1])

            except OSError:
                ave = 0
                pass

            Z[yi, xi] = ave - .5 * (ave == 0)

            # res = 0.36*X*X - 0.79*X +0.43 <= Y <= 0.375*X*X - 0.825*X +0.65
    plt.imshow(conduction, extent=(0, 1, 0, 1), origin='lower', zorder=1)
    plt.title("Risk Curve")

    plt.show()


def read_af_pos_data(path=None):
    """
    data structure = [runs [repeats [seed, dys_seed, AF?, x, y, z]]]
    :param path: folder path
    :return: list of af source positions for each seed [[seed, (z, y, x),etc.],etc.]
    """
    nu_yz_val = [0.1]
    nu_x_val = [0.9]
    af_positions = []

    for yi in nu_yz_val:
        for xi in nu_x_val:
            try:
                file = 'af_pos_data_2_5_25_{:.3f}_{:.3f}*'.format(xi, yi).replace('.', '')
                if path:
                    filename = glob.glob("{path}/{file}".format(path=path, file=file))
                else:
                    filename = glob.glob("{}".format(file))
                # check & move duplicate files
                if len(filename) > 1:
                    if not os.path.exists('{path}/duplicates'.format(path=path)):
                        os.makedirs('{path}/duplicates'.format(path=path))
                    for nfile in filename:
                        risk_data = np.load(nfile)
                        print("Duplicate found, last array value is: {risk_data}.".format(risk_data=risk_data[-1, :]))
                        print("Moving final duplicate to 'duplicates' folder...")
                    os.rename(filename[-1], filename[-1].replace("{}".format(path), "{}/duplicates".format(path)))
                    filename = filename[0]
                else:
                    filename = filename[0]
                # print(filename)
                risk_data = np.load(filename)
                if len(risk_data) > 1:
                    print("More than one run in file, separating list into separate runs. "
                          "Data structure is [[seed, (z, y, x),etc.],etc.]")
                for i, run in enumerate(risk_data):
                    af_positions.append([risk_data[i, 0, 0]])
                    for repeat in run:
                        if repeat[2] == 1:
                            af_positions[i].append(tuple(repeat[3:6]))

            except OSError:
                raise Exception("File could not be loaded, check path and file name.")

    if path:
        np.save("{path}/{file}".format(path=path, file=os.path.split(filename)[1].replace(
            'af_pos_data', 'af_positions')), af_positions)
    else:
        np.save(os.path.split(filename)[1].replace('af_pos_data', 'af_positions'), af_positions)

    return af_positions


if __name__ == '__main__':
    # The 'path' parameter is the folder path for data.
    # Check for the function running that the nu_x, nu_yz / nu_av ranges
    # are correct and that the 'file' variable is of the correct format.
    # plot_risk_curve_data(path='data_analysis/data_afinduced/run_2')
    # plot_af_time_data(path='data_analysis/data_af_time')
    # plot_con_vel_data(path='data_con_vel')
    print(read_af_pos_data(path='data_af_pos'))
