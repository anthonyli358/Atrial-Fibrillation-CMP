"""
Model of atrial fibrillation

Andrew Ford
"""
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


class Substrate:
    def __init__(self, substrate_size, structural_homogeneity,
                 dysfunction_parameter, dysfunction_probability, refractory_period, layer_linkage):
        self.substrate_size = substrate_size
        self.structural_heterogeneity = structural_homogeneity
        self.dysfunction_parameter = dysfunction_parameter
        self.dysfunction_probability = dysfunction_probability
        self.refractory_period = np.int8(refractory_period)
        self.activation = np.zeros(substrate_size, dtype='int8')  # Grid of activation state
        self.linkage = np.random.choice(a=[True, False], size=substrate_size,  # Grid of downward linkages
                                        p=[structural_homogeneity, 1 - structural_homogeneity])
        self.layer_linkage = np.random.choice(a=[True, False], size=substrate_size,  # Grid of layer linkages
                                        p=[layer_linkage, 1 - layer_linkage])
        self.dysfunctional = np.random.choice(a=[True, False], size=substrate_size,  # Grid of dysfunctional nodes
                                              p=[dysfunction_parameter, 1 - dysfunction_parameter])

        self.inactive = np.zeros(substrate_size, dtype=bool)  # Grid of currently dysfunctional nodes

    def activate_pacemaker(self):
        # Activate the substrate pacemaker cells
        self.activation[:, 0,:] = self.refractory_period

    def iterate(self):
        excited = self.activation == self.refractory_period  # Condition for being excited
        resting = self.activation == 0  # Condition for resting

        excited_from_rear = np.roll(excited, 1, axis=1)
        excited_from_rear[:,0] = np.bool_(False)  # Eliminates wrapping boundary, use numpy bool just in case

        excited_from_fwrd = np.roll(excited, -1, axis=1)
        excited_from_fwrd[:, -1] = np.bool_(False)

        excited_from_inside = np.roll(excited & self.layer_linkage, 1, axis=2)
        excited_from_inside[:,:,0] = np.bool(False)

        excited_from_outside = np.roll(excited & np.roll(self.layer_linkage, 1, axis=2), -1, axis=2)
        excited_from_outside[:,:,-1] = np.bool(False)

        excited_from_above = np.roll(excited & self.linkage, 1, axis=0)

        excited_from_below = np.roll(excited & np.roll(self.linkage, 1, axis=0), -1, axis=0)

        excitable = (excited_from_rear | excited_from_fwrd | excited_from_above |
                     excited_from_below | excited_from_inside | excited_from_outside)

        self.inactive[self.dysfunctional & excitable] = (np.random.random(len(self.inactive[self.dysfunctional
                                                                                            & excitable]))
                                                         < self.dysfunction_probability
                                                         )
        self.activation[~resting] -= 1  # If not resting, reduce activation count by one
        self.activation[resting & excitable & ~self.inactive] = self.refractory_period
        return self.activation


def simulation(runtime, pacemaker_period, substrate):
    result = np.zeros((runtime,) + substrate.substrate_size, dtype='int8')
    for t in range(runtime):
        if t % pacemaker_period == 0:
            substrate.activate_pacemaker()

        result[t] = substrate.iterate()
    return result


def animate(results, save=False):
    fig = plt.figure()
    ims = [[plt.imshow(frame, animated=True)] for frame in results]

    ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,
                                    repeat_delay=500)
    if save:
        plt.rcParams['animation.ffmpeg_path'] = "C:/Program Files/ffmpeg-20170807-1bef008-win64-static/bin/ffmpeg.exe"

        writer = animation.writers['ffmpeg'](fps=30)
        print('SAVING')
        t = time.time()
        ani.save(save, writer)
        print('Saved as {} in {:.1f} seconds'.format(save, time.time()-t))
    plt.show()



