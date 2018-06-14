import config
from model import Model
from utility_methods import *
import h5py
import numpy as np
import time


def risk_curve_data(runs, repeats, l_z, nu_x, nu_yz, angle_vars=False, t=100000):
    data = np.zeros(shape=(runs, repeats, 3), dtype='uint32')
    params = config.settings["structure"]
    params["size"][0], params["seed"] = l_z, None
    params["x_coupling"], params["yz_coupling"] = nu_x, nu_yz
    params["angle_toggle"], params["angle_vars"] = angle_vars, angle_vars
    print("l_z: {}, nu_x: {}, nu_yz: {}, angle_vars: {}".format(l_z, nu_x, nu_yz, angle_vars))
    start = time.time()
    for i in range(runs):
        tissue = Model(**params)
        for j in range(repeats):
            tissue.model_array.fill(0)  # Clear activations
            tissue.excount.fill(0)  # Clear excitation count
            tissue.activate_pacemaker()  # Initialise new wavefront
            tissue.time = 0
            data[i, j, 0] = tissue.seed
            while tissue.time < t:
                excitations = tissue.iterate()
                if np.intersect1d(tissue.excount, [2]):
                    maxpos = tissue.maxpos
                    data[i, j, 1] = 1
                    data[i, j, 2] = maxpos[0] * 100000 + maxpos[1] * 1000 + maxpos[2]
                    break
                elif not np.any(excitations == 50):
                    data[i, j, 2] = tissue.time
                    break
            print('Run: {}, Repeat: {}, Data: {}'.format(i + 1, j + 1, data[i][j]))
    print("time={}".format(time.time() - start))

    return data


def af_time_data(runs, repeats, l_z, nu_x, nu_yz, angle_vars=False, t=100000):
    data = np.zeros(shape=(runs, repeats, 3), dtype='uint32')
    params = config.settings["structure"]
    params["size"][0], params["seed"] = l_z, None
    params["x_coupling"], params["yz_coupling"] = nu_x, nu_yz
    params["angle_toggle"], params["angle_vars"] = angle_vars, angle_vars
    print("l_z: {}, nu_x: {}, nu_yz: {}, angle_vars: {}".format(l_z, nu_x, nu_yz, angle_vars))
    start = time.time()
    for i in range(runs):
        tissue = Model(**params)
        for j in range(repeats):
            tissue.model_array.fill(0)  # Clear activations
            tissue.excount.fill(0)
            tissue.time = 0
            data[i, j, 0] = tissue.seed
            fib_time = 0
            while tissue.time < t:
                if tissue.time % 220 == 0:
                    tissue.activate_pacemaker()
                tissue.iterate()
                if tissue.maxpos[2] > 1:
                    data[i, j, 1] = 1  # Fibrillation
                    fib_time += 1
            data[i, j, 2] = fib_time
            print('Run: {}, Repeat: {}, Data: {}'.format(i + 1, j + 1, data[i][j]))
    print("time={}".format(time.time() - start))

    return data


def gen_risk(runs, repeats, l_z, nu_x_range, nu_yz_range, angle_vars=False, t=100000, time_data=False):
    risk_type = af_time_data if time_data else risk_curve_data
    dir_name = "new_risk_angled" if angle_vars else "new_risk_homogeneous"
    if not os.path.exists('data_analysis/{}'.format(dir_name)):
        os.makedirs('data_analysis/{}'.format(dir_name))

    if angle_vars:
        for av in angle_vars[2]:
            result = risk_type(runs, repeats, l_z, 1.0, 1.0, [angle_vars[0], angle_vars[1], av], t)
            with h5py.File('data_analysis/{}/{}, runs={}, repeats={}, l_z={}, ang_epi={}, ang_endo={}, nu_av={}'.format(
                    dir_name, runs, repeats, risk_type.__name__, l_z, angle_vars[0], angle_vars[1], av), 'w') as data_file:
                data_file.create_dataset('risk', data=result, dtype='uint32')
    else:
        for x in nu_x_range:
            for yz in nu_yz_range:
                if not 0.45 < x + yz / 2 < 0.6:
                    break
                result = risk_type(runs, repeats, l_z, x, yz, False, t)
                with h5py.File('data_analysis/{}/{}, runs={}, repeats={}, l_z={}, nu_x={}, nu_yz={}'.format(
                        dir_name, runs, repeats, risk_type.__name__, l_z, x, yz), 'w') as data_file:
                    data_file.create_dataset('risk', data=result, dtype='uint32')


if __name__ == '__main__':
    for i in [1]:
        gen_risk(runs=100, repeats=1, l_z=i, nu_x_range=np.arange(0.01, 1, 0.01), nu_yz_range=np.arange(0.01, 1, 0.01),
                 angle_vars=False, t=100000, time_data=False)
        # gen_risk(runs=25, repeats=1, l_z=i, nu_x_range=[0.1, 0.3, 0.5, 0.7, 0.9], nu_yz_range=[0.1, 0.3, 0.5, 0.7, 0.9],
        #          angle_vars=False, t=10000, time_data=True)
