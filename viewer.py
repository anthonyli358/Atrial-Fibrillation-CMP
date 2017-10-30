import h5py
import os

from matplotlib import pyplot as plt

import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np


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
        """Read the HDF5 data files and plot the model statistics."""

        print("reading & plotting model statistics...")

        # Create output directory if it doesn't exist
        if not os.path.exists(os.path.join('data', self.path, 'model_statistics')):
            os.makedirs(os.path.join('data', self.path, 'model_statistics'))

        with h5py.File('data/{}/data_files/model_statistics'.format(self.path), 'r') as model_stats_file:
            model_stat_dict = {k: v[:] for k, v in model_stats_file.items()}

        data_to_plot = []
        time = [i for i in range(max(map(len, model_stat_dict.values())))]
        size = sum([stat_list[0] for stat_list in model_stat_dict.values()])

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

        for data_dict in data_to_plot:
            plt.figure()
            for (y, l) in data_dict['data']:
                plt.plot(time, y, label=l)
            plt.xlabel(data_dict['x_label'])
            plt.ylabel(data_dict['y_label'])
            plt.ylim(data_dict['y_lim'])
            plt.legend(loc=0)
            plt.title(data_dict['title'])
            plt.savefig(os.path.join('data', self.path, 'model_statistics', data_dict['filename']))
            plt.close()

# def animate(results, refractory_period, save=False, cross_view=False, cross_pos=-1):
#     """
#     Animate time series of activation matrices.
#
#     :rtype: object
#     :param results: Time series of activation matrices
#     :param refractory_period: Refractory period used in substrate.
#     :param save: If specified, name mp4 filename to save to.
#     :param cross_view: Enable the cross-view in the animation.
#     :param cross_pos: Specify location of cross-view.
#     :return:
#     """
#     fig = plt.figure()
#     if cross_view:
#         gs = gridspec.GridSpec(1, 2, width_ratios=np.shape(results)[-2:])
#         ax1 = plt.subplot(gs[0])
#         ax2 = plt.subplot(gs[1])
#         ims = [[ax1.imshow(frame[:, :, 0], animated=True, vmin=0, vmax=refractory_period),
#                 ax2.imshow(frame[:, cross_pos, :], animated=True, vmin=0, vmax=refractory_period),
#                 ax1.axvline(x=cross_pos, color='cyan', zorder=10, animated=True, linestyle='--')]
#                for frame in results]
#
#     else:
#         ims = [[plt.imshow(frame[:, :, 0], animated=True, vmin=0, vmax=refractory_period)] for frame in results]
#     ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,
#                                     repeat_delay=500)
#     if save:
#         plt.rcParams['animation.ffmpeg_path'] = "C:/Program Files/ffmpeg-20170807-1bef008-win64-static/bin/ffmpeg.exe"
#
#         writer = animation.writers['ffmpeg'](fps=30)
#         print("SAVING")
#         t = time.time()
#         ani.save(save, writer)
#         print("Saved as {} in {:.1f} seconds".format(save, time.time() - t))
#     plt.show()

# TODO: 2D AND 3D VIEWING OPTIONS
# TODO: JUST ANIMATE DATA OPTION
# TODO: model folder (output video/snapshots (specify timestep) here)
# TODO: ECGS
