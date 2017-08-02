"""
Model of atrial fibrillation

Andrew Ford
"""
import numpy as np
import scipy.ndimage as spim
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Substrate:
    def __init__(self, substrate_size, structural_heterogeneity, dysfunction_parameter):
        self.substrate_size = substrate_size
        self.structural_heterogeneity = structural_heterogeneity
        self.dysfunction_parameter = dysfunction_parameter
        self.activation = np.zeros(substrate_size)  # Grid of activation state
        self.linkage = np.random.choice(a=[True, False],  # Grid of downward linkages
                                        size=substrate_size,
                                        p=[structural_heterogeneity, 1 - structural_heterogeneity]
                                        )
        self.dysfunction_mask = np.random.choice(a=[True, False],  # Grid of dysfunctional nodes
                                                 size=substrate_size,
                                                 p=[dysfunction_parameter, 1 - dysfunction_parameter]
                                                 )

    def activate_pacemaker(self):
        # Activate the substrate pacecemaker cells
        self.activation[:, 0] = 15

    def iterate(self):
        excited = self.activation == 15  # Condition for being excited
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
        excitable = h_neighbor_excited|v_neighbor_excited_from_above|v_neighbor_excited_from_below
        self.activation[resting & excitable & ~self.dysfunction_mask] = 15
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
    t = 0

    def updatefig(t):
        im = plt.imshow(results[t], animated=True)
        t += 1
        return im

    ani = animation.FuncAnimation(fig, updatefig, interval=1000)
    plt.show()



structural_homogenity = .18       # Probability of transverse connections
dysfunction_parameter = 0.05     # Fraction of dysfunctional cells
substrate_size = (200, 200)
pacemaker_period = 10  # pacemaker activation period

substrate = Substrate(substrate_size, structural_homogenity, dysfunction_parameter)

results = simulation(runtime=200, pacemaker_period=200, substrate=substrate)
print('Done')
animate_results(results)





