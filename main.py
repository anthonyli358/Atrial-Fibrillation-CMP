import time
import numpy as np
import model as af
import config
import cProfile
import datetime

from model_recorder import ModelRecorder
from viewer import Viewer



from matplotlib import pyplot as plt
import gc


def simulation(substrate, recorder, runtime, pacemaker_period):
    """

    :param runtime: Number of timesteps in simulation.
    :type runtime: int
    :param pacemaker_period: Period of the pacemaker cells
    :type pacemaker_period: int
    :param substrate: Substrate to run simulaton on
    :type substrate: af_model.Substrate
    :return:
    :rtype:
    """

    for t in range(runtime + 1):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()
        # if t  == 5:  # Ectopic beat
        #     substrate.activate((0, 70,100))
        #     substrate.model_array[0, 70, 99] = 49

        recorder.update_model_stat_dict()
        recorder.update_model_array_list()
        substrate.iterate()


def risk_sim(substrate,settings):
    runtime = settings['sim']['runtime']
    refractory_period = settings["structure"]["refractory_period"]
    pacemaker_period = settings['sim']['pacemaker_period']
    sum_result = [[],[]]
    for t in range(runtime + 1):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()
        sub = substrate.iterate()
        sum_result[0].append(np.count_nonzero(sub == refractory_period))
        sum_result[1].append(np.count_nonzero(sub[:,:,-1] == refractory_period))
    return sum_result


def main():
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
    model_viewer.animate_model_array()


# -------------------
# Risc_Recording_Code
# -------------------
# results = []
# runs = 16
# results.append([config.settings['structure']['size'], config.settings['structure']['refractory_period'],
#                 config.settings['structure']['dysfunction_parameter'], config.settings['structure']['dysfunction_probability']
#                 ])
# config.settings['structure']['x_coupling'] = 0.85
# for x_coupling in np.linspace(0.0,0.2,10, endpoint=False):
#     for yz_coupling in np.linspace(0.0, 1, 50, endpoint=False):
#         fracs = []
#         conducting = []
#         config.settings['structure']['x_coupling'] = x_coupling
#         for i in range(runs):
#             config.settings['structure']['y_coupling'] = yz_coupling
#             config.settings['structure']['z_coupling'] = yz_coupling
#             substrate = af.Model(**config.settings["structure"])
#             result,conduction = risk_sim(substrate, config.settings)
#             frac = np.sum(result[220:] > 1.5*np.product(config.settings['structure']['size'][:-1])) / len(result)
#             if np.any(conduction):
#                 conducting.append(True)
#             else:
#                 conducting.append(False)
#             fracs.append(frac)
#             # print('{},\t{}'.format(frac, substrate.seed))
#
#         output = [x_coupling, yz_coupling, np.average(fracs), np.std(fracs), np.average(conducting)]
#         results.append(output)
#         print(output,',')
#         # print('Average = {}\nStandard deviation = {}'.format(np.average(fracs), np.std(fracs)))
# data = np.array(results[1:])
# identifier = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
# save_file = 'data_file_2_200_200-{}.npy'.format(identifier)
# np.save(save_file, data)
#
# # plt.errorbar(data[:,0], data[:,1], yerr=data[:,2]/np.sqrt(runs))
# # plt.show()

if __name__ == '__main__':
    main()
    plt.show()

# TODO: KILLSWITCH()
