import time

import numpy as np
from matplotlib import pyplot as plt

# import analysis
import config
import model as af
import gc
import viewer
import numpy as np
import config
from model_recorder import ModelRecorder


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
    result = np.zeros((runtime,) + substrate.size, dtype=int)
    for t in range(runtime):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()
        result[t] = substrate.iterate()
        recorder.update_model_stats()
        recorder.update_model_array_list()
    return result

def risksim(substrate,settings):
    runtime = settings['sim']['runtime']
    refractory_perid = settings["structure"]["refractory_period"]
    pacemaker_period = settings['sim']['pacemaker_period']
    result = np.zeros(int(runtime))
    for t in range(runtime):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()
        sub = substrate.iterate()
        result[t] =np.count_nonzero(sub == refractory_perid)
    return result

start = time.time()
print("GENERATING SUBSTRATE")

substrate = af.Model(**config.settings['structure'])
model_recorder = ModelRecorder(substrate)

print("RUNNING SIMULATION")

results = simulation(substrate, model_recorder, **config.settings['sim'], )

runtime = time.time() - start
print("SIMULATION COMPLETE IN {:.1f} SECONDS".format(runtime))

model_recorder.output_model_stats()
model_recorder.output_model_array_list()

# np.save('rotor_formation(0.18,0.1,0.1)x', results)

print("ANIMATING RESULTS")
viewer.animate(results, config.settings['structure']['refractory_period'], cross_view=substrate.d3, cross_pos=80)  # Cut through

# TODO: KILLSWITCH()
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

# ToDo: ECGs
# ToDo: 3D Tuning

