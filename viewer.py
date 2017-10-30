import h5py
import numpy as np
import os
import pyqtgraph as pg
import seaborn as sns

from matplotlib import pyplot as plt


class Viewer:
    """
    A class to read and view the data output for the model.
    """

    def __init__(self, path):
        """
        Viewer Initialisation
        :param path: The path for data to read and view
        """
        self.path = path

    def view_model_array(self):
        """Read the HDF5 data file and view the model array."""

        print("reading & viewing model array...")

        # Import the model_array from HFD5 format
        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
            model_array_list = model_data_file['array_list'][:]

        app = pg.mkQApp()
        view = pg.GraphicsLayoutWidget()
        view.show()
        w1 = view.addPlot()
        w1.disableAutoRange()
        for array in model_array_list:
            w1.plot(array)
        w1.autoRange()
        app.exec_()

        # if len(np.shape(model_array_list[0])) == 2:

        # TODO: CHECK 2D VS 3D

    def plot_model_stats(self):
        """Read the HDF5 data file and plot the model statistics."""

        print("reading & plotting model statistics...")

        # Create output directory if it doesn't exist
        if not os.path.exists(os.path.join('data', self.path, 'model_statistics')):
            os.makedirs(os.path.join('data', self.path, 'model_statistics'))

        # Import the model_stat_dict from HFD5 format
        with h5py.File('data/{}/data_files/model_stat_dict'.format(self.path), 'r') as model_stats_file:
            model_stat_dict = {k: v[:] for k, v in model_stats_file.items()}

        # Create data keys and values for plotting
        data_to_plot = []
        time = [i for i in range(max(map(len, model_stat_dict.values())))]  # get longest time series in dict
        size = sum([stat_list[0] for stat_list in model_stat_dict.values()])  # sum values at time=0 for model size

        data_excited = [(model_stat_dict['excited'] / size, "Excited")]
        data_to_plot.append({'data': data_excited, 'x_label': "Time", 'y_label': "Fraction of Cells", 'y_lim': None,
                             'title': "Excited Cells", 'filename': "excited.png"})

        data_resting = [(model_stat_dict['resting'] / size, "Resting")]
        data_to_plot.append({'data': data_resting, 'x_label': "Time", 'y_label': "Fraction of Cells", 'y_lim': [0, 1],
                             'title': "Resting Cells", 'filename': "resting.png"})

        data_refractory = [(model_stat_dict['refractory'] / size, "Refractory")]
        data_to_plot.append({'data': data_refractory, 'x_label': "Time", 'y_label': "Fraction of Cells",
                             'y_lim': [0, 1], 'title': "Refractory Cells", 'filename': "refractory.png"})

        data_failed = [(model_stat_dict['failed'] / size, "Failed")]
        data_to_plot.append({'data': data_failed, 'x_label': "Time", 'y_label': "Fraction of Cells", 'y_lim': None,
                             'title': "Failed Cells", 'filename': "failed.png"})

        data_overall = [*data_excited, *data_resting, *data_refractory, *data_failed]
        data_to_plot.append({'data': data_overall, 'x_label': "Time", 'y_label': "Fraction of Cells", 'y_lim': [0, 1],
                             'title': "Overall Cells", 'filename': "overall.png"})

        # Plot data keys and values
        for data_dict in data_to_plot:
            plt.figure()
            sns.set_style('ticks')
            for (y, l) in data_dict['data']:
                plt.plot(time, y, label=l)
            plt.xlabel(data_dict['x_label'])
            plt.ylabel(data_dict['y_label'])
            plt.ylim(data_dict['y_lim'])
            plt.legend(loc=0, fontsize=12, frameon=True)
            plt.title(data_dict['title'])
            plt.savefig(os.path.join('data', self.path, 'model_statistics', data_dict['filename']))
            plt.close()

    def plot_model_array(self):
        """Read the HDF5 data file and view the model array."""

        print("reading & plotting model array...")

        # Create output directory if it doesn't exist
        if not os.path.exists(os.path.join('data', self.path, 'model_array')):
            os.makedirs(os.path.join('data', self.path, 'model_array'))

        # TODO: CHECK 2D VS 3D
        # TODO: (output video - only way is matplotlib or screencap/snapshots (specify timestep) here)

    def plot_ecg(self):
        """Read the HDF5 data file create an ECG from the model array."""
