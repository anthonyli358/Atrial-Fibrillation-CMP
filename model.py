import numpy as np


class Model:
    """
    A class for the cellular automata basis of the CMP model.
    """

    def __init__(self, size, s_structural_homogeneity, p_structural_homogeneity,
                 dysfunction_parameter, dysfunction_probability, refractory_period, seed=False):
        """
        Heart Initialisation
        :param size: The dimensions of the heart as a tuple e.g. (200, 200, 10)
        :param s_structural_homogeneity: The perpendicular coupling factor
        :param p_structural_homogeneity: The parallel coupling factor
        :param dysfunction_parameter: The fraction of dysfunctional cells
        :param dysfunction_probability: The fraction of dysfunctional cells which fail to excite
        :param refractory_period: Cell refactory period
        :param seed: Model randomisation seed
        """
        if not seed:
            seed = np.random.randint(0, 2 ** 32 - 1, dtype=int)
        self.seed = seed
        self.r = np.random.RandomState(seed)
        self.size = size
        self.s_structural_heterogeneity = s_structural_homogeneity
        self.p_structural_homogeneity = p_structural_homogeneity
        self.dysfunction_parameter = dysfunction_parameter
        self.dysfunction_probability = dysfunction_probability
        self.refractory_period = refractory_period
        self.activation = np.zeros(size, dtype=int)  # Grid of activation state
        self.s_linkage = self.r.choice(a=[True, False], size=size,  # Grid of downward linkages
                                       p=[s_structural_homogeneity, 1 - s_structural_homogeneity])
        self.p_linkage = self.r.choice(a=[True, False], size=size,  # Grid of layer linkages
                                       p=[p_structural_homogeneity, 1 - p_structural_homogeneity])
        self.dysfunctional = self.r.choice(a=[True, False], size=size,  # Grid of dysfunctional nodes
                                           p=[dysfunction_parameter, 1 - dysfunction_parameter])

        self.inactive = np.zeros(size, dtype=bool)  # Grid of currently dysfunctional nodes

    def activate_pacemaker(self):
        """
        Activate the pacemaker cells at the sinoatrial node (very left of the model).
        """
        self.activation[:, 0, :] = self.refractory_period

    def iterate(self):
        """
        Iterate model forward one time step.
        :return: Activation Array
        """
        excited = self.activation == self.refractory_period  # Condition for being excited
        resting = self.activation == 0  # Condition for resting

        # Roll excited values to get arrays of possible excitations
        excited_from_above = np.roll(excited & self.s_linkage, 1, axis=0)

        excited_from_below = np.roll(excited & np.roll(self.s_linkage, 1, axis=0), -1, axis=0)

        excited_from_rear = np.roll(excited, 1, axis=1)
        excited_from_rear[:, 0] = np.bool_(False)  # Eliminates wrapping boundary, use numpy bool just in case

        excited_from_fwrd = np.roll(excited, -1, axis=1)
        excited_from_fwrd[:, -1] = np.bool_(False)

        # 3d model
        excited_from_inside = np.roll(excited & self.p_linkage, 1, axis=2)
        excited_from_inside[:, :, 0] = np.bool(False)

        excited_from_outside = np.roll(excited & np.roll(self.p_linkage, 1, axis=2), -1, axis=2)
        excited_from_outside[:, :, -1] = np.bool(False)

        # Create array of excitable cells
        excitable = (excited_from_above | excited_from_below | excited_from_rear |
                     excited_from_fwrd | excited_from_inside | excited_from_outside)

        # Check if dysfunctional cells fail to excite
        self.inactive[self.dysfunctional & excitable] = (np.random.random(len(self.inactive[self.dysfunctional
                                                                                            & excitable]))
                                                         < self.dysfunction_probability)

        # Time +1: Reduce excitation and excite resting and excitable (not inactive) cells.
        self.activation[~resting] -= 1
        self.activation[resting & excitable & ~self.inactive] = self.refractory_period

        return self.activation

    def identifier(self):
        """
        Identifier for each substrate.
        :return: Substrate parameters and seed as a string
        """
        return '{},{},{},{},{},{},{}'.format(self.size,
                                             self.s_structural_heterogeneity,
                                             self.dysfunction_parameter,
                                             self.dysfunction_probability,
                                             self.refractory_period,
                                             self.p_structural_homogeneity,
                                             self.seed)

# ToDo: 2d and 3d running options
# ToDo: RENAME VARIABLES
# ToDo: OPTIMISE
# ToDo: UNIT TESTS
