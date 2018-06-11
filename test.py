import numpy as np
import matplotlib.pyplot as plt


def distplot():
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, True, True, True)
    pos, frac = np.load('record/0.99,0.07.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax1.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax1.text(12.5, .22, r'$\nu_x = 0.99, \nu_{y,z} = 0.07$', fontsize=15, horizontalalignment='center')
    print(len(pos))

    pos, frac = np.load('record/0.99,0.1.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax2.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax2.text(12.5, .22, r'$\nu_x = 0.99, \nu_{y,z} = 0.1$', fontsize=15, horizontalalignment='center')

    pos, frac = np.load('record/0.85,0.07.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax3.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax3.text(12.5, .22, r'$\nu_x = 0.85, \nu_{y,z} = 0.07$', fontsize=15, horizontalalignment='center')

    pos, frac = np.load('record/0.85,0.1.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax4.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax4.text(12.5, .22, r'$\nu_x = 0.85, \nu_{y,z} = 0.1$', fontsize=15, horizontalalignment='center')

    pos, frac = np.load('record/0.8,0.07.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax5.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax5.text(12.5, .22, r'$\nu_x = 0.8, \nu_{y,z} = 0.07$', fontsize=15, horizontalalignment='center')

    pos, frac = np.load('record/0.8,0.1.npy')
    pos = np.array(pos[np.nonzero(pos)])
    ax6.hist([i[0] for i in pos], 25, (0, 25), density=True)
    ax6.text(12.5, .22, r'$\nu_x = 0.8, \nu_{y,z} = 0.1$', fontsize=15, horizontalalignment='center')

    ax1.yaxis.set_ticks(np.arange(0, 0.35, .05))
    ax2.yaxis.set_ticks(np.arange(0, 0.35, .05))
    ax3.yaxis.set_ticks(np.arange(0, 0.35, .05))
    ax1.xaxis.set_ticks(np.arange(0, 25.1, 5))
    ax2.xaxis.set_ticks(np.arange(0, 25.1, 5))
    ax3.xaxis.set_ticks(np.arange(0, 25.1, 5))
    ax4.xaxis.set_ticks(np.arange(0, 25.1, 5))
    ax5.xaxis.set_ticks(np.arange(0, 25.1, 5))
    ax6.xaxis.set_ticks(np.arange(0, 25.1, 5))

    ax1.set_xlabel(r'$z$', fontsize=12)
    ax2.set_xlabel(r'$z$', fontsize=12)
    ax3.set_xlabel(r'$z$', fontsize=12)
    ax4.set_xlabel(r'$z$', fontsize=12)
    ax5.set_xlabel(r'$z$', fontsize=12)
    ax6.set_xlabel(r'$z$', fontsize=12)
    ax1.set_ylabel('Circuit Fraction', fontsize=12)
    ax2.set_ylabel('Circuit Fraction')
    ax3.set_ylabel('Circuit Fraction')
    ax4.set_ylabel('Circuit Fraction')
    ax5.set_ylabel('Circuit Fraction')
    ax6.set_ylabel('Circuit Fraction', fontsize=12)
    plt.show()


def fracplot():
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, True, True, True)
    pos, frac = np.load('record/0.99,0.07.npy')
    for x in frac:
        if x is None:
            x=0
    frac = np.array(frac, dtype='int16')
    ax1.hist(frac / 1000, 100, (0, 1), density=True)
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax1.text(.5, 30, r', $<$AF Time$>={:.2f}$'.format(ave), fontsize=15, horizontalalignment='center',
             verticalalignment='top')

    pos, frac = np.load('record/0.99,0.1.npy')
    for x in frac:
        if x is None:
            x=0
    frac = np.array(frac, dtype='int16')
    ax2.hist(frac / 1000, 100, (0, 1), density=True)
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax2.text(.5, 30, r', $<$AF Time$>={:.2f}$'.format(ave), fontsize=15, horizontalalignment='center',
             verticalalignment='top')

    pos, frac = np.load('record/0.85,0.07.npy')
    for x in frac:
        if x is None:
            x=0
    frac = np.array(frac, dtype='int16')
    ax3.hist(frac / 1000, 100, (0, 1), density=True)
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax3.text(.5, 30, r'$, <AF Time>={:.2f}$'.format(ave), fontsize=15, horizontalalignment='center',
             verticalalignment='top')

    pos, frac = np.load('record/0.85,0.1.npy')
    for x in frac:
        if x is None:
            x=0
    frac = np.array(frac, dtype='int16')
    ax4.hist(frac / 1000, 100, (0, 1), density=True)
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax4.text(.5, 30, r'$, <AF Time>={:.2f}$'.format(ave), fontsize=15, horizontalalignment='center',
             verticalalignment='top')

    pos, frac = np.load('record/0.8,0.07.npy')
    for x in frac:
        if x is None:
            x=0
    frac = np.array(frac, dtype='int16')
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax5.hist(frac / 1000, 100, (0, 1), density=True)
    ax5.text(.5, 30, r'$, <AF Time>={:.2f}$'.format(ave), fontsize=15, horizontalalignment='center',
             verticalalignment='top')

    pos, frac = np.load('record/0.8,0.1.npy')
    for x in frac:
        if x is None:
            x=0
    frac = np.array(frac, dtype='int16')
    ave = np.average(frac) / 1000
    std = np.std(frac)
    ax6.hist(frac / 1000, 100, (0, 1), density=True)
    ax6.text(.5, 30, r'$, <AF Time>={:.2f}$'.format(ave), fontsize=15, horizontalalignment='center',
             verticalalignment='top')

    # ax1.yaxis.set_ticks(np.arange(0, 0.1, .05))
    # ax1.xaxis.set_ticks(np.arange(0, 25.1, 5))
    ax5.set_xlabel('Fractional time in AF', fontsize=12)
    ax6.set_xlabel('Fractional time in AF', fontsize=12)
    ax1.set_ylabel('Probability', fontsize=12)
    ax3.set_ylabel('Probability', fontsize=12)
    ax5.set_ylabel('Probability', fontsize=12)
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
    yzs = np.arange(0, 1, 0.01)
    xs = np.arange(0, 1.0, 0.01)
    X, Y = np.meshgrid(xs, yzs)
    aves = np.zeros(np.shape(X))
    stds = np.zeros(np.shape(X))
    for i, yz in enumerate(yzs):
        for j, x in enumerate(xs):
            try:
                pos, frac = np.load('roughrecord/{},{}.npy'.format(str(x), str(yz)))
                frac = np.array(frac, dtype='int16')
                aves[i, j] = np.average(frac)
                stds[i, j] = np.std(frac)
            except:
                pass

    plt.figure()
    plt.imshow(aves, vmin=0, vmax=1000, extent=(0, 1, 0, 1), origin='lower')
    plt.figure()
    plt.imshow(stds, vmin=0, extent=(0, 1, 0, 1), origin='lower')
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
        pos, frac = np.load('record/{},0.12.npy'.format(str(x)))
        frac = np.array(frac, dtype='int16')
        aves.append(np.average(frac))
        stds.append(np.std(frac))
    print(aves)
    plt.figure()
    plt.errorbar(xs, aves, stds)


fracplot()
plt.show()
