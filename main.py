import time
import model as af
import viewer
import numpy as np
import config
np.set_printoptions(threshold=np.nan)

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
    # substrate.create_rotor((100,100))
    for t in range(runtime):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()
        # if t % (substrate.refractory_period+15) == 0:  # Ectopic beat
        #     substrate.activate((70,100,-1))
        result[t] = substrate.iterate()
    return result


start = time.time()
print('GENERATING SUBSTRATE')

substrate = af.Substrate(**config.settings["structure"])
print(substrate.identifier())

print('RUNNING SIMULATION')

results = simulation(substrate, **config.settings["sim"], )

runtime = time.time() - start
print('SIMULATION COMPLETE IN {:.1f} SECONDS'.format(runtime))

# np.save('rotor_formation(0.18,0.1,0.1)x', results)


print('ANIMATING RESULTS')
viewer.animate(results, config.settings)  # Cut through
