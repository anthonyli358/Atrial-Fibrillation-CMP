import numpy as np


class ECG:
    """
    A class for the ECG analysis of model data.
    """

    def __init__(self, centre, size, heart):
        """
        ECG Initialisation
        :param centre: The centre of the measurement
        :param size: The size of the measurement
        :param activation_array: The array to calculate the ECG value for
        """
        self.heart = heart
        self.centre = centre
        self.size = size

        # measure all cells?

    def voltage(self):
        for cell in self.measured_cells:
            # get voltage
