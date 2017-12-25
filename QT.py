import sys
from PyQt5 import QtWidgets, QtGui

from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
import numpy as np

from time import sleep

import model
import main
import config

class AFInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.anim = Animation()
        #
        self.setCentralWidget(self.anim)
        self.setWindowIcon(QtGui.QIcon('icons8-heart-with-pulse-50.png'))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        settAct = QtWidgets.QAction('Open &Config', self)
        settAct.triggered.connect(self.show_config)
        fileMenu.addAction(settAct)

        viewMenu = menubar.addMenu('&View')
        phaseAct = QtWidgets.QAction('View &Phase spaces', self)
        phaseAct.triggered.connect(self.show_phase)
        viewMenu.addAction(phaseAct)

        self.toolbar = self.addToolBar('Play')
        playAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-play-50.png'), 'play', self)
        playAct.setCheckable(True)
        playAct.setChecked(True)
        playAct.triggered.connect(self.toggle_pause)
        playAct.setShortcut('space')
        chartAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-heat-map-50.png'), 'chart', self)
        chartAct.triggered.connect(self.show_phase)
        settAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-services-50.png'), 'settings', self)
        settAct.triggered.connect(self.show_config)
        self.toolbar.addActions([playAct, chartAct, settAct])
        self.toolbar.setMaximumHeight(25)


        self.setGeometry(300,100,300,400)
        self.setWindowTitle('AF Viewer')

        self.show()

    # def plot(self):
    #     data = [np.random.random() for i in range(10)]
    #     ax = self.figure.add_subplot(111)
    #     ax.plot(data)
    #
    #     self.canvas.draw()

    def toggle_pause(self):

        config.settings['pause'] ^= True

    def show_config(self):
        self.popup = Config()
        self.popup.setWindowTitle('Config')
        self.popup.show()

    def show_phase(self):
        self.popup = makePhases()
        self.popup.setWindowTitle('Phase Spaces')
        self.popup.show()




class Config(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        form = QtWidgets.QFormLayout()
        self.setWindowIcon(QtGui.QIcon('icons8-services-50.png'))
        self.sizeq= QtWidgets.QLineEdit(str(config.settings['structure']['size']))
        # self.sizeq.editingFinished.connect(self.printer)
        form.addRow(QtWidgets.QLabel('Dimensions'), self.sizeq)

        form.addRow(QtWidgets.QLabel('Linkage'), QtWidgets.QLineEdit())
        refrt = QtWidgets.QLineEdit('220')
        form.addRow(QtWidgets.QLabel('Refractory Period'), refrt)

        viewopts = QtWidgets.QComboBox()
        viewopts.addItems(['activation', 'count'])
        viewopts.currentTextChanged.connect(self.updateview)
        form.addRow(QtWidgets.QLabel('Animation Style'), viewopts)

        crosspos_slider = QtWidgets.QSlider(Qt.Horizontal)
        crosspos_slider.setValue(50)
        crosspos_slider.setRange(0, config.settings['structure']['size'][1]-1)
        crosspos_spin = QtWidgets.QSpinBox()
        crosspos_spin.setValue(config.settings['crosspos'])
        crosspos_spin.setRange(0, config.settings['structure']['size'][1]-1)

        crosspos_spin.valueChanged.connect(crosspos_slider.setValue)
        crosspos_slider.valueChanged.connect(crosspos_spin.setValue)

        crosspos_spin.valueChanged.connect(self.updatecrosspos)
        crosspos = QtWidgets.QHBoxLayout()
        crosspos.addWidget(crosspos_spin)
        crosspos.addWidget(crosspos_slider)
        form.addRow(QtWidgets.QLabel('Cross view position'), crosspos)

        self.setLayout(form)
        self.setWindowTitle('Configuration Settings')

    def updateview(self, val):
        config.settings['view'] = val

    def updatecrosspos(self, val):
        config.settings['crosspos'] = val


class makeCanvas(FigureCanvas):
    def __init__(self):
        self.figure = Figure(dpi=50)
        super().__init__(self.figure)
        self.compute_initial_figure()

        self.toolbar = NavigationToolbar(self, self)


    def compute_initial_figure(self):
        pass


class makePhases(makeCanvas):

    def compute_initial_figure(self):
        self.resize(400,350)
        names = ['Phase_Spaces/1_200_200.npy', 'Phase_Spaces/2_200_200.npy',
                 'Phase_Spaces/4_200_200.npy', 'Phase_Spaces/8_200_200.npy',
                 'Phase_Spaces/16_200_200.npy', 'Phase_Spaces/32_200_200.npy']
        compilation = []
        for i in names:
            compilation.append(np.load(i)[:, :, 2])

        for num, i in enumerate(compilation):
            ax = self.figure.add_subplot(200 + len(names)/2 * 10 + 1 + num)
            ax.set_title(names[num][13:-4])
            ax.imshow(i, extent=(0,1,0,1), origin='lower')


class Animation(makeCanvas):

    def compute_initial_figure(self):
        self.substrate = model.Model(**config.settings['structure'])

        gs = GridSpec(1, 2, width_ratios=config.settings['structure']['size'][-2::-1])

        self.ax1 = self.figure.add_subplot(gs[0])
        line = self.ax1.axvline(x=config.settings['crosspos'], color='cyan', linestyle='--')
        image = self.ax1.imshow(self.substrate.model_array[0], animated=True, cmap='Oranges_r',
                                vmin=0, vmax=config.settings['structure']['refractory_period'],
                                origin = 'lower', alpha=1, extent=(0, 200, 0, 200), interpolation='nearest',
                                zorder=1)
        image2 = self.ax1.imshow(self.substrate.model_array[-1], animated=True, cmap='Greys_r',
                                 vmin=0, vmax=config.settings['structure']['refractory_period'],
                                 origin = 'lower', alpha = 0.5, extent=(0, 200, 0, 200), interpolation='nearest',
                                 zorder=1)

        self.ax2 = self.figure.add_subplot(gs[1])
        crossim = self.ax2.imshow(np.swapaxes(self.substrate.model_array[:,:,config.settings['crosspos']], 0,1), animated=True,
                                  vmin=0, vmax=config.settings['structure']['refractory_period'],
                                  origin = 'lower', cmap='Greys_r', interpolation='nearest')

        def func(framedata):
            t, pause = framedata
            """Function to iterate animation over"""
            if t % config.settings['sim']['pacemaker_period'] == 0:
                self.substrate.activate_pacemaker()
            self.ax1.set_title('seed={}, t={}'.format(self.substrate.seed, t))
            if not pause:
                self.substrate.iterate()
            arr = self.get_anim_array()
            return [line.set_xdata(config.settings['crosspos']), image.set_data(arr[0]), image2.set_data(arr[-1]),
                    crossim.set_data(np.swapaxes(arr[:,:,config.settings['crosspos']], 0,1)),
                    ]

        def frames():
            t = -1
            while True:
                if not config.settings['pause']:
                    t += 1
                yield (t, config.settings['pause'])

        self.ani = FuncAnimation(self.figure, func, frames, interval=1, blit=False)

    def get_anim_array(self):
        method = config.settings['view']
        if method == 'activation':
            return self.substrate.model_array
        if method == 'count':
            return self.substrate.excount % 3 / 3 * config.settings['structure']['refractory_period']



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    af = AFInterface()
    af.show()
    sys.exit(app.exec_())
