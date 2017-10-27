import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
import h5py


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

        print(model_stat_dict)

        data_to_plot = []
        time = [i for i in range(max(map(len, model_stat_dict)))]
        size = sum([stat_list[0] for stat_list in model_stat_dict.values()])

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
# TODO: model folder (output video/snapshots here)
# TODO: ECGS
