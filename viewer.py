import h5py
import numpy as np
import os
import seaborn as sns
import sys

from matplotlib import pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = "C:/Year4_Project/ffmpeg-20170807-1bef008-win64-static/bin/ffmpeg.exe"
from matplotlib import animation  # must be defined after defining ffmpeg line
from matplotlib import gridspec
from time import time


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

    def plot_model_array(self, time_steps=None, start=0):
        """
        Read the HDF5 data file and view the model array for a range of time steps.
        :param time_steps: Number of time steps to plot
        :param start: Start time
        """

        print("reading & plotting model array...")

        # Create output directory if it doesn't exist
        if not os.path.exists(os.path.join('data', self.path, 'model_array')):
            os.makedirs(os.path.join('data', self.path, 'model_array'))

        # TODO: ISSUE WITH THIS READ FUNCTION
        # Import the model_array from HFD5 format
        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
            model_array_list = model_data_file['array_list'][:]

        total_time = len(model_array_list)
        refractory_period = max(model_array_list.flatten())

        # TODO: CHECK 2D VS 3D

        if time_steps is None or time_steps > total_time:
            time_steps = total_time - start

        # World plotting axis initialisation
        ax = plt.figure(figsize=(20, 20)).add_subplot(1, 1, 1)
        plt.subplots_adjust(top=0.95, bottom=0.02, left=0.02, right=0.98)

        # TODO: VARIABLE FIGSIZE AND FONTSIZE - GET MODEL ARRAY SIZE FROM DATA

        # Plot the data for each time step
        for i in range(time_steps):
            sys.stdout.write(
                '\r' + 'reading & plotting model array, time_step: {}/{}...'.format(start + i, total_time - 1))
            sys.stdout.flush()
            ax.axis('off')
            plt.title('time={}'.format(start + i), fontsize=40)
            plt.imshow(model_array_list[start + i][:, :, 0], cmap='Greys_r', vmin=0, vmax=refractory_period)
            plt.savefig(os.path.join('data', self.path, 'model_array', '{}.png'.format(i)))
            plt.cla()

    def animate_model_array(self, save=True):
        """Read the HDF5 data file and animate the model array."""

        print("reading & animating model array...")

        # Import the model_array from HFD5 format
        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
            model_array_list = model_data_file['array_list'][:]

        refractory_period = max(model_array_list.flatten())

        # if len(np.shape(model_array_list[0])) == 3:

        fig = plt.figure()
        ims = [[plt.imshow(frame[:, :, 0], animated=True, cmap='Greys_r', vmin=0, vmax=refractory_period)]
               for frame in model_array_list]
        ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=500)

        plt.show()

        if save:
            if not os.path.exists(os.path.join('data', self.path, 'model_array')):
                os.makedirs(os.path.join('data', self.path, 'model_array'))

            writer = animation.writers['ffmpeg'](fps=30)
            print("Saving animation (approx 1s/10 time steps for 40000 cells)...")
            t = time()
            ani.save(os.path.join('data', self.path, 'model_array', '_animation.mp4'), writer)
            print("Saved in {:.1f}s".format(save, time() - t))

        # TODO: PYQTPLOT SO CAN GET ROTOR POSITIONS
        # TODO: 2D VS 3D
        # TODO: ANIMATE A SPECIFIC TIME SEGMENT
        # TODO: CROSS VIEW

            # if cross_view:
            #     gs = gridspec.GridSpec(1, 2, width_ratios=np.shape(results)[-2:])
            #     ax1 = plt.subplot(gs[0])
            #     ax2 = plt.subplot(gs[1])
            #     ims = [[ax1.imshow(frame[:, :, 0], animated=True, vmin=0, vmax=refractory_period),
            #             ax2.imshow(frame[:, cross_pos, :], animated=True, vmin=0, vmax=refractory_period),
            #             ax1.axvline(x=cross_pos, color='cyan', zorder=10, animated=True, linestyle='--')]
            #            for frame in results]
            #
            # else:

    def plot_ecg(self):
        """Read the HDF5 data file create an ECG from the model array."""
