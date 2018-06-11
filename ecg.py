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

    def __init__(self, centre, probe_height, path, model_array_list=None):
        """
        ECG Initialisation
        :param centre: The point of ecg contact on the surface
        :param probe_height: Height of the probe above the surface
        :param path: The path for data to read and view
        """
        self.centre = centre  # (x, y), 0 based
        self.probe_height = probe_height
        self.path = path

        if model_array_list:
            self.model_array_list = model_array_list
        else:
            # Import the model_array from HFD5 format
            with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
                self.model_array_list = model_data_file['array_list'][:]
        self.refractory_period = max(self.model_array_list.flatten())

        self.voltage_array_list = [array[0, :, :].astype(int) for array in self.model_array_list]
        (y, x) = self.voltage_array_list[0].shape
        self.y1 = round(y / 2)
        self.voltage_array_list = [np.roll(array, self.y1 - self.centre[1], axis=0) for array in
                                   self.voltage_array_list]

        create_dir('{}/ecg'.format(self.path))

    def voltage(self, voltage_array):
        """
        Get the ECG voltage for the current time step.
        """

        rows = voltage_array.shape[0]
        columns = voltage_array.shape[1]

        y_pos_diff = np.array([i for i in range(rows)]) - self.y1
        y_pos_diff_transpose = y_pos_diff.reshape(rows, 1)
        x_pos_diff = np.array([i for i in range(columns)]) - self.centre[0]
        x_pos_diff_matrix = np.tile(x_pos_diff, (rows, 1))
        y_pos_diff_matrix = np.tile(y_pos_diff_transpose, (1, columns))
        normalise = (x_pos_diff_matrix ** 2 + y_pos_diff_matrix ** 2 + self.probe_height ** 2) ** 1.5

        y_volt_diff = np.insert(np.diff(voltage_array, axis=0), 0, voltage_array[0, :] - voltage_array[-1, :], axis=0
                                ) * 93 / 50
        x_volt_diff = np.insert(np.diff(voltage_array, axis=1), 0, voltage_array[:, 0], axis=1
                                ) * 93 / 50

        voltage = np.sum(((x_pos_diff * x_volt_diff) + (y_pos_diff_transpose * y_volt_diff)) / normalise)

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
                '\r' + "calculating ecg at ({}, {}), time_step: {}/{}...".format(self.centre[0], self.centre[1],
                                                                                 start + i, total_time - 1))
            sys.stdout.flush()
            voltage_list[i] = self.voltage(self.voltage_array_list[i])

        return voltage_list

    def plot_ecg(self, x, y):
        """Plot the ECG."""

        plt.figure()
        sns.set_style('ticks')
        plt.plot(x, y, label="ecg")
        plt.xlabel("Time")
        plt.ylabel("Voltage (V)")
        plt.title("ECG at {}".format(self.centre))
        plt.legend(loc=0, fontsize=12, frameon=True)
        plt.margins(x=0)
        plt.savefig('data/{}/ecg/ecg_{}.png'.format(self.path, self.centre))
        plt.close()


# model_ecg = ECG([137, 100], 3, "mechanism/focal/18-02-15_15-09-29 (130, 156)")
# model_ecg.plot_ecg([i for i in range(len(model_ecg.model_array_list))], model_ecg.ecg())
