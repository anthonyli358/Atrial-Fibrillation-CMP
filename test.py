import numpy as np
import matplotlib.pyplot as plt


def distplot():
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, True, True, True)
    pos, frac = np.load('record/0.99,0.07.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax1.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax1.text(12.5, .22, '$x = 0.99; yz = 0.07$', fontsize=12, horizontalalignment='center')

    pos, frac = np.load('record/0.99,0.1.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax2.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax2.text(12.5, .22, '$x = 0.99; yz = 0.1$', fontsize=12, horizontalalignment='center')

    pos, frac = np.load('record/0.85,0.07.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax3.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax3.text(12.5, .22, '$x = 0.85; yz = 0.07$', fontsize=12, horizontalalignment='center')

    pos, frac = np.load('record/0.85,0.1.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax4.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax4.text(12.5, .22, '$x = 0.85; yz = 0.1$', fontsize=12, horizontalalignment='center')

    pos, frac = np.load('record/0.8,0.07.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax5.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax5.text(12.5, .22, '$x = 0.8; yz = 0.07$', fontsize=12, horizontalalignment='center')

    pos, frac = np.load('record/0.8,0.1.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax6.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax6.text(12.5, .22, '$x = 0.8; yz = 0.1$', fontsize=12, horizontalalignment='center')

    ax1.yaxis.set_ticks(np.arange(0, 0.3, .05))
    ax1.xaxis.set_ticks(np.arange(0, 25.1, 5))
    ax5.set_xlabel('Depth')
    ax6.set_xlabel('Depth')
    ax1.set_ylabel('Frequency')
    ax3.set_ylabel('Frequency')
    ax5.set_ylabel('Frequency')
    plt.show()


def fracplot():
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, True, True, True)
    pos, frac = np.load('record/0.99,0.07.npy')
    frac[frac == None] = 0
    frac = np.array(frac, dtype='int16')
    ax1.hist(frac / 1000, 100, (0, 1), density=True)
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax1.text(.5, 6, '$x = 0.99; yz = 0.07$\nave={:.2f}'.format(ave), fontsize=12, horizontalalignment='center',
             verticalalignment='top')

    pos, frac = np.load('record/0.99,0.1.npy')
    frac[frac == None] = 0
    frac = np.array(frac, dtype='int16')
    ax2.hist(frac / 1000, 100, (0, 1), density=True)
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax2.text(.5, 6, '$x = 0.99; yz = 0.1$\nave={:.2f}'.format(ave), fontsize=12, horizontalalignment='center',
             verticalalignment='top')

    pos, frac = np.load('record/0.85,0.07.npy')
    frac[frac == None] = 0
    frac = np.array(frac, dtype='int16')
    ax3.hist(frac / 1000, 100, (0, 1), density=True)
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax3.text(.5, 6, '$x = 0.85; yz = 0.07$\nave={:.2f}'.format(ave), fontsize=12, horizontalalignment='center',
             verticalalignment='top')

    pos, frac = np.load('record/0.85,0.1.npy')
    frac[frac == None] = 0
    frac = np.array(frac, dtype='int16')
    ax4.hist(frac / 1000, 100, (0, 1), density=True)
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax4.text(.5, 6, '$x = 0.85; yz = 0.1$\nave={:.2f}'.format(ave), fontsize=12, horizontalalignment='center',
             verticalalignment='top')

    pos, frac = np.load('record/0.8,0.07.npy')
    frac[frac == None] = 0
    frac = np.array(frac, dtype='int16')
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax5.hist(frac / 1000, 100, (0, 1), density=True)
    ax5.text(.5, 6, '$x = 0.8; yz = 0.07$\nave={:.2f}'.format(ave), fontsize=12, horizontalalignment='center',
             verticalalignment='top')

    pos, frac = np.load('record/0.8,0.1.npy')
    frac[frac == None] = 0
    frac = np.array(frac, dtype='int16')
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax6.hist(frac / 1000, 100, (0, 1), density=True)
    ax6.text(.5, 6, '$x = 0.8; yz = 0.1$\nave={:.2f}'.format(ave), fontsize=12, horizontalalignment='center',
             verticalalignment='top')

    # ax1.yaxis.set_ticks(np.arange(0, 0.3, .05))
    # ax1.xaxis.set_ticks(np.arange(0, 25.1, 5))
    ax5.set_xlabel('Time in fibrillation')
    ax6.set_xlabel('Time in fibrillation')
    ax1.set_ylabel('Frequency / %')
    ax3.set_ylabel('Frequency / %')
    ax5.set_ylabel('Frequency / %')
    plt.show()


def oneplot():
    pos, frac = np.load('record/0.8,0.1.npy')
    frac[frac == None] = 0
    frac = np.array(frac, dtype='int16')
    pos = np.array(pos[np.nonzero(pos)])
    ave = np.average(frac)
    std = np.std(frac)

    print(ave, std)

    plt.hist(frac / 1000, 100, (0, 1), density=True)
    # plt.title('x: 0.96; yz: 0.07')
    plt.show()


def curveplot():
    yzs = np.arange(0.06, 0.121, 0.01)
    xs = np.arange(0.8, 1.001, 0.01)
    X, Y = np.meshgrid(xs, yzs)
    aves = np.zeros(np.shape(X))
    stds = np.zeros(np.shape(X))
    for i, yz in enumerate(yzs):
        for j, x in enumerate(xs):
            try:
                pos, frac = np.load('record/{},{}.npy'.format(str(x), str(yz)))
                frac = np.array(frac, dtype='int16')
                aves[i, j] = np.average(frac)
                stds[i, j] = np.std(frac)
            except:
                pass

    aves = np.transpose(aves) / 1000
    stds = np.transpose(stds) / 1000
    plt.figure()
    plt.imshow(aves, vmin=0, vmax=1, extent=(0.07, .12, 0.8, 1.0), origin='lower',
               cmap='Greys')
    plt.colorbar()
    plt.figure()
    plt.imshow(stds, vmin=0, extent=(0.07, .12, 0.8, 1.0), origin='lower',
               cmap='Greys')
    plt.colorbar()
    plt.show()


def yriskcurve():
    yzs = np.arange(0.07, .1201, .01)
    aves = []
    stds = []
    for yz in yzs:
        pos, frac = np.load('record/1.0,{}.npy'.format(str(yz)))
        frac = np.array(frac, dtype='int16')
        aves.append(np.average(frac))
        stds.append(np.std(frac))
    plt.figure()
    plt.errorbar(yzs, aves, stds)


def xriskcurve():
    xs = np.arange(0.8, 1.001, .01)
    aves = []
    stds = []
    for x in xs:
        pos, frac = np.load('record/{},0.07.npy'.format(str(x)))
        frac = np.array(frac, dtype='int16')
        aves.append(np.average(frac))
        stds.append(np.std(frac))
    print(aves)
    plt.figure()
    plt.errorbar(xs, aves, stds)


distplot()
plt.show()
