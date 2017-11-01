import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
plt.rcParams['image.cmap'] = 'viridis'


def animate(results, settings):
    """
    Animate time series of activation matrices.

    :rtype: object
    :param results: Time series of activation matrices
    :param refractory_period: Refractory period used in substrate.
    :param save: If specified, name mp4 filename to save to.
    :param cross_view: Enable the cross-view in the animation.
    :param cross_pos: Specify location of cross-view.
    :return:
    """
    cross_view = settings['viewer']['cross_view']
    cross_pos = settings['viewer']['cross_pos']
    refractory_period = settings['structure']['refractory_period']
    save = settings['viewer']['save']
    interval = settings['viewer']['interval']

    fig = plt.figure()
    if cross_view:
        gs = gridspec.GridSpec(1, 2, width_ratios=np.shape(results)[2:0:-1])
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ims = [[ax1.imshow(frame[0, :, :], animated=True, vmin=0, vmax=refractory_period),
                ax2.imshow(np.transpose(frame[:, :, cross_pos]), animated=True, vmin=0, vmax=refractory_period),
                ax1.axvline(x=cross_pos, color='cyan', zorder=10, animated=True, linestyle='--')]
               for frame in results]

    else:
        ims = [[plt.imshow(frame[0, :, :], animated=True, vmin=0, vmax=refractory_period)] for frame in results]
    ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True,
                                    repeat_delay=500)
    if save:
        plt.rcParams['animation.ffmpeg_path'] = "C:/Program Files/ffmpeg-20170807-1bef008-win64-static/bin/ffmpeg.exe"

        writer = animation.writers['ffmpeg'](fps=30)
        print("SAVING")
        t = time.time()
        ani.save(save, writer)
        print("Saved as {} in {:.1f} seconds".format(save, time.time() - t))
    plt.show()

# TODO: 2D AND 3D VIEWING OPTIONS
# TODO: model folder (output video/snapshots here)
# TODO: model statistics folder
# TODO: resting.etc cells over time, and ecgs over time
