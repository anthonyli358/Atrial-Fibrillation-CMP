"""
Model of atrial fibrillation

Andrew Ford
"""
import numpy as np
import scipy.ndimage as spim
import matplotlib.pyplot as plt
import matplotlib.animation as animation

structural_homogenity = 1       # Probability of transverse connections
dysfunctional_parameter = 0     # Fraction of dysfunctional cells
substrate_size = (100, 100)
pacemaker_period = 10  # pacemaker activation period


def activate_pacemaker(substrate):
    # Activate the substrate pacecemaker cells
    substrate[:, 0] = 15


def gen_substrate(substrate_size, structural_homogenity, dysfunction_parameter):
    substrate = np.zeros(substrate_size)
    linkage = np.random.choice(a=[True, False],
                               size=substrate_size,
                               p=[structural_homogenity, 1-structural_homogenity]
                               )
    dysfunction_mask = np.random.choice(a=[True, False],
                                        size=substrate_size,
                                        p=[dysfunction_parameter, 1-dysfunction_parameter]
                                        )
    return substrate, linkage, dysfunction_mask

def iterate(substrate):
    excited = substrate == 15  # Condition for being excited
    resting = substrate == 0  # Condition for resting

    neighbors = [[0, 0, 0],
                 [1, 0, 1],
                 [0, 0, 0]]
    neighbor_excited = spim.convolve(excited, neighbors, mode='constant')
    substrate[np.invert(resting)] -= 1
    substrate[resting & neighbor_excited] = 15

def simulation(runtime, pacemaker_period, substrate):
    result = np.zeros((runtime,)+substrate_size)
    for t in range(runtime):
        if t % pacemaker_period == 0:
            activate_pacemaker(substrate)
        iterate(substrate)
        result[t] = substrate
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

substrate = np.zeros(substrate_size)

results = simulation(runtime=20, pacemaker_period=25, substrate=substrate)

animate_results(results)





