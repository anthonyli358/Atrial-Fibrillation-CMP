import config
from model import Model
from utility_methods import *
import numpy as np
import time
import binascii
import sys


def risk_curve_data(runs, l_z, nu_x, nu_yz, angle_vars=False, t=100000):
    data = np.zeros(shape=(runs, 7), dtype='uint32')
    params = config.settings["structure"]
    params["size"][0], params["seed"] = l_z, None
    params["x_coupling"], params["yz_coupling"] = nu_x, nu_yz
    params["angle_toggle"], params["angle_vars"] = angle_vars, angle_vars
    # start = time.time()
    for i in range(runs):
        tissue = Model(**params)
        tissue.activate_pacemaker()  # Initialise new wavefront
        data[i, 0] = tissue.seed
        while tissue.time < t:
            excitations = tissue.iterate()
            if np.intersect1d(tissue.excount, [2]):
                data[i, 1] = True
                data[i, 2:5] = tissue.maxpos
                data[i, 5] = tissue.time
                break
            elif not np.any(excitations == 50):
                data[i, 5] = tissue.time
                break
            if np.any(excitations[:, :, -1]):
                data[i, 6] = True
    # print('Run: {}, Data: {}'.format(i + 1, data[i]))
    # print("time={}".format(time.time() - start))

    return data


def af_time_data(runs, l_z, nu_x, nu_yz, angle_vars=False, t=100000):
    data = []
    params = config.settings["structure"]
    params["size"][0], params["seed"] = l_z, None
    params["x_coupling"], params["yz_coupling"] = nu_x, nu_yz
    params["angle_toggle"], params["angle_vars"] = angle_vars, angle_vars
    # start = time.time()
    for i in range(runs):
        tissue = Model(**params)
        run_data = [tissue.seed, 0]
        prior = False
        while tissue.time <= t:
            if tissue.time % 220 == 0:
                tissue.activate_pacemaker()
            tissue.iterate()
            if tissue.maxpos[2] > 1:
                run_data[1] += 1
                new = True
            else:
                new = False
            if new != prior:
                run_data.append(tissue.time)
            prior = new
        if new:
            run_data.append(tissue.time)
        data.append(run_data)
    # print('Run: {}, Data: {}'.format(i + 1, data[i]))
    # print("time={}".format(time.time() - start))

    return data


def con_vel_data(runs, l_z, nu_x, nu_yz, angle_vars=False, t=100000):
    data = np.zeros(shape=(runs, 6), dtype='uint32')
    params = config.settings["structure"]
    params["size"][0], params["seed"] = l_z, None
    params["x_coupling"], params["yz_coupling"] = nu_x, nu_yz
    params["angle_toggle"], params["angle_vars"] = angle_vars, angle_vars
    # start = time.time()
    for i in range(runs):
        tissue = Model(**params)
        data[i, 0] = tissue.seed
        tissue.activate_pacemaker()  # Initialise new wavefront
        while tissue.time < t:
            excitations = tissue.iterate()
            if np.intersect1d(tissue.excount, [2]):
                data[i, 1] = True
                break
            elif np.any(excitations[:, :, -1]):
                data[i, 2] = tissue.time
                data[i, 3] = np.average(np.where(excitations == 50)[2])
                if angle_vars:
                    data[i, 4] = np.average(np.where(excitations[0, :, :] == 50)[1])
                    data[i, 5] = np.average(np.where(excitations[24, :, :] == 50)[1])
                break
            elif not np.any(excitations == 50):
                data[i, 2] = tissue.time
                data[i, 3] = np.average(np.where(excitations == 49)[2])
                if angle_vars:
                    data[i, 4] = np.average(np.where(excitations[0, :, :] == 50)[1])
                    data[i, 5] = np.average(np.where(excitations[24, :, :] == 50)[1])
                break
    # print('Run: {}, Data: {}'.format(i + 1, data[i]))
    # print("time={}".format(time.time() - start))
    return data


def gen_risk(runs, l_z, nu_x, nu_yz, angle_vars=False, t=100000, time_data=False):
    risk_type = af_time_data if time_data else risk_curve_data

    file_dict = dict(
        risk=risk_type.__name__,
        runs=runs,
        l_z=l_z,
        nu_x=nu_x,
        nu_yz=nu_yz,
        angle_vars=angle_vars,
        time=t,
        token=str(binascii.b2a_hex(np.random.random(1)))[2:-1]
    )
    filename = "{risk}_{runs}_{l_z}_{nu_x:.3f}_{nu_yz:.3f}_{angle_vars}_{time}_{token}".format(**file_dict)
    filename = filename.replace(".", "").replace(', ', '_').replace('[', '').replace(']', '')
    # print(filename)
    result = risk_type(runs, l_z, nu_x, nu_yz, angle_vars, t)

    np.save(filename, result)


if __name__ == '__main__':

    # input_values = int(sys.argv[1]) + np.array([0, 1000, 2000, 3000])
    # for input_value in input_values:
    #     if input_value < 3179:
    #         [x, y] = np.load('nu_variables_res_3179.npy')[input_value]

    # change the variables, you can loop over nu_x and nu_y
    for x in [1]:
        for y in [0.02]:

            variables = dict(
                runs=5,
                l_z=25,
                nu_x=x,
                nu_yz=y,
                # to loop over various angles, do angle_vars=[ang_zmin, ang_zmax, nu_av], looping over nu_av
                # if angle_vars are defined nu_x, nu_y are ignored (angular fibre simulation)
                angle_vars=False,
                t=10000,
                time_data=False,  # True for AF time sim, False for AF induction probability sim
            )
            gen_risk(**variables)
