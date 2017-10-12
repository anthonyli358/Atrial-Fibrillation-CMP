"""
Model of atrial fibrillation

Andrew Ford
"""

import numpy as np


class Substrate:
    """

    """

    def __init__(self, substrate_size, s_structural_homogeneity, p_structural_homogeneity,
                 dysfunction_parameter, dysfunction_probability, refractory_period, seed=False):
        """
        Initialise a heart substrare.

        :param substrate_size:
        :param s_structural_homogeneity:
        :param p_structural_homogeneity:
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
        self.s_structural_heterogeneity = s_structural_homogeneity
        self.p_structural_homogeneity = p_structural_homogeneity
        self.dysfunction_parameter = dysfunction_parameter
        self.dysfunction_probability = dysfunction_probability
        self.refractory_period = np.int8(refractory_period)
        self.activation = np.zeros(substrate_size, dtype='int8')  # Grid of activation state
        self.s_linkage = self.r.choice(a=[True, False], size=substrate_size,  # Grid of downward linkages
                                       p=[s_structural_homogeneity, 1 - s_structural_homogeneity])
        self.p_linkage = self.r.choice(a=[True, False], size=substrate_size,  # Grid of layer linkages
                                       p=[p_structural_homogeneity, 1 - p_structural_homogeneity])
        self.dysfunctional = self.r.choice(a=[True, False], size=substrate_size,  # Grid of dysfunctional nodes
                                           p=[dysfunction_parameter, 1 - dysfunction_parameter])

        self.inactive = np.zeros(substrate_size, dtype=bool)  # Grid of currently dysfunctional nodes

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
        excited_from_rear[:, 0] = np.bool_(False)  # Eliminates wrapping boundary, use numpy bool just in case

        excited_from_fwrd = np.roll(excited, -1, axis=1)
        excited_from_fwrd[:, -1] = np.bool_(False)

        excited_from_inside = np.roll(excited & self.p_linkage, 1, axis=2)
        excited_from_inside[:, :, 0] = np.bool(False)

        excited_from_outside = np.roll(excited & np.roll(self.p_linkage, 1, axis=2), -1, axis=2)
        excited_from_outside[:, :, -1] = np.bool(False)

        excited_from_above = np.roll(excited & self.s_linkage, 1, axis=0)

        excited_from_below = np.roll(excited & np.roll(self.s_linkage, 1, axis=0), -1, axis=0)

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
        return '{},{},{},{},{},{},{}'.format(self.substrate_size, self.s_structural_heterogeneity,
                                             self.dysfunction_parameter,
                                             self.dysfunction_probability, self.refractory_period,
                                             self.p_structural_homogeneity,
                                             self.seed)
