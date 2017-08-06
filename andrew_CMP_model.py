"""
Model of atrial fibrillation

Andrew Ford
"""
import numpy as np
import scipy.ndimage as spim
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle


class Substrate:
    def __init__(self, substrate_size, structural_heterogeneity,
                 dysfunction_parameter, dysfunction_probability, refractory_period):
        self.substrate_size = substrate_size
        self.structural_heterogeneity = structural_heterogeneity
        self.dysfunction_parameter = dysfunction_parameter
        self.dysfunction_probability = dysfunction_probability
        self.refractory_period = refractory_period
        self.activation = np.zeros(substrate_size)  # Grid of activation state
        self.linkage = np.random.choice(a=[True, False],  # Grid of downward linkages
                                        size=substrate_size,
                                        p=[structural_heterogeneity, 1 - structural_heterogeneity]
                                        )
        self.dysfunctional = np.random.choice(a=[True, False],  # Grid of dysfunctional nodes
                                              size=substrate_size,
                                              p=[dysfunction_parameter, 1 - dysfunction_parameter]
                                              )
        self.inactive = np.zeros(substrate_size, dtype=bool)  # Grid of currently dysfunctioning nodes

    def activate_pacemaker(self):
        # Activate the substrate pacecemaker cells
        self.activation[:, 0] = int(self.refractory_period)

    def iterate(self):
        excited = self.activation == int(self.refractory_period)  # Condition for being excited
        resting = self.activation == 0  # Condition for resting


        l_neighbors = [[0, 0, 0],
                       [1, 0, 1],
                       [0, 0, 0]]
        v_neighbors = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 1, 0]]
        h_neighbor_excited = spim.convolve(excited, l_neighbors, mode='constant')
        v_neighbor_excited_from_above = spim.convolve(excited & self.linkage,
                                                      v_neighbors,
                                                      mode='wrap'
                                                      )
        v_neighbor_excited_from_below = spim.convolve(excited & np.roll(self.linkage, 1, axis=0),  # shifts link value down
                                                      np.roll(v_neighbors,1, axis=0),  # Changes neighbor from down to up
                                                      mode='wrap'
                                                      )
        self.activation[~resting] -= 1  # If not resting, reduce activation count by one
        excitable = h_neighbor_excited | v_neighbor_excited_from_above | v_neighbor_excited_from_below

        self.inactive[self.dysfunctional & excitable] = np.random.choice(a=[True, False],  # Deactivate dysfunctional nodes
                                                             size=len(self.inactive[self.dysfunctional & excitable]),
                                                             p=[self.dysfunction_probability,
                                                                1 - self.dysfunction_probability]
                                                             )

        self.activation[resting & excitable & ~self.inactive] = self.refractory_period
        return self.activation


def simulation(runtime, pacemaker_period, substrate):
    result = np.zeros((runtime,)+substrate_size)
    for t in range(runtime):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()

        result[t] = substrate.iterate()
    return result


def animate_results(results):
    fig = plt.figure()
    ims = [[plt.imshow(frame, animated=True)] for frame in results]

    ani = animation.ArtistAnimation(fig, ims, interval=5, blit=True,
                                    repeat_delay=500)
    plt.show()


structural_homogeniety = 1     # Probability of transverse connections
dysfunction_parameter = .78    # Fraction of dysfunctional cells
dysfunction_probability = .5
substrate_size = (300, 300)
pacemaker_period = 220  # pacemaker activation period
refractory_period = 50

substrate = Substrate(substrate_size, structural_homogeniety,
                      dysfunction_parameter, dysfunction_probability, refractory_period)

results = simulation(runtime=1000, pacemaker_period=200, substrate=substrate)
print('Done')
animate_results(results)

plt.show()
