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
        np.around(voltage_array, decimals=2)

        voltage = 0
        print(voltage_array.shape)
        for i in range(voltage_array.shape[1]):
            print(i)
            for j in range(voltage_array.shape[0]):
                print(j)
                voltage += ((i - self.centre[0]) * (
                    voltage_array[i, j] - voltage_array[i - 1, j]) + (j - self.centre[j]) * (
                                voltage_array[i, j] - voltage_array[i, j - 1])) / ((i - self.centre[0]
                                                                                    ) ** 2 + (
                                                                                   j - self.centre[1]) ** 2) ** 1.5

        return voltage


ecg = ECG([1, 1])
print(ecg.voltage())
