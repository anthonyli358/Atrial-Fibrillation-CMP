import datetime
import numpy as np


class Model:
    """
    A class for the cellular automata basis of the CMP model.
    """

    def __init__(self, size, y_coupling, dysfunction_parameter, dysfunction_probability, refractory_period,
                 d3=False, z_coupling=0, time=0, seed=False):
        """
        Heart Initialisation
        :param size: The dimensions of the heart as a tuple e.g. (200, 200, 10)
        :param y_coupling: The y coupling factor
        :param z_coupling: The z coupling factor
        :param dysfunction_parameter: The fraction of dysfunctional cells
        :param dysfunction_probability: The fraction of dysfunctional cells which fail to excite
        :param refractory_period: Cell refractory period
        :param d3: Set to True to enable 3d modelling
        :param time: Current time step
        :param seed: Model randomisation seed
        """
        self.size = size
        self.dysfunction_parameter = dysfunction_parameter
        self.dysfunction_probability = dysfunction_probability
        self.refractory_period = refractory_period
        self.time = time
        self.seed = seed if seed is not None else datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        np.random.seed(self.seed)

        self.excited, self.resting, self.failed = (0 for _ in range(3))
        self.model_array = np.zeros(size, dtype='int16')  # Grid of model_array state
        self.y_linkage = np.random.choice(a=[True, False], size=size,  # Grid of downward linkages
                                          p=[y_coupling, 1 - y_coupling])
        self.dysfunctional = np.random.choice(a=[True, False], size=size,  # Grid of dysfunctional nodes
                                              p=[dysfunction_parameter, 1 - dysfunction_parameter])
        self.inactive = np.zeros(size, dtype=bool)  # Grid of currently dysfunctional nodes

        self.d3 = d3
        if d3:
            self.z_linkage = np.random.choice(a=[True, False], size=size,  # Grid of layer linkages
                                              p=[z_coupling, 1 - z_coupling])

    def activate_pacemaker(self):
        """
        Activate the pacemaker cells at the sinoatrial node (very left of the model).
        """

        if self.d3:
            self.model_array[:, 0, :] = self.refractory_period
        else:
            self.model_array[:, 0] = self.refractory_period

    def iterate(self):
        """
        Iterate model forward one time step.
        :return: Activation Array
        """
        self.excited = self.model_array == self.refractory_period  # Condition for being excited
        self.resting = self.model_array == 0  # Condition for resting

        # Roll excited values to get arrays of possible excitations
        excited_from_above = np.roll(self.excited & self.y_linkage, 1, axis=0)

        excited_from_below = np.roll(self.excited & np.roll(self.y_linkage, 1, axis=0), -1, axis=0)

        excited_from_rear = np.roll(self.excited, 1, axis=1)
        excited_from_rear[:, 0] = np.bool_(False)  # Eliminates wrapping boundary, use numpy bool just in case

        excited_from_fwrd = np.roll(self.excited, -1, axis=1)
        excited_from_fwrd[:, -1] = np.bool_(False)

        # 3d model
        if self.d3:
            excited_from_inside = np.roll(self.excited & self.z_linkage, 1, axis=2)
            excited_from_inside[:, :, 0] = np.bool(False)

            excited_from_outside = np.roll(self.excited & np.roll(self.z_linkage, 1, axis=2), -1, axis=2)
            excited_from_outside[:, :, -1] = np.bool(False)

            # Create array of excitable cells
            excitable = (excited_from_above | excited_from_below | excited_from_rear |
                         excited_from_fwrd | excited_from_inside | excited_from_outside)

        else:
            excitable = (excited_from_above | excited_from_below | excited_from_rear | excited_from_fwrd)

        # Check if dysfunctional cells fail to excite
        self.inactive[self.dysfunctional & excitable] = (np.random.random(len(self.inactive[self.dysfunctional
                                                                                            & excitable]))
                                                         < self.dysfunction_probability)

        # Time +1: Reduce excitation and excite resting and excitable (not inactive) cells.
        self.model_array[~self.resting] -= 1
        self.model_array[self.resting & excitable & ~self.inactive] = self.refractory_period
        self.time += 1

        return self.model_array

# ToDo: Data Output
# ToDo: Other Modules
# ToDo: OPTIMISE
# ToDo: UNIT TESTS
