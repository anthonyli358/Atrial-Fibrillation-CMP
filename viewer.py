import h5py
import numpy as np
import pandas as pd
import seaborn as sns
import sys

from matplotlib import pyplot as plt

plt.rcParams['animation.ffmpeg_path'] = "data/ffmpeg-20170807-1bef008-win64-static/bin/ffmpeg.exe"
from matplotlib import animation  # must be defined after defining ffmpeg line
from matplotlib import gridspec
from matplotlib import cm
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

        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
            dimensions = np.shape(model_data_file['array_list'][0])
        size = np.product(dimensions)  # sum values at time=0 for model size
        area = np.product(dimensions[:-1])
        plotting_data_frame = stat_data_frame.copy()  # Change variable name for clarity

        # Plot statistics
        for key in stat_data_frame.columns.values.tolist():
            plt.figure()
            sns.set_style('ticks')
            (plotting_data_frame[key]/(size if key != 'excited' else area)).plot(title="{} Cells".format(key).title())
            plt.xlabel("Time")
            plt.ylabel("Fraction of Cells" if key !='excited' else "Number of Excited Cells / Ideal Number of Excited Cells")
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

    def import_data(self):
        # Import the model_array from HFD5 format
        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'r') as model_data_file:
            model_array_list = model_data_file['array_list'][:]

        return model_array_list

    def animate_model_array(self, model_array_list, highlight=None, save=False, layer=0, cross_view=False, cross_pos=None, remove_refractory=False):
        """Read the HDF5 data file and animate the model array."""

        # TODO: ALLOW THIS FUNCTION WITHOUT SAVING DATA
        # TODO: TIME=i IN TITLE

        print("animating model array...")

        refractory_period = max(model_array_list.flatten())
        print(highlight)

        if highlight:
            print("highlighting circuit cells...")
            # create possible views
            (xy_view, xz_view, yz_view) = (model_array_list.copy() for _ in range(3))
            for point in highlight:
                # frame[point] = 51
                # 'cell transparency' to always see circuit shape
                xy_view[0][:, point[1], point[2]] = 51
                xz_view[0][point[0], :, point[2]] = 51
                yz_view[0][point[0], point[1], :] = 51
            for i in range(len(model_array_list)):
                xy_view[i][xy_view[0] == 51] = 51
                xz_view[i][xz_view[0] == 51] = 51
                yz_view[i][yz_view[0] == 51] = 51

        # Create cmap
        highlight_cmap = cm.get_cmap('Greys_r')
        highlight_cmap.set_over('r')

        if remove_refractory:
            for array in model_array_list:
                excited = array >= refractory_period * 0.8
                array[~excited] = 0
                array[excited] = (array[excited] - (refractory_period * 0.8)) * 3 + (refractory_period * 0.4)

        fig = plt.figure(1)
        if cross_view:
            gs = gridspec.GridSpec(1, 2, width_ratios=[np.shape(model_array_list)[3], np.shape(model_array_list)[1]])
            ax1 = plt.subplot(gs[0])
            ax2 = plt.subplot(gs[1])
            view1 = xy_view if highlight else model_array_list
            view2 = yz_view if highlight else model_array_list
            ims = [[ax1.imshow(view1[i][layer, :, :],
                               animated=True, vmin=0, vmax=refractory_period, origin='lower', cmap=highlight_cmap),
                    ax2.imshow(np.transpose(view2[i][:, :, cross_pos]), animated=True, cmap=highlight_cmap,
                               vmin=0, vmax=refractory_period, origin='lower'),
                    ax1.axvline(x=cross_pos, color='b', zorder=10, animated=True, linestyle='--'),
                    ax1.text(100, 220, "time=".format(i), size=plt.rcParams["axes.titlesize"])]
                   for i in range(len(model_array_list))]

        else:
            view = xy_view if highlight else model_array_list
            ims = [[plt.imshow(view[i][layer, :, :],
                               animated=True, vmin=0, vmax=refractory_period, origin='lower', cmap=highlight_cmap),
                    plt.text(100, 220, "time=".format(i), size=plt.rcParams["axes.titlesize"])]
                   for i in range(len(model_array_list))]

        # fig, ax = plt.subplots()
        # image = ax.imshow(model_array_list[0, 0], animated=True, cmap='Greys_r', vmin=0,
        #                   vmax=refractory_period, origin='lower')

        # def func(t):
        #     image.set_array(model_array_list[t, 0])
        #     ax.set_title(t)
        #     return image,
        #
        # global ani
        # ani = animation.FuncAnimation(fig, func, interval=5, frames=len(model_array_list), blit=True)

        ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True, repeat_delay=500)
        plt.show()

        if save:
            create_dir('{}/model_array'.format(self.path))

            writer = animation.writers['ffmpeg'](fps=30)
            print("Saving animation (approx 1s/10 time steps for 40000 cells)...")
            t = time()
            ani.save('data/{}/model_array/_animation.mp4', writer)
            print("Saved in {:.1f}s".format(save, time() - t))

    def plot_circuit_3d(self, circuit):
        """
        Plot the circuit responsible for AF in 3D.
        :param circuit: The circuit points to plot
        """

        create_dir('{}/model_array'.format(self.path))
        circuit.append(circuit[0])

        z = [p[0] for p in circuit]
        y = [p[1] for p in circuit]
        x = [p[2] for p in circuit]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # ax.set_aspect('equal')
        # ax.auto_scale_xyz([0, 200], [0, 200], [0, 25])

        # Create cubic bounding box to simulate equal aspect ratio
        max_range = np.array([max(x) - min(x), max(y) - min(y), max(z) - min(z)]).max()
        xb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5 * (max(x) + min(x))
        yb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5 * (max(y) + min(y))
        zb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5 * (max(z) + min(z))
        # Comment or uncomment following both lines to test the fake bounding box:
        for xb, yb, zb in zip(xb, yb, zb):
            ax.plot([xb], [yb], [zb], 'w')

        ax.plot(x, y, z, color='r')
        ax.grid(False)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.set_zlim(0, 25)
        plt.savefig('data/{}/model_array/circuit_{}.png'.format(self.path, circuit[0]))
        plt.show()
        plt.close()

    def plot_model_array(self, model_array_list, time_steps=None, start=0):
        """
        Read the HDF5 data file and view the model array for a range of time steps.
        :param time_steps: Number of time steps to plot
        :param start: Start time
        """

        print("reading model array...")

        create_dir('{}/model_array'.format(self.path))
        total_time = len(model_array_list)

        if time_steps is None or time_steps > total_time:
            time_steps = total_time - start

        # World plotting axis initialisation
        ax = plt.figure(figsize=(20, 20)).add_subplot(1, 1, 1)
        plt.subplots_adjust(top=0.95, bottom=0.02, left=0.02, right=0.98)

        # TODO: VARIABLE FIGSIZE AND FONTSIZE - GET MODEL ARRAY SIZE FROM DATA

        # Plot the data for each time step
        for i in range(time_steps):
            sys.stdout.write(
                '\r' + "reading & plotting model array, time_step: {}/{}...".format(start + i, total_time - 1))
            sys.stdout.flush()
            # ax.axis('off')
            plt.title("time={}".format(start + i), fontsize=80)
            ax.xaxis.set_ticks([50, 100, 150])
            ax.yaxis.set_ticks([50, 100, 150])
            plt.xlabel("x", fontsize=80)
            plt.ylabel("y", fontsize=80, rotation=0, labelpad=30)
            plt.tick_params(axis='both', which='major', labelsize=50)
            plt.imshow(model_array_list[i][0, :, :], cmap='Greys_r', vmin=0, vmax=50, origin='lower')
            cbar = plt.colorbar()
            cbar.ax.tick_params(labelsize=50)
            plt.tight_layout()
            plt.savefig('data/{}/model_array/{}.png'.format(self.path, i))
            cbar.remove()
            plt.cla()

# TODO: COLOURBAR
