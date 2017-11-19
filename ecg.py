import numpy as np


class ECG:
    """
    A class for the ECG analysis of model data.
    """

    def __init__(self, centre):
        """
        ECG Initialisation
        :param centre: The point of ecg contact on the surface
        :param heart: The heart to be measured
        """
        self.centre = centre  # 0 based

    def voltage(self):
        """Get the ECG voltage for the current time step."""

        # TODO: TAKE IN DATA ARRAY
        voltage_array = np.array([[[1, 2, 3], [2, 3, 4]], [[1, 2, 3], [4, 5, 6]]])[0, :, :].astype(dtype=float) * (
            110 / 50) - 90
        # np.around(voltage_array, decimals=2)

        voltage = 0
        for ((j, i), v) in np.ndenumerate(voltage_array):
            if [j, i] == self.centre:
                pass
            else:
                voltage += ((i - self.centre[1]) * (voltage_array[j, i] - voltage_array[j, i - 1])
                            + (j - self.centre[0]) * (voltage_array[j, i] - voltage_array[j - 1, i])
                            ) / ((i - self.centre[1])**2 + (j - self.centre[0])**2) ** 1.5

        return voltage


ecg = ECG([1, 1])  # [y, x]
print(ecg.voltage())
