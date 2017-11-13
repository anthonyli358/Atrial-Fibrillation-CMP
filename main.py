import time
import numpy as np
import model as af
import config
import cProfile

import viewer
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
    result = np.zeros((runtime,) + substrate.size, dtype='uint8')
    for t in range(runtime):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()
        recorder.update_model_stat_dict()
        recorder.update_model_array_list()
        # if t % (substrate.refractory_period+15) == 0:  # Ectopic beat
        #     substrate.activate((70,100,-1))
        result[t] = substrate.iterate()
    return result


def risksim(substrate,settings):
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

print("RUNNING SIMULATION")

results = simulation(substrate, model_recorder, **config.settings['sim'], )

runtime = time.time() - start
print("SIMULATION COMPLETE IN {:.1f} SECONDS".format(runtime))

model_recorder.output_model_stat_dict()
model_recorder.output_model_array_list()

if config.settings['output']:
    model_recorder.output_model_stats()
    model_recorder.output_model_array_list()

# np.save('rotor_formation(0.18,0.1,0.1)x', results)

# model_viewer = Viewer(model_recorder.path)
# model_viewer.plot_model_stats()

# # Need cross_view?
# d3 = True if substrate.dimensions == 3 else False
#
# print("ANIMATING RESULTS")
# viewer.animate(results, config.settings['structure']['refractory_period'], cross_view=d3, cross_pos=80)  # Cut through

# fracs = []  # Loop to generate risk data
# for i in range(48):
#     # config.settings['structure']['s_homogeneity'] = i
#     substrate = af.Substrate(**config.settings["structure"])
#     result = risksim(substrate, config.settings)
#     frac = np.count_nonzero(result > 220) / len(result)
#     fracs.append(frac)
#     print('{},\t{}'.format(frac, substrate.seed))
#     gc.collect()
# print('Average = {}\nStandard deviation = {}'.format(np.average(fracs), np.std(fracs)))

# TODO: KILLSWITCH()
# ToDo: ECGs
# ToDo: 3D Tuning
