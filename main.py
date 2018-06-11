import time
import numpy as np
import model as af
import config
import datetime

from matplotlib import pyplot as plt

from model_recorder import ModelRecorder
from viewer import Viewer


def simulation(substrate, recorder, runtime, pacemaker_period):
    """
     :param substrate: Substrate to run simulaton on
     :type substrate: af_model.Substrate
     :param recorder: Class to record data with update methods
     :type recorder: recorder Class
     :param runtime: Number of timesteps in simulation.
     :type runtime: int
     :param pacemaker_period: Period of the pacemaker cells
     :type pacemaker_period: int
     :return: Array of activation arrays at each timestep
     :rtype: numpy array (runtime, z, y, x)
     """
    result = np.zeros((runtime + 1,) + substrate.size, dtype='uint8')
    for t in range(runtime + 1):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()
        recorder.update_model_stat_dict()
        recorder.update_model_array_list()
        # if t % (substrate.refractory_period+15) == 0:  # Ectopic beat
        #     substrate.activate((70,100,-1))
        result[t] = substrate.iterate()
    return result


def main():
    """
    Run the 3D CMP model, outputting data in HDF5 format using the model_recorder module.
    """
    start = time.time()
    print("GENERATING SUBSTRATE")
    substrate = af.Model(**config.settings['structure'])
    model_recorder = ModelRecorder(substrate)
    print('SEED: {}'.format(substrate.seed))
    print("RUNNING SIMULATION")
    simulation(substrate, model_recorder, **config.settings['sim'], )
    run = time.time() - start
    print("SIMULATION COMPLETE IN {:.1f} SECONDS".format(run))
    model_recorder.output_model_stat_dict()
    model_recorder.output_model_array_list()
    model_viewer = Viewer(model_recorder.path)
    model_viewer.plot_model_stats()
    # data = model_viewer.import_data()
    # model_viewer.animate_model_array(data)


def risk_sim(substrate, settings):
    runtime = settings['sim']['runtime']
    refractory_period = settings["structure"]["refractory_period"]
    pacemaker_period = settings['sim']['pacemaker_period']
    sum_result = [[], []]
    for t in range(runtime + 1):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()
        sub = substrate.iterate()
        sum_result[0].append(np.count_nonzero(sub == refractory_period))
        sum_result[1].append(np.count_nonzero(sub[:, :, -1] == refractory_period))
    return sum_result


def rotor_position():
    positions = []
    for _ in range(1000):
        substrate = af.Model(**config.settings['structure'])
        t = 0
        while substrate.maxpos[2] < 20 and t <= 500:
            if t % 200 == 0:
                substrate.activate_pacemaker()
            substrate.iterate()
            t += 1
        if t < 500:
            positions.append(substrate.maxpos)
            print(_, positions[-1])
        else:
            print(_)
    plt.hist(positions[:][0], 25, (0, 25), True)
    return positions


def risk_recording_code():
    results = []
    runs = 16
    results.append([config.settings['structure']['size'],
                    config.settings['structure']['refractory_period'],
                    config.settings['structure']['dysfunction_parameter'],
                    config.settings['structure']['dysfunction_probability']
                    ])
    config.settings['structure']['x_coupling'] = 0.85
    for x_coupling in np.linspace(0.0, 0.2, 10, endpoint=False):
        for yz_coupling in np.linspace(0.0, 1, 50, endpoint=False):
            fracs = []
            conducting = []
            config.settings['structure']['x_coupling'] = x_coupling
            for i in range(runs):
                config.settings['structure']['y_coupling'] = yz_coupling
                config.settings['structure']['z_coupling'] = yz_coupling
                substrate = af.Model(**config.settings["structure"])
                result, conduction = risk_sim(substrate, config.settings)
                frac = np.sum(result[220:] > 1.5 * np.product(config.settings['structure']['size'][:-1])) / len(result)
                if np.any(conduction):
                    conducting.append(True)
                else:
                    conducting.append(False)
                fracs.append(frac)
                # print('{},\t{}'.format(frac, substrate.seed))

            output = [x_coupling, yz_coupling, np.average(fracs), np.std(fracs), np.average(conducting)]
            results.append(output)
            print(output, ',')
            # print('Average = {}\nStandard deviation = {}'.format(np.average(fracs), np.std(fracs)))
    data = np.array(results[1:])
    identifier = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
    save_file = 'data_file_2_200_200-{}.npy'.format(identifier)
    np.save(save_file, data)

    # plt.errorbar(data[:,0], data[:,1], yerr=data[:,2]/np.sqrt(runs))
    # plt.show()


def risk_pos(x, yz):
    positions = []
    risks = []
    strut_sett = config.settings['structure']
    strut_sett['x_coupling'] = x
    strut_sett['yz_coupling'] = yz

    for _ in range(1000):
        substrate = af.Model(**strut_sett)
        t = 0
        risk = 0
        breakpoint = None
        while t <= 1200:
            if t % 200 == 0:
                substrate.activate_pacemaker()
            substrate.iterate()
            if substrate.maxpos[-1] > 1 and not breakpoint:
                breakpoint = substrate.maxpos
            if substrate.maxpos[-1] > 1 and t > 200:
                risk += 1
            t += 1
        positions.append(breakpoint)
        risks.append(risk)
        print(_, risk, breakpoint)

    return np.array([positions, risks])


def gen_risk_pos():
    for yz in [0.11, 0.12]:
        for x in np.arange(0.8, .85, 0.01):
            name = 'record/' + str(x) + ',' + str(yz) + '.npy'
            print('===========', name)
            result = risk_pos(x, yz)
            np.save(name, result)


if __name__ == '__main__':
    main()

# TODO: KILLSWITCH()
