import time
import af_model as af
import viewer
import numpy as np
import config


def simulation(substrate, runtime, pacemaker_period):
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
    result = np.zeros((runtime,) + substrate.substrate_size, dtype='int8')
    for t in range(runtime):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()
        result[t] = substrate.iterate()
    return result


start = time.time()
print('GENERATING SUBSTRATE')

substrate = af.Substrate(**config.settings["structure"])
print(substrate.identifier())

print('RUNNING SIMULATION')

results = simulation(substrate, **config.settings["sim"])

runtime = time.time() - start
print('SIMULATION COMPLETE IN {:.1f} SECONDS'.format(runtime))

# np.save('rotor_formation(0.18,0.1,0.1)x', results)


print('ANIMATING RESULTS')
viewer.animate(results, config.settings["structure"]["refractory_period"], cross_view=True, cross_pos=80)  # Cut through
