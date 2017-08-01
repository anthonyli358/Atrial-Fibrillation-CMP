"""
Model of atrial fibrillation

Andrew Ford
"""
import numpy as np
import scipy.ndimage as spim

structural_homogenity = 1       # Probability of transverse connections
dysfunctional_parameter = 0     # Fraction of dysfunctional cells
substrate_size = (10,10)
pacemaker_period = 10  # pacemaker activation period

class Cell:
    """Heart cell"""

    def __init__(self, coordinates, dysfunctional, transverse_connection, state):
        self.coordinates = coordinates
        self.dysfunctional = dysfunctional
        self.transverse_connections = transverse_connection
        self.state = state



def activate_pacemaker(substrate):
    substrate[:,0] = 15


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
        if t%pacemaker_period == 0:
            activate_pacemaker(substrate)
        iterate(substrate)
        result[t] = substrate
    return result


substrate = np.zeros(substrate_size)

print(simulation(runtime=20, pacemaker_period=16, substrate=substrate))






