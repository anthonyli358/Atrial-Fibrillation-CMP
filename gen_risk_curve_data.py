import config
from model import Model
import numpy as np
import time
import binascii
import sys


def risk_curve_data(runs, l_z, nu_x, nu_yz, angle_vars=False, t=100000):
    """
    Generate risk of inducing AF data.
    :param runs: runs
    :param l_z: layers
    :param nu_x: x (parallel) coupling
    :param nu_yz: yz (perpendicular) coupling
    :param angle_vars: theta(z=0), theta(z=max), magnitude of connectivity
    :param t: timesteps
    :return: data [runs [seed, AF?, x, y, z, time AF/end, conduction block?]]
    """
    data = np.zeros(shape=(runs, 7), dtype='uint32')
    params = config.settings['structure']
    params['size'][0], params['seed'] = l_z, None
    params['x_coupling'], params['yz_coupling'] = nu_x, nu_yz
    params['angle_toggle'], params['angle_vars'] = angle_vars, angle_vars
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
    # print("time={}s".format(time.time() - start))

    return data


def af_time_data(runs, l_z, nu_x, nu_yz, angle_vars=False, t=100000):
    """
    Generate AF time risk data.
    :param runs: runs
    :param l_z: layers
    :param nu_x: x (parallel) coupling
    :param nu_yz: yz (perpendicular) coupling
    :param angle_vars: theta(z=0), theta(z=max), magnitude of connectivity
    :param t: timesteps
    :return: data [runs [seed, AF?, {AF_on, AF_off},etc.]]
    """
    data = []
    params = config.settings['structure']
    params['size'][0], params['seed'] = l_z, None
    params['x_coupling'], params['yz_coupling'] = nu_x, nu_yz
    params['angle_toggle'], params['angle_vars'] = angle_vars, angle_vars
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
    # print("time={}s".format(time.time() - start))

    return data


def con_vel_data(runs, l_z, nu_x, nu_yz, angle_vars=False, t=100000):
    """
    Generate data for conduction velocity.
    :param runs: runs
    :param l_z: number of layers
    :param nu_x: x (parallel) coupling
    :param nu_yz: yz (perpendicular coupling)
    :param angle_vars:
    :param t: timesteps
    :return: data [runs[seed, time, bulk (av, max, min), z=0 (av, max, min), z=24 (av, max, min)]]
    """
    data = np.zeros(shape=(runs, 11), dtype='float32')
    params = config.settings['structure']
    params['dysfunction_parameter'] = 0
    params['size'][0], params['seed'] = l_z, None
    params['x_coupling'], params['yz_coupling'] = nu_x, nu_yz
    params['angle_toggle'], params['angle_vars'] = angle_vars, angle_vars
    start = time.time()
    for i in range(runs):
        tissue = Model(**params)
        data[i, 0] = tissue.seed
        tissue.activate_pacemaker()  # Initialise new wavefront
        while tissue.time < t:
            excitations = tissue.iterate()
            if np.intersect1d(tissue.excount, [2]):
                raise Exception("AF occurred, check that delta is set to 0!")
            # data[i, 1] = True
            #     break
            elif np.any(excitations[:, :, -1]):
                data[i, 1] = tissue.time
                x_pos = np.where(excitations == 50)[2]
                data[i, 2] = np.average(x_pos)
                data[i, 3] = max(x_pos)
                data[i, 4] = min(x_pos)
                if np.any(excitations[0, :, :] == 50):
                    x_pos_0 = np.where(excitations[0, :, :] == 50)[1]
                    data[i, 5] = np.average(x_pos_0)
                    data[i, 6] = max(x_pos_0)
                    data[i, 7] = min(x_pos_0)
                if np.any(excitations[24, :, :] == 50):
                    x_pos_24 = np.where(excitations[24, :, :] == 50)[1]
                    data[i, 8] = np.average(x_pos_24)
                    data[i, 9] = max(x_pos_24)
                    data[i, 10] = min(x_pos_24)
                break
            elif not np.any(excitations == 50):
                data[i, 1] = tissue.time
                x_pos = np.where(excitations == 49)[2]
                data[i, 2] = np.average(x_pos)
                data[i, 3] = max(x_pos)
                data[i, 4] = min(x_pos)
                if np.any(excitations[0, :, :] == 49):
                    x_pos_0 = np.where(excitations[0, :, :] == 49)[1]
                    data[i, 5] = np.average(x_pos_0)
                    data[i, 6] = max(x_pos_0)
                    data[i, 7] = min(x_pos_0)
                if np.any(excitations[24, :, :] == 49):
                    x_pos_24 = np.where(excitations[24, :, :] == 49)[1]
                    data[i, 8] = np.average(x_pos_24)
                    data[i, 9] = max(x_pos_24)
                    data[i, 10] = min(x_pos_24)
                break
        print('Run: {}, Data: {}'.format(i + 1, data[i]))
    print("time={}s".format(time.time() - start))
    return data


def af_pos_data(runs, repeats, l_z, nu_x, nu_yz, angle_vars=False, t=100000):
    """
    Generate position of possible AF source positions for the same structure.
    :param runs: runs - probably look at single runs with lots of repeat to keep same structure.
    :param l_z: layers
    :param nu_x: x (parallel) coupling
    :param nu_yz: yz (perpendicular) coupling
    :param angle_vars: theta(z=0), theta(z=max), magnitude of connectivity
    :param t: timesteps
    :return: data [runs [repeats [seed, dys_seed, AF?, x, y, z]]]
    """
    data = np.zeros(shape=(runs, repeats, 6), dtype='uint32')
    params = config.settings['structure']
    params['dys_seed'] = None  # Randomise dysfunctional cell firing for the same structure
    params['size'][0], params['seed'] = l_z, None
    params['x_coupling'], params['yz_coupling'] = nu_x, nu_yz
    params['angle_toggle'], params['angle_vars'] = angle_vars, angle_vars
    start = time.time()
    for i in range(runs):
        tissue = Model(**params)
        for j in range(repeats):
            tissue.model_array.fill(0)  # Clear activations
            tissue.excount.fill(0)  # Clear excitation count
            tissue.activate_pacemaker()  # Initialise new wavefront
            tissue.time = 0
            data[i, j, 0] = tissue.seed
            data[i, j, 1] = tissue.dys_seed
            while tissue.time < t:
                excitations = tissue.iterate()
                if np.intersect1d(tissue.excount, [2]):
                    data[i, j, 2] = 1
                    data[i, j, 3:6] = tissue.maxpos
                    break
                elif not np.any(excitations == 50):
                    break
            print('Run: {}, Repeat: {}, Data: {}'.format(i + 1, j + 1, data[i, j]))
    print("time={}s".format(time.time() - start))
    return data


def gen_risk(runs, repeats, l_z, nu_x, nu_yz, angle_vars=False, t=100000, func=False):
    """
    Run and np.save risk data to file using selected risk function.
    :param runs: runs
    :param repeats: repeat run with same seed for af_pos_data
    :param l_z: layers
    :param nu_x: x (parallel) coupling
    :param nu_yz: yz (perpendicular) coupling
    :param angle_vars: theta(z=0), theta(z=max), magnitude of connectivity
    :param t: timesteps
    :param func: risk function: risk_curve_data, af_time_data, con_vel_data, or af_pos_data
    :return: np.save data to disk
    """
    if not func:
        raise Exception("Set func='risk_curve_data, af_time_data, con_vel_data, or af_pos_data' to create data!")
    risk_type = func

    file_dict = dict(
        risk=risk_type.__name__,
        runs=runs,
        repeats=repeats,
        l_z=l_z,
        nu_x=nu_x,
        nu_yz=nu_yz,
        angle_vars=angle_vars,
        time=t,
        token=str(binascii.b2a_hex(np.random.random(1)))[2:-1]
    )

    if risk_type == af_pos_data:
        filename = "{risk}_{runs}_{repeats}_{l_z}_{nu_x:.3f}_{nu_yz:.3f}_{angle_vars}_{time}_{token}".format(
            **file_dict)
        result = risk_type(runs, repeats, l_z, nu_x, nu_yz, angle_vars, t)
    else:
        filename = "{risk}_{runs}_{l_z}_{nu_x:.3f}_{nu_yz:.3f}_{angle_vars}_{time}_{token}".format(**file_dict)
        result = risk_type(runs, l_z, nu_x, nu_yz, angle_vars, t)
    filename = filename.replace(".", "").replace(', ', '_').replace('[', '').replace(']', '')
    # print(filename)

    np.save(filename, result)


if __name__ == '__main__':

    # input_values = int(sys.argv[1]) + np.array([0, 1000, 2000, 3000])
    # for input_value in input_values:
    #     if input_value < 3179:
    #         [x, y] = np.load('nu_variables_res_3179.npy')[input_value]

    # change the variables, you can loop over nu_x and nu_y
    for x in [0.9]:
        for y in [0.1]:
            variables = dict(
                runs=2,
                repeats=5,
                l_z=25,
                nu_x=x,
                nu_yz=y,
                # to loop over various angles, do angle_vars=[ang_zmin, ang_zmax, nu_av], looping over nu_av
                # if angle_vars are defined nu_x, nu_y are ignored (angular fibre simulation)
                angle_vars=False,
                t=100000,
                func=af_pos_data,  # risk_curve_data, af_time_data, con_vel_data, or af_pos_data
            )
            gen_risk(**variables)
