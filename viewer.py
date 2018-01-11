import h5py
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sys
import scipy.ndimage.filters as filters
import scipy.ndimage.morphology as morphology

from matplotlib import pyplot as plt

plt.rcParams['animation.ffmpeg_path'] = "data/ffmpeg-20170807-1bef008-win64-static/bin/ffmpeg.exe"
from matplotlib import animation  # must be defined after defining ffmpeg line
from matplotlib import gridspec
from matplotlib import patches
from mpl_toolkits.mplot3d import Axes3D
from time import time

from utility_methods import *


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

        create_dir('{}/model_statistics'.format(self.path))

        # Import the pandas stat_data_frame from HDF5 format
        stat_data_frame = pd.read_hdf('data/{}/data_files/stat_data_frame'.format(self.path), 'stat_data_frame')
        size = stat_data_frame.loc[0].sum()  # sum values at time=0 for model size

        plotting_data_frame = stat_data_frame.copy()/size  # normalise values and change variable name for clarity

        # Plot statistics
        for key in stat_data_frame.columns.values.tolist():
            plt.figure()
            sns.set_style('ticks')
            stat_data_frame[key].plot(title="{} Cells".format(key).title())
            plt.xlabel("Time")
            plt.ylabel("Number of Cells")
            plt.legend(loc=0, fontsize=12, frameon=True)
            plt.margins(x=0)
            plt.savefig('data/{}/model_statistics/{}.png'.format(self.path, key))
            plt.close()

        plt.figure()
        sns.set_style('ticks')
        plotting_data_frame.plot(title="Overall Cells", ylim=[0, 1])
        plt.xlabel("Time")
        plt.ylabel("Fraction of Cells")
        plt.legend(loc=0, fontsize=12, frameon=True)
        plt.margins(x=0)
        plt.savefig('data/{}/model_statistics/overall.png'.format(self.path))
        plt.close()

    def detect_local_maxima(self, arr):
        # https://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array/3689710#3689710
        """
        Takes an array and detects the troughs using the local maximum filter.
        Returns a boolean mask of the troughs (i.e. 1 when
        the pixel's value is the neighborhood maximum, 0 otherwise)
        """
        # define an connected neighborhood
        # http://www.scipy.org/doc/api_docs/SciPy.ndimage.morphology.html#generate_binary_structure
        neighborhood = morphology.generate_binary_structure(len(arr.shape), 2)
        # apply the local maxmimum filter; all locations of minimum value
        # in their neighborhood are set to 1
        # http://www.scipy.org/doc/api_docs/SciPy.ndimage.filters.html#minimum_filter
        local_max = (filters.maximum_filter(arr, footprint=neighborhood, mode='constant') == arr)
        # local_min is a mask that contains the peaks we are
        # looking for, but also the background.
        # In order to isolate the peaks we must remove the background from the mask.
        #
        # we create the mask of the background
        background = (arr == 0)
        #
        # a little technicality: we must erode the background in order to
        # successfully subtract it from local_min, otherwise a line will
        # appear along the background border (artifact of the local minimum filter)
        # http://www.scipy.org/doc/api_docs/SciPy.ndimage.morphology.html#binary_erosion
        eroded_background = morphology.binary_erosion(
            background, structure=neighborhood, border_value=1)
        #
        # we obtain the final mask, containing only peaks,
        # by removing the background from the local_min mask
        detected_maxima = local_max ^ eroded_background

        return np.where(detected_maxima)

    def moving_average(self, data, n=3):
        smoothed_data = []
        for i in range(n, len(data) - n):
            smoothed_data.append(sum(data[i - n:i + n]) / (2 * n + 1))

        return smoothed_data

    def time_since_last_excitation(self, slice):

        print("reading & animating model array...")

        # Import the model_array from HFD5 format
        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
            model_array_list = model_data_file['array_list'][:]

        # TODO: MOVE TO PATHLENGTH CLASS

        rest_time_array = np.zeros(model_array_list[0].shape)
        time_array = np.zeros(model_array_list[0].shape)
        truth_array = np.zeros(model_array_list[0].shape)
        list = []

        for array in model_array_list[0:2000]:
            excited = array == 50

            rest_time_array[~excited] += 1
            same = time_array == rest_time_array
            not_same = time_array != rest_time_array

            truth_array[excited & same] = 1
            truth_array[excited & not_same] = 0

            time_array[excited] = rest_time_array[excited]
            rest_time_array[excited] = 0

            list.append(truth_array.copy())

        return list

    def animate_model_array(self, highlight=None, save=False, cross_view=False, cross_pos=None, remove_refractory=False):
        """Read the HDF5 data file and animate the model array."""

        # TODO: ALLOW THIS FUNCTION WITHOUT SAVING DATA

        print("reading & animating model array...")

        # Import the model_array from HFD5 format
        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
            model_array_list = model_data_file['array_list'][:]

        refractory_period = max(model_array_list.flatten())
        if remove_refractory:
            for array in model_array_list:
                excited = array >= 40
                array[~excited] = 0
                array[excited] = (array[excited] - 40) * 3 + 20

        fig = plt.figure(1)
        if cross_view:
            gs = gridspec.GridSpec(1, 2, width_ratios=[np.shape(model_array_list)[3], np.shape(model_array_list)[1]])
            ax1 = plt.subplot(gs[0])
            ax2 = plt.subplot(gs[1])
            ims = [[ax1.imshow(frame[24, :, :], animated=True, cmap='Greys_r', vmin=0, vmax=refractory_period),
                    ax2.imshow(np.transpose(frame[:, :, cross_pos]), animated=True, cmap='Greys_r', vmin=0, vmax=refractory_period),
                    ax1.axvline(x=cross_pos, color='r', zorder=10, animated=True, linestyle='--')]
                   for frame in model_array_list]

        # TODO: 2ND PLOT X AXIS

        else:
            ims = [[plt.imshow(frame[0, :, :], animated=True, cmap='Greys_r')]
                   for frame in highlight]

        ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True, repeat_delay=500)
        plt.show()

        # TODO: SAVING DOESN'T WORK
        if save:
            create_dir('{}/model_array'.format(self.path))

            writer = animation.writers['ffmpeg'](fps=30)
            print("Saving animation (approx 1s/10 time steps for 40000 cells)...")
            t = time()
            ani.save('data/{}/model_array/_animation.mp4', writer)
            print("Saved in {:.1f}s".format(save, time() - t))

            # TODO: ANIMATE A SPECIFIC TIME SEGMENT
            # TODO: CROSS VIEW

    def plot_model_array(self, highlight, time_steps=None, start=0):
        """
        Read the HDF5 data file and view the model array for a range of time steps.
        :param time_steps: Number of time steps to plot
        :param start: Start time
        """

        # highlight_min = highlight == np.min(highlight[np.nonzero(highlight)])

        print("reading model array...")

        create_dir('{}/model_array'.format(self.path))

        # TODO: CROSS VIEW

        # Import the model_array from HFD5 format
        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
            model_array_list = model_data_file['array_list'][:]

        total_time = len(model_array_list)
        refractory_period = max(model_array_list.flatten())

        if time_steps is None or time_steps > total_time:
            time_steps = total_time - start

        # World plotting axis initialisation
        ax = plt.figure(figsize=(20, 20)).add_subplot(1, 1, 1)
        plt.subplots_adjust(top=0.95, bottom=0.02, left=0.02, right=0.98)

        # TODO: VARIABLE FIGSIZE AND FONTSIZE - GET MODEL ARRAY SIZE FROM DATA
        # TODO: GRAPH STYLING
        # TODO: ADD AXIS LABELS.ETC

        # Plot the data for each time step
        for i in range(time_steps):
            sys.stdout.write(
                '\r' + "reading & plotting model array, time_step: {}/{}...".format(start + i, total_time - 1))
            sys.stdout.flush()
            ax.axis('off')
            plt.title("time={}".format(start + i), fontsize=40)
            plt.imshow(highlight[i][0, :, :], cmap='Greys_r', vmin=0, vmax=2)
            plt.savefig('data/{}/model_array/{}.png'.format(self.path, i))
            plt.cla()

    def plot_d3(self):

        print("reading model array...")

        create_dir('{}/model_array'.format(self.path))

        # Import the model_array from HFD5 format
        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
            model_array_list = model_data_file['array_list'][:]
        refractory_period = max(model_array_list.flatten())

        test = np.ones(model_array_list[100].shape, dtype=bool)
        colours = (model_array_list[100] / refractory_period).astype(str)

        fig = plt.figure()
        fig.set_alpha(0.3)
        ax = fig.gca(projection='3d')
        ax.voxels(test, facecolors=colours)
        plt.show()

        # TODO: SCALING AXIS
        # TODO: REMOVE CUBE OUTLINES
        # TODO: PYQT GRAPH


# TODO: @STATICMETHOD FOR PLOTTING
# TODO: LOAD DATA ON INITIALISATION
# TODO: COLOURBAR
