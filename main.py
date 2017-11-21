import time
import numpy as np
import model as af
import config
import cProfile

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


def risk_sim(substrate,settings):
    runtime = settings['sim']['runtime']
    refractory_period = settings["structure"]["refractory_period"]
    pacemaker_period = settings['sim']['pacemaker_period']
    result = np.zeros(int(runtime + 1))
    for t in range(runtime + 1):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()
        sub = substrate.iterate()
        result[t] = np.count_nonzero(sub == refractory_period)
    return result


start = time.time()
print("GENERATING SUBSTRATE")

substrate = af.Model(**config.settings['structure'])
model_recorder = ModelRecorder(substrate)
print('SEED: {}'.format(substrate.seed))

print("RUNNING SIMULATION")

results = simulation(substrate, model_recorder, **config.settings['sim'], )

runtime = time.time() - start
print("SIMULATION COMPLETE IN {:.1f} SECONDS".format(runtime))

model_recorder.output_model_stat_dict()
model_recorder.output_model_array_list()

# np.save('rotor_formation(0.18,0.1,0.1)x', results)

model_viewer = Viewer(model_recorder.path)
model_viewer.plot_model_stats()
model_viewer.animate_model_array(cross_view=True, cross_pos=80)


# print("ANIMATING RESULTS")
# Viewer.animate(results, config.settings['structure']['refractory_period'], cross_view=True, cross_pos=80)  # Cut through

# -------------------
# Risc_Recording_Code
# -------------------
# results = []
# runs = 24
# results.append([config.settings['structure']['size'], config.settings['structure']['refractory_period'],
#                 config.settings['structure']['dysfunction_parameter'], config.settings['structure']['dysfunction_probability']
#                 ])
# config.settings['structure']['x_coupling'] = 0.85
# for coupling in np.linspace(0.0,.14,29):
#     fracs = []
#     for i in range(runs):
#         config.settings['structure']['y_coupling'] = coupling
#         config.settings['structure']['z_coupling'] = coupling
#         substrate = af.Model(**config.settings["structure"])
#         result = risksim(substrate, config.settings)[220:]
#         frac = np.count_nonzero(result > 1100) / len(result)
#         fracs.append(frac)
#         # print('{},\t{}'.format(frac, substrate.seed))
#         output = [coupling,np.average(fracs),np.std(fracs)]
#     results.append(output)
#     print(output)
#     # print('Average = {}\nStandard deviation = {}'.format(np.average(fracs), np.std(fracs)))
# data = np.array(results[1:])
# np.save('{}_test1000t{}nu'.format(runs, config.settings['structure']['x_coupling']), data)
# plt.errorbar(data[:,0], data[:,1], yerr=data[:,2]/np.sqrt(runs))
# plt.show()


# TODO: KILLSWITCH()
