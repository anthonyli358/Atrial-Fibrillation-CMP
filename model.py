"""
Model of atrial fibrillation

Andrew Ford
"""

import numpy as np


class Substrate:
    """

    """

    def __init__(self, substrate_size, x_structural_homogeneity, y_structural_homogeneity,
                 dysfunction_parameter, dysfunction_probability, refractory_period, seed=False):
        """
        Initialise a heart substrare.

        :param substrate_size:
        :param x_structural_homogeneity:
        :param y_structural_homogeneity:
        :param dysfunction_parameter:
        :param dysfunction_probability:
        :param refractory_period:
        :param seed:
        """
        if not seed:
            seed = np.random.randint(0, 2 ** 32 - 1, dtype='uint32')
        self.seed = seed
        self.r = np.random.RandomState(seed)
        self.substrate_size = substrate_size
        self.x_structural_heterogeneity = x_structural_homogeneity
        self.y_structural_homogeneity = y_structural_homogeneity
        self.dysfunction_parameter = dysfunction_parameter
        self.dysfunction_probability = dysfunction_probability
        self.refractory_period = np.uint8(refractory_period)
        self.activation = np.zeros(substrate_size, dtype='uint8')  # Grid of activation state
        self.x_linkage = self.r.choice(a=[np.True_, np.False_], size=substrate_size,  # Grid of downward linkages
                                       p=[x_structural_homogeneity, 1 - x_structural_homogeneity])
        self.y_linkage = self.r.choice(a=[np.True_, np.False_], size=substrate_size,  # Grid of layer linkages
                                       p=[y_structural_homogeneity, 1 - y_structural_homogeneity])
        self.dysfunctional = self.r.choice(a=[np.True_, np.False_], size=substrate_size,  # Grid of dysfunctional nodes
                                           p=[dysfunction_parameter, 1 - dysfunction_parameter])

        self.inactive = np.zeros(substrate_size, dtype=np.bool_)  # Grid of currently dysfunctional nodes

    def activate_pacemaker(self):
        """
        Activate the substrate pacemaker cells

        :return:
        """
        self.activation[:, 0, :] = self.refractory_period

    def iterate(self):
        """
        Iterate substrate forward one time step and return activation matrix.

        :return:
        """
        excited = self.activation == self.refractory_period  # Condition for being excited
        resting = self.activation == 0  # Condition for resting

        excited_from_rear = np.roll(excited, 1, axis=1)
        excited_from_rear[:, 0] = np.False_  # Eliminates wrapping boundary, use numpy bool just in case

        excited_from_fwrd = np.roll(excited, -1, axis=1)
        excited_from_fwrd[:, -1] = np.False_

        excited_from_inside = np.roll(excited & self.y_linkage, 1, axis=2)
        excited_from_inside[:, :, 0] = np.False_

        excited_from_outside = np.roll(excited & np.roll(self.y_linkage, 1, axis=2), -1, axis=2)
        excited_from_outside[:, :, -1] = np.False_

        excited_from_above = np.roll(excited & self.x_linkage, 1, axis=0)

        excited_from_below = np.roll(excited & np.roll(self.x_linkage, 1, axis=0), -1, axis=0)

        excitable = (excited_from_rear | excited_from_fwrd | excited_from_above |
                     excited_from_below | excited_from_inside | excited_from_outside)

        self.inactive[self.dysfunctional & excitable] = (np.random.random(len(self.inactive[self.dysfunctional
                                                                                            & excitable]))
                                                         < self.dysfunction_probability
                                                         )
        self.activation[~resting] -= 1  # If not resting, reduce activation count by one
        self.activation[resting & excitable & ~self.inactive] = self.refractory_period
        return self.activation

    def identifier(self):
        """
        Return unique identifier for each substrate

        :return:
        """
        return '{},{},{},{},{},{},{}'.format(self.substrate_size, self.x_structural_heterogeneity,
                                             self.dysfunction_parameter,
                                             self.dysfunction_probability, self.refractory_period,
                                             self.y_structural_homogeneity,
                                             self.seed)
    def one_d_create_rotor(self, rotor_coord):
        """
        Create a rotor at the specified coordinate

        :param rotor_coord:
        :type rotor_coord:
        :return:
        :rtype:
        """
        self.x_linkage[rotor_coord[0] - 1:rotor_coord[0] + 1,
        rotor_coord[1]: int(rotor_coord[1] + self.refractory_period / 2 + 1)] = 0
        self.activation[rotor_coord[0], rotor_coord[1] + 3, 0] = self.refractory_period
        self.activation[rotor_coord[0], rotor_coord[1] + 4, 0] = self.refractory_period - 1


    def activate(self, coordinate):
        """
        Activate specified cell
        :param coordinate:
        :type coordinate:
        :return:
        :rtype:
        """
        self.activation[tuple(coordinate)] = self.refractory_period

