import numpy as np


class Model:
    """
    A class for the cellular automata basis of the CMP model.
    """

    def __init__(self, size, refractory_period, dysfunction_parameter, dysfunction_probability, x_coupling,
                 yz_coupling, seed, time=0, angle_toggle=False, angle_vars=[20, 45, 0.7]):
        """
        Heart Initialisation
        :param size: The dimensions of the heart as a tuple e.g. (200, 200, 10)
        :param refractory_period: Cell refractory period
        :param dysfunction_parameter: The fraction of dysfunctional cells
        :param dysfunction_probability: The fraction of dysfunctional cells which fail to excite
        :param x_coupling: The x yz_coupling factor
        :param yz_coupling: The y yz_coupling factor
        :param seed: Model randomisation seed
        :param time: Current time step
        :param angle_toggle: Toggle the setting of connectivity by angle
        :param angle_vars: List [angle at min(z), angle at max(z), connectivity magnitude]
        """
        self.size = size
        self.refractory_period = refractory_period
        self.dysfunction_parameter = dysfunction_parameter
        self.dysfunction_probability = dysfunction_probability
        self.time = time
        self.seed = seed if seed is not None else np.random.randint(np.iinfo('uint32').max, dtype='uint32')
        np.random.seed(self.seed)
        self.direction = np.zeros(size, dtype='uint8')

        self.excited = np.zeros(size, dtype=bool)
        self.resting = np.ones(size, dtype=bool)
        self.excount = np.zeros(size, dtype='uint32')
        self._max = 0
        self.maxpos = [0, 0, 0]
        self.model_array = np.zeros(size, dtype='uint8')  # array of model_array state

        if angle_toggle:
            angle0 = angle_vars[0]
            angle1 = angle_vars[1]
            connectivity = 2 * angle_vars[2]

            angle_grid = np.linspace(angle0, angle1, size[0]) * np.pi / 180
            tangent = np.tan(angle_grid)
            x_coupling_grid = connectivity / (1 + tangent)
            yz_coupling_grid = x_coupling_grid * tangent
            print(x_coupling_grid, yz_coupling_grid)
            x_ran = np.random.random(size)
            y_ran = np.random.random(size)
            z_ran = np.random.random(size)

            self.x_linkage = np.apply_along_axis(np.less, 0, x_ran, x_coupling_grid)
            self.y_linkage = np.apply_along_axis(np.less, 0, y_ran, yz_coupling_grid)
            self.z_linkage = np.apply_along_axis(np.less, 0, z_ran, yz_coupling_grid)

        else:
            self.x_linkage = np.random.choice(a=[True, False], size=size,  # array of longitudinal linkages
                                              p=[x_coupling, 1 - x_coupling])
            self.y_linkage = np.random.choice(a=[True, False], size=size,  # array of transverse linkages
                                              p=[yz_coupling, 1 - yz_coupling])
            self.z_linkage = np.random.choice(a=[True, False], size=size,  # array of layer linkages
                                              p=[yz_coupling, 1 - yz_coupling])

        self.x_linkage[:, :, -1] = False  # No links from end
        self.z_linkage[-1, :, :] = False
        self.dysfunctional = np.random.choice(a=[True, False], size=size,  # array of dysfunctional nodes
                                              p=[dysfunction_parameter, 1 - dysfunction_parameter])
        self.failed = np.zeros(size, dtype=bool)  # array of currently dysfunctional nodes
        self.destroyed = np.zeros(size, dtype=bool)

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

        excited_from_pos_z = np.roll(self.excited & self.z_linkage, 1, axis=0)

        excited_from_neg_z = np.roll(self.excited & np.roll(self.z_linkage, 1, axis=0), -1, axis=0)

        excited_from_neg_y = np.roll(self.excited & self.y_linkage, 1, axis=1)

        excited_from_pos_y = np.roll(self.excited & np.roll(self.y_linkage, 1, axis=1), -1, axis=1)

        excited_from_neg_x = np.roll(self.excited & self.x_linkage, 1, axis=2)

        excited_from_pos_x = np.roll(self.excited & np.roll(self.x_linkage, 1, axis=2), -1, axis=2)

        # Create array of excitable cells

        excitable = (excited_from_neg_y | excited_from_pos_y | excited_from_neg_x |
                     excited_from_pos_x | excited_from_pos_z | excited_from_neg_z) & self.resting & ~ self.destroyed

        self.direction[excitable] = (1 * excited_from_neg_y.astype('int8') +
                                     2 * excited_from_pos_y.astype('int8') +
                                     4 * excited_from_neg_x.astype('int8') +
                                     8 * excited_from_pos_x.astype('int8') +
                                     16 * excited_from_pos_z.astype('int8') +
                                     32 * excited_from_neg_z.astype('int8')
                                     )[excitable]

        # Check if dysfunctional cells fail to excite
        self.failed[excitable & self.dysfunctional] = np.random.random(
            len(self.failed[excitable & self.dysfunctional])) < self.dysfunction_probability

        # Time +1: Reduce excitation and excite resting and excitable (not failed) cells.
        self.model_array[~self.resting] -= 1
        self.model_array[excitable & ~self.failed] = self.refractory_period
        self.time += 1

        # Update excited and resting arrays
        self.excited = self.model_array == self.refractory_period
        self.resting = self.model_array == 0
        self.excount += np.uint32(self.excited)

        itermax = np.max(self.excount)
        if itermax != self._max:  # When a new level of excitation happens find position of excitation
            self._max = itermax
            self.maxpos = np.unravel_index(np.argmax(self.excount), self.size)

        return self.model_array

    def add_ablation(self, coordinate, radius):
        """
        Destroy tissue within radius(mm) of coordinates.
        """
        z = range(self.size[0])
        y = range(self.size[1])
        x = range(self.size[2])
        Z, Y, X = np.meshgrid(z, y, x, indexing='ij')
        Xp, Yp, Zp = X - coordinate[2], Y - coordinate[1], Z
        dist_sq = np.square(Xp * 0.5) + np.square(Yp * 0.1) + np.square(Zp * 0.1)
        self.destroyed = dist_sq < radius ** 2

    def activate(self, coordinate):
        """
        Activate specified cell.
        :param coordinate: Coordinate of cell to activate
        """
        self.model_array[tuple(coordinate)] = self.refractory_period

    def one_d_create_circuit(self, circuit_coord):
        """
        Create a circuit at the specified coordinate.
        :param circuit_coord: First activated cell (starting point) of the circuit
        """
        self.y_linkage[0, circuit_coord[0] - 1:circuit_coord[0] + 1,
        circuit_coord[1]: int(circuit_coord[1] + self.refractory_period / 2 + 1)] = 0
        self.model_array[0, circuit_coord[0], circuit_coord[1] + 3] = self.refractory_period
        self.model_array[0, circuit_coord[0], circuit_coord[1] + 4] = self.refractory_period - 1
