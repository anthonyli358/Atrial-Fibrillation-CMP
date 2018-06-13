import config
from model import Model
from utility_methods import *
import h5py
import numpy as np
import time


def risk_curve_data(runs, repeats, l_z, nu_x, nu_yz, angle_vars=False, time=100000):
    data = np.zeros(shape=(runs, repeats, 3), dtype='uint32')
    params = config.settings["structure"]
    params["size"][0], params["seed"] = l_z, None
    params["x_coupling"], params["yz_coupling"] = nu_x, nu_yz
    params["angle_toggle"], params["angle_vars"] = angle_vars, angle_vars
    for i in range(runs):
        tissue = Model(**params)
        for j in range(repeats):
            tissue.model_array.fill(0)  # Clear activations
            data[i][j][0] = tissue.seed
            ended = False
            for t in range(time):
                if t % 1000 == 0:
                    tissue.excount.fill(0)  # Clear excitation count
                    tissue.activate_pacemaker()
                excitations = tissue.iterate()
                if np.intersect1d(tissue.excount, [2]):
                    maxpos = tissue.maxpos
                    data[i][j][1] = True
                    data[i][j][2] = maxpos[0] * 100000 + maxpos[1] * 1000 + maxpos[2]
                    break
                elif ended is False:
                    if not np.any(excitations == 50):
                        data[i][j][2] = t + 1
                        ended = True
            print('Run: {}, Repeat: {}, Data: {}'.format(i, j, data[i][j]))

    return data


def af_time_data(runs, repeats, l_z, nu_x, nu_yz, angle_vars=False, time=1000):
    data = np.zeros(shape=(runs, repeats, 3), dtype='uint32')
    params = config.settings["structure"]
    params["size"][0], params["seed"] = l_z, None
    params["x_coupling"], params["yz_coupling"] = nu_x, nu_yz
    params["angle_toggle"], params["angle_vars"] = angle_vars, angle_vars
    for i in range(runs):
        tissue = Model(**params)
        for j in range(repeats):
            tissue.model_array.fill(0)  # Clear activations
            tissue.excount.fill(0)
            tissue.time = 0
            data[i][j][0] = tissue.seed
            fib_time = 0
            while tissue.time < time:
                if tissue.time % 200 == 0:
                    tissue.activate_pacemaker()
                tissue.iterate()
                if tissue.maxpos[2] > 1:
                    data[i][j][1] 1  # No fibrillation
                    fib_time += 1
            data[i][j][2] = fib_time

            print('Run: {}, Repeat: {}, Data: {}'.format(i, j, data[i][j]))

    return data

def gen_risk(runs, repeats, l_z, nu_x_range, nu_yz_range, angle_vars=False,
             time=100000, dir_name="new_risk_homogeneous"):
    if not os.path.exists('data_analysis/{}'.format(dir_name)):
        os.makedirs('data_analysis/{}'.format(dir_name))
    if angle_vars:
        for av in angle_vars[2]:
            result = af_time_data(runs, repeats, l_z, 1.0, 1.0, [angle_vars[0], angle_vars[1], av], time)
            with h5py.File('data_analysis/{}/l_z={}, ang_epi={}, ang_endo={}, nu_av={}'.format(
                    dir_name, l_z, angle_vars[0], angle_vars[1], av), 'w') as data_file:
                data_file.create_dataset('risk', data=result, dtype='uint32')
    else:
        for x in nu_x_range:
            for yz in nu_yz_range:
                result = af_time_data(runs, repeats, l_z, x, yz, False, time)
                with h5py.File('data_analysis/{}/l_z={}, nu_x={}, nu_yz={}'.format(
                        dir_name, l_z, x, yz), 'w') as data_file:
                    data_file.create_dataset('risk', data=result, dtype='uint32')


if __name__ == '__main__':
    for i in [ 25]:
        start = time.time()
        gen_risk(runs=100, repeats=1, l_z=i, nu_x_range=[.7], nu_yz_range=[0.12], angle_vars=False, time=1000)
        print(time.time() - start)
