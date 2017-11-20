import h5py
import numpy as np
import seaborn as sns
import sys
from matplotlib import pyplot as plt

from utility_methods import *


class ECG:
    """
    A class for the ECG analysis of model data.
    """

    def __init__(self, centre, path):
        """
        ECG Initialisation
        :param centre: The point of ecg contact on the surface
        :param path: The path for data to read and view
        """
        self.centre = centre  # 0 based
        self.path = path

        # Import the model_array from HFD5 format
        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
            self.model_array_list = model_data_file['array_list'][:]
        self.refractory_period = max(self.model_array_list.flatten())

        create_dir('{}/ecg'.format(self.path))

    def voltage(self, time):
        """
        Get the ECG voltage for the current time step.
        :param time: Current time step
        """

        # TODO: SELECT SURFACE (3D)
        voltage_array = self.model_array_list[time][0, :, :].astype(dtype=float) * (110 / self.refractory_period) - 90
        voltage = 0

        for ((j, i), v) in np.ndenumerate(voltage_array):
            if [j, i] == self.centre:
                pass
            else:
                voltage += ((i - self.centre[1]) * (voltage_array[j, i] - voltage_array[j, i - 1])
                            + (j - self.centre[0]) * (voltage_array[j, i] - voltage_array[j - 1, i])
                            ) / ((i - self.centre[1])**2 + (j - self.centre[0])**2) ** 1.5

        return voltage

    def ecg(self, time_steps=None, start=0):
        """
        Return list of ECG voltages for a time period.
        :param time_steps: Number of time steps to calculate ECG for
        :param start: Start time
        """
        total_time = len(self.model_array_list)
        voltage_list = np.zeros(total_time)
        if time_steps is None or time_steps > total_time:
            time_steps = total_time - start

        for i in range(time_steps):
            sys.stdout.write(
                '\r' + "calculating ecg, time_step: {}/{}...".format(start + i, total_time - 1))
            sys.stdout.flush()
            voltage_list[i] = self.voltage(i)

        return voltage_list

    def plot_ecg(self, x, y, label):
        """Plot the ECG."""

        plt.figure()
        sns.set_style('ticks')
        plt.plot(x, y, label="{}".format(label))
        plt.xlabel("Time")
        plt.ylabel("Voltage (V)")
        plt.title("ECG")
        plt.legend(loc=0, fontsize=12, frameon=True)
        plt.savefig('data/{}/ecg/ecg.png'.format(self.path))
        plt.close()


e = ECG([1, 1], '11-20_20-09-43')  # [y, x]
e.plot_ecg([i for i in range(len(e.model_array_list))], e.ecg(), "ecg")
