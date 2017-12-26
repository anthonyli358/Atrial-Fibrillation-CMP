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
    """Atrial Fibrillation simulation class."""
    def __init__(self):
        super().__init__()
        self.settings = config.settings
        self.initUI()

    def initUI(self):

        self.settings['play'] = True
        self.settings['step'] = False
        self.settings['view'] = 'activation'
        self.setWindowIcon(QtGui.QIcon('icons8-heart-with-pulse-50.png'))
        self.anim = Animation(self)
        self.setCentralWidget(self.anim)

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
        playAct.setChecked(self.settings['play'])
        playAct.triggered.connect(self.toggle_pause)
        playAct.setShortcut('space')
        chartAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-heat-map-50.png'), 'chart', self)
        chartAct.triggered.connect(self.show_phase)
        settAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-settings-50.png'), 'settings', self)
        settAct.triggered.connect(self.show_config)
        resetAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-reset-50.png'), 'reset', self)
        resetAct.triggered.connect(self.reset)
        advAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-advance-50.png'), 'advance', self)
        advAct.triggered.connect(self.advance)
        self.toolbar.addActions([playAct, chartAct, settAct, resetAct, advAct])
        self.toolbar.setMaximumHeight(25)


        self.setGeometry(300,100,300,400)
        self.setWindowTitle('AF Viewer')

        self.show()

    def toggle_pause(self):

        self.settings['play'] ^= True  # Toggle play setting

    def show_config(self):
        self.popup = Config(self)
        self.popup.setWindowTitle('Config')
        self.popup.show()

    def show_phase(self):
        self.popup = makePhases(self)
        self.popup.setWindowTitle('Phase Spaces')
        self.popup.show()

    def reset(self):
        if not config.settings['structure']['seed']:
            self.settings['structure']['seed'] = None
        self.anim.close_event()  # Ends Current animation
        self.anim = Animation(self)  # Overrites animation with new one
        self.setCentralWidget(self.anim)  # Replaces animation with new one

    def advance(self):
        self.settings['step'] = True




class Config(QtWidgets.QWidget):
    """Edit system settings"""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = parent.settings
        self.setWindowIcon(QtGui.QIcon('icons8-settings-50.png'))
        self.sizeq= QtWidgets.QLineEdit(str(self.settings['structure']['size']))
        self.setWindowTitle('Configuration Settings')
        self.initUI()

    def initUI(self):

        config_form = QtWidgets.QFormLayout()

        x_dim = QtWidgets.QSpinBox()
        y_dim = QtWidgets.QSpinBox()
        z_dim = QtWidgets.QSpinBox()
        x_dim.setRange(1,999)
        y_dim.setRange(1,999)
        z_dim.setRange(1,999)
        x_dim.setValue(self.settings['structure']['size'][2])
        y_dim.setValue(self.settings['structure']['size'][1])
        z_dim.setValue(self.settings['structure']['size'][0])
        x_dim.valueChanged.connect(self.update_x_dim)
        y_dim.valueChanged.connect(self.update_y_dim)
        z_dim.valueChanged.connect(self.update_z_dim)
        xyz_dim = QtWidgets.QHBoxLayout()
        xyz_dim.addWidget(QtWidgets.QLabel('x:'))
        xyz_dim.addWidget(x_dim)
        xyz_dim.addWidget(QtWidgets.QLabel('y:'))
        xyz_dim.addWidget(y_dim)
        xyz_dim.addWidget(QtWidgets.QLabel('z:'))
        xyz_dim.addWidget(z_dim)

        config_form.addRow(QtWidgets.QLabel('Dimensions'), xyz_dim)

        x_linkage = QtWidgets.QDoubleSpinBox()
        y_linkage = QtWidgets.QDoubleSpinBox()
        z_linkage = QtWidgets.QDoubleSpinBox()
        x_linkage.setDecimals(3)
        y_linkage.setDecimals(3)
        z_linkage.setDecimals(3)
        x_linkage.setRange(0.00, 1.00)
        y_linkage.setRange(0, 1)
        z_linkage.setRange(0, 1)
        x_linkage.setSingleStep(0.01)
        y_linkage.setSingleStep(0.01)
        z_linkage.setSingleStep(0.01)
        x_linkage.setValue(self.settings['structure']['x_coupling'])
        y_linkage.setValue(self.settings['structure']['y_coupling'])
        z_linkage.setValue(self.settings['structure']['z_coupling'])
        x_linkage.valueChanged.connect(self.update_x_linkage)
        y_linkage.valueChanged.connect(self.update_y_linkage)
        z_linkage.valueChanged.connect(self.update_z_linkage)

        xyz_linkage = QtWidgets.QHBoxLayout()
        xyz_linkage.addWidget(QtWidgets.QLabel('x:'))
        xyz_linkage.addWidget(x_linkage)
        xyz_linkage.addWidget(QtWidgets.QLabel('y:'))
        xyz_linkage.addWidget(y_linkage)
        xyz_linkage.addWidget(QtWidgets.QLabel('z:'))
        xyz_linkage.addWidget(z_linkage)

        config_form.addRow(QtWidgets.QLabel('Linkage'), xyz_linkage)

        refractoryBox = QtWidgets.QSpinBox()
        refractoryBox.setRange(1, 999)
        refractoryBox.setValue(self.settings['structure']['refractory_period'])
        refractoryBox.valueChanged.connect(self.update_refractory)
        config_form.addRow(QtWidgets.QLabel('Refractory Period'), refractoryBox)

        reset_button = QtWidgets.QPushButton()
        reset_button.setText('Reset with these settings')
        reset_button.pressed.connect(self.parent.reset)

        config_form.addWidget(reset_button)

        config_box = QtWidgets.QGroupBox()
        config_box.setTitle('Substrate Configuration Settings')
        config_box.setLayout(config_form)

        anim_form = QtWidgets.QFormLayout()
        viewopts = QtWidgets.QComboBox()
        viewopts.addItems(['activation', 'count'])
        viewopts.currentTextChanged.connect(self.updateview)
        anim_form.addRow(QtWidgets.QLabel('Animation Style'), viewopts)

        crosspos_slider = QtWidgets.QSlider(Qt.Horizontal)
        crosspos_spin = QtWidgets.QSpinBox()

        crosspos_slider.setValue(self.settings['crosspos'])
        crosspos_spin.setValue(self.settings['crosspos'])
        crosspos_slider.setRange(0, self.settings['structure']['size'][1]-1)
        crosspos_spin.setRange(0, self.settings['structure']['size'][1]-1)
        crosspos_slider.valueChanged.connect(crosspos_spin.setValue)  # Connect slider to spin boc
        crosspos_spin.valueChanged.connect(crosspos_slider.setValue)  # Connect spin box to slider
        crosspos_slider.valueChanged.connect(self.updatecrosspos)  # Connect slider to position updater
        crosspos_spin.valueChanged.connect(self.updatecrosspos)  # Connect spin box to position updater

        crosspos = QtWidgets.QHBoxLayout()
        crosspos.addWidget(crosspos_spin)
        crosspos.addWidget(crosspos_slider)
        anim_form.addRow(QtWidgets.QLabel('Cross view position'), crosspos)

        anim_box = QtWidgets.QGroupBox()
        anim_box.setTitle('Animation Settings')
        anim_box.setLayout(anim_form)

        box_list = QtWidgets.QVBoxLayout()

        box_list.addWidget(config_box)
        box_list.addWidget(anim_box)

        self.setLayout(box_list)

    # ToDo: Change slider range when size is changed

    def update_x_dim(self, val):
        self.settings['structure']['size'][2] = val

    def update_y_dim(self, val):
        self.settings['structure']['size'][1] = val

    def update_z_dim(self, val):
        self.settings['structure']['size'][0] = val

    def update_x_linkage(self, val):
        self.settings['structure']['x_coupling'] = val

    def update_y_linkage(self, val):
        self.settings['structure']['y_coupling'] = val

    def update_z_linkage(self, val):
        self.settings['structure']['z_coupling'] = val

    def update_refractory(self, val):
        self.settings['structure']['refractory_period'] = val


    def updateview(self, val):
        self.settings['view'] = val

    def updatecrosspos(self, val):
        self.settings['crosspos'] = val


class makeCanvas(FigureCanvas):
    """Parent class of all Canvases. Initiate a figure with a toolbar."""
    def __init__(self, parent):
        self.figure = Figure(dpi=50)
        super().__init__(self.figure)
        self.settings = parent.settings
        self.compute_initial_figure()

        self.toolbar = NavigationToolbar(self, self)

    def compute_initial_figure(self):
        pass


class makePhases(makeCanvas):
    """Window containing figures of risk for different substrates."""

    def compute_initial_figure(self):
        self.resize(400,350)
        self.step = False
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
    """Window with real-time Atrial Fibrillation animation."""
    def compute_initial_figure(self):
        self.substrate = model.Model(**self.settings['structure'])

        gs = GridSpec(1, 2, width_ratios=self.settings['structure']['size'][-2::-1])

        self.ax1 = self.figure.add_subplot(gs[0])
        line = self.ax1.axvline(x=self.settings['crosspos'],
                                color='cyan',
                                linestyle='--'
                                )
        image = self.ax1.imshow(self.substrate.model_array[0],
                                animated=True,
                                cmap='Oranges_r',
                                vmin=0,
                                vmax=self.settings['structure']['refractory_period'],
                                origin = 'lower',
                                alpha=1,
                                extent=(0, self.settings['structure']['size'][2],
                                        0, self.settings['structure']['size'][1]),
                                interpolation='nearest',
                                zorder=1,
                                )
        image2 = self.ax1.imshow(self.substrate.model_array[-1],
                                 animated=True,
                                 cmap='Greys_r',
                                 vmin=0,
                                 vmax=self.settings['structure']['refractory_period'],
                                 origin = 'lower',
                                 alpha = 0.5,
                                 extent=(0, self.settings['structure']['size'][2],
                                         0, self.settings['structure']['size'][1]),
                                 interpolation='nearest',
                                 zorder=1

                                 )

        self.ax2 = self.figure.add_subplot(gs[1])
        crossim = self.ax2.imshow(np.swapaxes(self.substrate.model_array[:,:,self.settings['crosspos']], 0,1),
                                  animated=True,
                                  vmin=0,
                                  vmax=self.settings['structure']['refractory_period'],
                                  origin='lower',
                                  cmap='Greys_r',
                                  interpolation='nearest',
                                  extent=(0, self.settings['structure']['size'][0],
                                          0, self.settings['structure']['size'][1])
                                  )

        def func(framedata):
            t, play = framedata
            """Function to iterate animation over"""
            if t % self.settings['sim']['pacemaker_period'] == 0:
                self.substrate.activate_pacemaker()
            self.ax1.set_title('seed={}, t={}'.format(self.substrate.seed, t))
            if play:
                self.substrate.iterate()
            arr = self.get_anim_array()
            return [line.set_xdata(self.settings['crosspos']),
                    image.set_data(arr[0]),
                    image2.set_data(arr[-1]),
                    crossim.set_data(np.swapaxes(arr[:,:,self.settings['crosspos']], 0,1)),
                    ]

        def frames():
            t = -1
            while True:
                advanced = False
                if self.settings['play'] or self.settings['step']:
                    self.settings['step'] = False  # enable one timestep only while paused
                    advanced = True  # let substrate iterate
                    t += 1
                yield (t, advanced)


        self.ani = FuncAnimation(self.figure, func, frames, interval=1, blit=False)

    def get_anim_array(self):
        method = self.settings['view']
        if method == 'activation':
            return self.substrate.model_array
        if method == 'count':
            return self.substrate.excount % 3 / 3 * self.settings['structure']['refractory_period']





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    af = AFInterface()
    af.show()
    sys.exit(app.exec_())
