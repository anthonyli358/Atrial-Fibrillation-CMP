"""
Model of atrial fibrillation

Andrew Ford
"""
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import convolve


class Substrate:
    def __init__(self, substrate_size, structural_homogeneity,
                 dysfunction_parameter, dysfunction_probability, refractory_period):
        self.substrate_size = substrate_size
        self.structural_heterogeneity = structural_homogeneity
        self.dysfunction_parameter = dysfunction_parameter
        self.dysfunction_probability = dysfunction_probability
        self.refractory_period = np.int8(refractory_period)
        self.activation = np.zeros(substrate_size, dtype='int8')  # Grid of activation state
        self.linkage = np.random.choice(a=[True, False], size=substrate_size,  # Grid of downward linkages
                                        p=[structural_homogeneity, 1 - structural_homogeneity])
        self.dysfunctional = np.random.choice(a=[True, False], size=substrate_size,  # Grid of dysfunctional nodes
                                              p=[dysfunction_parameter, 1 - dysfunction_parameter])

        self.inactive = np.zeros(substrate_size, dtype=bool)  # Grid of currently dysfunctional nodes

    def activate_pacemaker(self):
        # Activate the substrate pacemaker cells
        self.activation[:, 0] = self.refractory_period

    def iterate(self):
        excited = self.activation == self.refractory_period  # Condition for being excited
        resting = self.activation == 0  # Condition for resting

        h_neighbors = [[0, 0, 0],
                       [1, 0, 1],
                       [0, 0, 0]]
        v_neighbord = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 1, 0]]
        v_neighboru = [[0, 1, 0],
                       [0, 0, 0],
                       [0, 0, 0]]
        h_neighbor_excited = convolve(excited, h_neighbors, mode='constant')
        v_neighbor_excited_from_above = convolve(excited & self.linkage, v_neighbord, mode='wrap')
        v_neighbor_excited_from_below = convolve(excited & np.roll(self.linkage, 1, axis=0),  # shifts link value down
                                                 v_neighboru, mode='wrap')

        excitable = h_neighbor_excited | v_neighbor_excited_from_above | v_neighbor_excited_from_below

        self.inactive[self.dysfunctional & excitable] = (np.random.random(len(self.inactive[self.dysfunctional
                                                                                            & excitable]))
                                                         < self.dysfunction_probability
                                                         )
        self.activation[~resting] -= 1  # If not resting, reduce activation count by one
        self.activation[resting & excitable & ~self.inactive] = self.refractory_period
        return self.activation


def simulation(runtime, pacemaker_period, substrate):
    result = np.zeros((runtime,) + substrate_size, dtype='int8')
    for t in range(runtime):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()

        result[t] = substrate.iterate()
    return result


def animate(results):
    fig = plt.figure()
    ims = [[plt.imshow(frame, animated=True)] for frame in results]

    ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,
                                    repeat_delay=500)
    plt.show()


structural_homogeneity = .18  # Probability of transverse connections
dysfunction_parameter = .05  # Fraction of dysfunctional cells
dysfunction_probability = .05
substrate_size = (300, 300)
pacemaker_period = 220  # pacemaker activation period
refractory_period = 50
runtime = 1000

start = time.time()
print('GENERATING SUBSTRATE')

substrate = Substrate(substrate_size, structural_homogeneity,
                      dysfunction_parameter, dysfunction_probability, refractory_period)

print('RUNNING SIMULATION')

results = simulation(runtime, pacemaker_period, substrate)

runtime = time.time() - start
print('SIMULATION COMPLETE IN {:.1f} SECONDS'.format(runtime))

print('ANIMATING RESULTS')
animate(results)
