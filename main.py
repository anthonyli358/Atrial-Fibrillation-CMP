import time
import af_model as af
import viewer
import numpy as np


def simulation(runtime, pacemaker_period, substrate):
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


s_structural_homogeneity = .1  # Probability of transverse connections
p_structural_homogeneity = .01
dysfunction_parameter = 0  # Fraction of dysfunctional cells
dysfunction_probability = 0
substrate_size = (100, 100, 10)
pacemaker_period = 220  # pacemaker activation period
refractory_period = 50
runtime = 1000
seed = False

start = time.time()
print('GENERATING SUBSTRATE')

substrate = af.Substrate(substrate_size, s_structural_homogeneity, p_structural_homogeneity,
                         dysfunction_parameter, dysfunction_probability, refractory_period, seed)
print(substrate.identifier())

print('RUNNING SIMULATION')

results = simulation(runtime, pacemaker_period, substrate)

runtime = time.time() - start
print('SIMULATION COMPLETE IN {:.1f} SECONDS'.format(runtime))

# np.save('rotor_formation(0.18,0.1,0.1)x', results)


print('ANIMATING RESULTS')
viewer.animate(results, refractory_period, cross_view=True, cross_pos=80)  # Cut through
