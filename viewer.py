
import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


def animate(results, refractory_period, save=False, cross_view=False, cross_pos=-1):
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
    fig = plt.figure()
    if cross_view:
        gs = gridspec.GridSpec(1, 2, width_ratios=np.shape(results)[-2:])
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ims = [[ax1.imshow(frame[:,:,0], animated=True, vmin=0, vmax=refractory_period),
                ax2.imshow(frame[:, cross_pos, :], animated=True, vmin=0, vmax=refractory_period)]
               for frame in results]
    else:
        ims = [[plt.imshow(frame[:,:,0], animated=True, vmin=0, vmax=refractory_period)] for frame in results]
    ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,
                                    repeat_delay=500)
    if save:
        plt.rcParams['animation.ffmpeg_path'] = "C:/Program Files/ffmpeg-20170807-1bef008-win64-static/bin/ffmpeg.exe"

        writer = animation.writers['ffmpeg'](fps=30)
        print('SAVING')
        t = time.time()
        ani.save(save, writer)
        print('Saved as {} in {:.1f} seconds'.format(save, time.time()-t))
    plt.show()