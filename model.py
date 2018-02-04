import datetime
import numpy as np

from re import sub


class Model:
    """
    A class for the cellular automata basis of the CMP model.
    """

    def __init__(self, size, refractory_period, dysfunction_parameter, dysfunction_probability, x_coupling,
                 y_coupling, z_coupling, seed, time=0):
        """
        Heart Initialisation
        :param size: The dimensions of the heart as a tuple e.g. (200, 200, 10)
        :param x_coupling: The x coupling factor
        :param y_coupling: The y coupling factor
        :param z_coupling: The z coupling factor
        :param dysfunction_parameter: The fraction of dysfunctional cells
        :param dysfunction_probability: The fraction of dysfunctional cells which fail to excite
        :param refractory_period: Cell refractory period
        :param time: Current time step
        :param seed: Model randomisation seed
        """
        self.size = size
        self.refractory_period = refractory_period
        self.dysfunction_parameter = dysfunction_parameter
        self.dysfunction_probability = dysfunction_probability
        self.time = time
        self.seed = seed if seed is not None else datetime.datetime.now().strftime('%m-%d_%H-%M-%S')
        np.random.seed(int(sub('[^0-9]', '', self.seed)))

        self.excited = np.zeros(size, dtype=bool)
        self.resting = np.ones(size, dtype=bool)
        self.model_array = np.zeros(size, dtype='uint8')  # array of model_array state
        self.x_linkage = np.random.choice(a=[True, False], size=size,  # array of longitudinal linkages
                                          p=[x_coupling, 1 - x_coupling])
        self.y_linkage = np.random.choice(a=[True, False], size=size,  # array of transverse linkages
                                          p=[y_coupling, 1 - y_coupling])
        self.z_linkage = np.random.choice(a=[True, False], size=size,  # array of layer linkages
                                          p=[z_coupling, 1 - z_coupling])
        self.dysfunctional = np.random.choice(a=[True, False], size=size,  # array of dysfunctional nodes
                                              p=[dysfunction_parameter, 1 - dysfunction_parameter])
        self.failed = np.zeros(size, dtype=bool)  # array of currently dysfunctional nodes

    def activate_pacemaker(self):
        """
        Activate the pacemaker cells at the sinoatrial node (very left of the model).
        """
        self.model_array[:, :, 0] = self.refractory_period

        # Update excited and resting arrays
        self.excited = self.model_array == self.refractory_period  # condition for being excited
        self.resting = self.model_array == 0  # condition for resting

    def iterate(self):
        """
        Iterate model forward one time step.
        :return: Activation Array
        """
        self.failed = np.zeros(self.size, dtype=bool)

        # Roll excited values to get arrays of possible excitations
        excited_from_above = np.roll(self.excited & self.y_linkage, 1, axis=1)
        excited_from_below = np.roll(self.excited & np.roll(self.y_linkage, 1, axis=0), -1, axis=1)

        excited_from_rear = np.roll(self.excited & self.x_linkage, 1, axis=2)
        excited_from_rear[:, :, 0] = np.bool_(False)  # eliminates wrapping boundary, use numpy bool just in case

        excited_from_fwrd = np.roll(self.excited & np.roll(self.x_linkage, 1, axis=0), -1, axis=2)
        excited_from_fwrd[:, :, -1] = np.bool_(False)

        excited_from_inside = np.roll(self.excited & self.z_linkage, 1, axis=0)
        excited_from_inside[0, :, :] = np.bool(False)

        excited_from_outside = np.roll(self.excited & np.roll(self.z_linkage, 1, axis=2), -1, axis=0)
        excited_from_outside[-1, :, :] = np.bool(False)

        # Create array of excitable cells
        excitable = (excited_from_above | excited_from_below | excited_from_rear |
                     excited_from_fwrd | excited_from_inside | excited_from_outside) & self.resting

        # Check if dysfunctional cells fail to excite
        self.failed[excitable & self.dysfunctional] = np.random.random(len(self.failed[excitable & self.dysfunctional]
                                                                           )) < self.dysfunction_probability

        # Time +1: Reduce excitation and excite resting and excitable (not failed) cells.
        self.model_array[~self.resting] -= 1
        self.model_array[excitable & ~self.failed] = self.refractory_period
        self.time += 1

        # Update excited and resting arrays
        self.excited = self.model_array == self.refractory_period
        self.resting = self.model_array == 0

        return self.model_array
    
    def activate(self, coordinate):
        """
        Activate specified cell
        :param coordinate:
        :type coordinate:
        :return:
        :rtype:
        """
        self.model_array[tuple(coordinate)] = self.refractory_period

    def one_d_create_rotor(self, rotor_coord):
        """
        Create a rotor at the specified coordinate

        :param rotor_coord:
        :type rotor_coord:
        :return:
        :rtype:
        """
        self.y_linkage[0, rotor_coord[0] - 1:rotor_coord[0] + 1,
                       rotor_coord[1]: int(rotor_coord[1] + self.refractory_period / 2 + 1)] = 0
        self.model_array[0, rotor_coord[0], rotor_coord[1] + 3] = self.refractory_period
        self.model_array[0, rotor_coord[0], rotor_coord[1] + 4] = self.refractory_period - 1

# TODO: MAIN
# ToDo: OPTIMISE
# TODO: COMMENT AND ORGANISE ALL MODULES
# ToDo: UNIT TESTS
# TODO: UPDATE README WITH HOW TO USE
