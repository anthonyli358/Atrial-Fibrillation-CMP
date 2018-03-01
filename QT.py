import sys
from PyQt5 import QtWidgets, QtGui

from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
import numpy as np
from pprint import pprint  # to get readable print output for dicts

import model
import config


class AFInterface(QtWidgets.QMainWindow):
    """Atrial Fibrillation simulation class."""
    def __init__(self):
        super().__init__()
        self.settings = config.settings
        self.config = Config(self)
        self.initUI()

    def initUI(self):

        self.settings['play'] = True
        self.settings['step'] = False
        self.settings['view'] = 'activation'
        self.setWindowIcon(QtGui.QIcon('icons8-heart-with-pulse-50.png'))
        self.anim = Animation(self)
        self.setCentralWidget(self.anim)

        # Defining UI actions
        settAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-settings-50.png'), 'settings', self)
        settAct.triggered.connect(self.show_config)

        phaseAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-heat-map-50.png'), 'View &Phase spaces', self)
        phaseAct.triggered.connect(self.show_phase)

        playAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-play-50.png'), 'play', self)
        playAct.setCheckable(True)
        playAct.setChecked(self.settings['play'])
        playAct.triggered.connect(self.toggle_pause)
        playAct.setShortcut('space')  # Pressing space bar will toggle pause

        resetAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-reset-50.png'), 'reset', self)
        resetAct.triggered.connect(self.reset)

        advAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-advance-50.png'), 'advance', self)
        advAct.triggered.connect(self.advance)
        advAct.setShortcut('return')

        # Creating menu bar
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(settAct)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(phaseAct)

        # Adding animation toolbar
        self.toolbar = self.addToolBar('Animation')
        self.toolbar.addActions([playAct, phaseAct, settAct, resetAct, advAct])
        self.toolbar.setMaximumHeight(25)

        self.setGeometry(300, 100, 300, 400)
        self.setWindowTitle('AF Viewer')

        self.show()

    def toggle_pause(self):

        self.settings['play'] ^= True  # Toggle play setting

    def show_config(self):
        # self.config = Config(self)
        self.config.show()

    def show_phase(self):
        self.popup = makePhases(self)
        self.popup.setWindowTitle('Phase Spaces')
        self.popup.show()

    def reset(self):
        if not config.settings['structure']['seed']:
            self.settings['structure']['seed'] = None
        self.anim.close_event()  # Ends Current animation
        self.anim = Animation(self)  # Overwrites animation with new one
        self.setCentralWidget(self.anim)  # Replaces animation with new one
        print('\n\n New Settings \n')
        pprint(self.settings)

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

        refractoryBox = QtWidgets.QSpinBox()
        refractoryBox.setRange(1, 999)
        refractoryBox.setValue(self.settings['structure']['refractory_period'])
        refractoryBox.valueChanged.connect(self.update_refractory)

        dysfunction = QtWidgets.QDoubleSpinBox()
        dysfunction.setDecimals(3)
        dysfunction.setRange(0, 1)
        dysfunction.setSingleStep(0.005)
        dysfunction.setValue(self.settings['structure']['dysfunction_parameter'])
        dysfunction.valueChanged.connect(self.update_dysfunctional_param)

        dysfunction_p = QtWidgets.QDoubleSpinBox()
        dysfunction_p.setDecimals(3)
        dysfunction_p.setRange(0, 1)
        dysfunction_p.setSingleStep(0.005)
        dysfunction_p.setValue(self.settings['structure']['dysfunction_probability'])
        dysfunction_p.valueChanged.connect(self.update_dysfunctional_prob)

        reset_button = QtWidgets.QPushButton()
        reset_button.setText('Reset with these settings')
        reset_button.pressed.connect(self.parent.reset)

        viewopts = QtWidgets.QComboBox()
        viewopts.addItems(['activation', 'count', 'direction'])
        viewopts.currentTextChanged.connect(self.updateview)

        v_cross_pos_slider = QtWidgets.QSlider(Qt.Horizontal)
        v_cross_pos_spin = QtWidgets.QSpinBox()

        v_cross_pos_slider.setValue(self.settings['v_cross_pos'])
        v_cross_pos_spin.setValue(self.settings['v_cross_pos'])
        v_cross_pos_slider.setRange(0, self.settings['structure']['size'][1]-1)
        v_cross_pos_spin.setRange(0, self.settings['structure']['size'][1]-1)
        v_cross_pos_slider.valueChanged.connect(v_cross_pos_spin.setValue)  # Connect slider to spin boc
        v_cross_pos_spin.valueChanged.connect(v_cross_pos_slider.setValue)  # Connect spin box to slider
        v_cross_pos_slider.valueChanged.connect(self.update_v_cross_pos)  # Connect slider to position updater
        v_cross_pos_spin.valueChanged.connect(self.update_v_cross_pos)  # Connect spin box to position updater

        h_cross_pos_slider = QtWidgets.QSlider(Qt.Horizontal)
        h_cross_pos_spin = QtWidgets.QSpinBox()

        h_cross_pos_slider.setValue(self.settings['h_cross_pos'])
        h_cross_pos_spin.setValue(self.settings['h_cross_pos'])
        h_cross_pos_slider.setRange(0, self.settings['structure']['size'][2]-1)
        h_cross_pos_spin.setRange(0, self.settings['structure']['size'][2]-1)
        h_cross_pos_slider.valueChanged.connect(h_cross_pos_spin.setValue)  # Connect slider to spin boc
        h_cross_pos_spin.valueChanged.connect(h_cross_pos_slider.setValue)  # Connect spin box to slider
        h_cross_pos_slider.valueChanged.connect(self.update_h_cross_pos)  # Connect slider to position updater
        h_cross_pos_spin.valueChanged.connect(self.update_h_cross_pos)  # Connect spin box to position updater

        w_cross_pos_slider = QtWidgets.QSlider(Qt.Horizontal)
        w_cross_pos_spin = QtWidgets.QSpinBox()

        w_cross_pos_slider.setValue(self.settings['w_cross_pos'])
        w_cross_pos_spin.setValue(self.settings['w_cross_pos'])
        w_cross_pos_slider.setRange(0, self.settings['structure']['size'][0]-1)
        w_cross_pos_spin.setRange(0, self.settings['structure']['size'][0]-1)
        w_cross_pos_slider.valueChanged.connect(w_cross_pos_spin.setValue)  # Connect slider to spin boc
        w_cross_pos_spin.valueChanged.connect(w_cross_pos_slider.setValue)  # Connect spin box to slider
        w_cross_pos_slider.valueChanged.connect(self.update_w_cross_pos)  # Connect slider to position updater
        w_cross_pos_spin.valueChanged.connect(self.update_w_cross_pos)  # Connect spin box to position updater

        cross_pos = QtWidgets.QHBoxLayout()
        cross_pos.addWidget(v_cross_pos_spin)
        cross_pos.addWidget(v_cross_pos_slider)
        cross_pos2 = QtWidgets.QHBoxLayout()
        cross_pos2.addWidget(h_cross_pos_spin)
        cross_pos2.addWidget(h_cross_pos_slider)
        cross_pos3 = QtWidgets.QHBoxLayout()
        cross_pos3.addWidget(w_cross_pos_spin)
        cross_pos3.addWidget(w_cross_pos_slider)

        config_box = QtWidgets.QGroupBox()
        config_box.setTitle('Substrate Configuration Settings')

        config_form = QtWidgets.QFormLayout()
        config_form.addRow(QtWidgets.QLabel('Dimensions'), xyz_dim)
        config_form.addRow(QtWidgets.QLabel('Linkage'), xyz_linkage)
        config_form.addRow(QtWidgets.QLabel('Refractory Period'), refractoryBox)
        config_form.addRow(QtWidgets.QLabel('Dysfunctional cells'), dysfunction)
        config_form.addRow(QtWidgets.QLabel('Dysfunctional Probability'), dysfunction_p)
        config_form.addWidget(reset_button)

        config_box.setLayout(config_form)

        anim_box = QtWidgets.QGroupBox()
        anim_box.setTitle('Animation Settings')

        anim_form = QtWidgets.QFormLayout()
        anim_form.addRow(QtWidgets.QLabel('Animation Style'), viewopts)
        anim_form.addRow(QtWidgets.QLabel('Vertical cross view position'), cross_pos)
        anim_form.addRow(QtWidgets.QLabel('Horizontal cross view position'), cross_pos2)
        anim_form.addRow(QtWidgets.QLabel('Inline cross view position'), cross_pos3)
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

    def update_dysfunctional_param(self, val):
        self.settings['structure']['dysfunction_parameter'] = val

    def update_dysfunctional_prob(self, val):
        self.settings['structure']['dysfunction_probability'] = val

    def updateview(self, val):
        self.settings['view'] = val

    def update_v_cross_pos(self, val):
        self.settings['v_cross_pos'] = val

    def update_h_cross_pos(self, val):
        self.settings['h_cross_pos'] = val

    def update_w_cross_pos(self, val):
        self.settings['w_cross_pos'] = val


class makeCanvas(FigureCanvas):
    """Parent class of all Canvases. Initiate a figure with a toolbar."""
    def __init__(self, parent):
        self.parent = parent
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
        self.resize(400, 350)
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
            ax.imshow(i, extent=(0, 1, 0, 1), origin='lower')


class Animation(makeCanvas):
    """Window with real-time Atrial Fibrillation animation."""
    def compute_initial_figure(self):
        size = self.settings['structure']['size']

        self.substrate = model.Model(**self.settings['structure'])

        gs = GridSpec(3, 2,
                      width_ratios=[1, size[0]/size[1]],
                      height_ratios=[1, 1, size[0]/size[2]])

        self.ax0 = self.figure.add_subplot(gs[0])
        im = self.ax0.imshow(self.substrate.model_array[self.settings['w_cross_pos']],
                             animated=True,
                             cmap='Greys_r',
                             vmin=0,
                             vmax=self.settings['structure']['refractory_period'],
                             origin='lower',
                             alpha=1,
                             extent=(0, self.settings['structure']['size'][2],
                                     0, self.settings['structure']['size'][1]),
                             interpolation='nearest',
                             )

        self.ax1 = self.figure.add_subplot(gs[2])
        clicked = self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        linev = self.ax1.axvline(x=self.settings['v_cross_pos'],
                                 color='cyan',
                                 linestyle='--'
                                 )
        lineh = self.ax1.axhline(y=self.settings['h_cross_pos'],
                                 color='cyan',
                                 linestyle='--'
                                 )
        image = self.ax1.imshow(self.substrate.model_array[0],
                                animated=True,
                                cmap='Greys_r',
                                vmin=0,
                                vmax=self.settings['structure']['refractory_period'],
                                origin='lower',
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
                                 origin='lower',
                                 alpha=0.5,
                                 extent=(0, self.settings['structure']['size'][2],
                                         0, self.settings['structure']['size'][1]),
                                 interpolation='nearest',
                                 zorder=1

                                 )

        self.ax2 = self.figure.add_subplot(gs[3])
        v_cross_view = self.ax2.imshow(np.swapaxes(self.substrate.model_array[:, :, self.settings['v_cross_pos']],
                                                   0, 1),
                                       animated=True,
                                       vmin=0,
                                       vmax=self.settings['structure']['refractory_period'],
                                       origin='lower',
                                       cmap='Greys_r',
                                       interpolation='nearest',
                                       extent=(0, self.settings['structure']['size'][0],
                                               0, self.settings['structure']['size'][1])
                                       )

        self.ax3 = self.figure.add_subplot(gs[4])
        h_cross_view = self.ax3.imshow(self.substrate.model_array[:, self.settings['h_cross_pos'], :],
                                       animated=True,
                                       vmin=0,
                                       vmax=self.settings['structure']['refractory_period'],
                                       origin='lower',
                                       cmap='Greys_r',
                                       interpolation='nearest',
                                       extent=(0, self.settings['structure']['size'][2],
                                               0, self.settings['structure']['size'][0])
                                       )

        def func(framedata):
            t, play = framedata
            """Function to iterate animation over"""
            if t % self.settings['sim']['pacemaker_period'] == 0:
                self.substrate.activate_pacemaker()
            if play:
                self.substrate.iterate()
            if t == 300:
                self.substrate.add_ablation(self.substrate.maxpos, 2)
            arr = self.get_anim_array()

            self.ax1.set_title('seed={}, t={}, {}'.format(self.substrate.seed, t, self.substrate.maxpos))
            return [linev.set_xdata(self.settings['v_cross_pos']),
                    lineh.set_ydata(self.settings['h_cross_pos']),
                    im.set_data(arr[self.settings['w_cross_pos']]),
                    image.set_data(arr[0]),
                    image2.set_data(arr[-1]),
                    v_cross_view.set_data(np.swapaxes(arr[:, :, self.settings['v_cross_pos']], 0, 1)),
                    h_cross_view.set_data(arr[:, self.settings['h_cross_pos'], :])
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

    def onclick(self, event):
        if event.xdata:
            self.parent.config.update_v_cross_pos(int(event.xdata))
            self.parent.config.update_h_cross_pos(int(event.ydata))

    def get_anim_array(self):
        method = self.settings['view']
        if method == 'activation':
            return self.substrate.model_array
        if method == 'count':
            return self.substrate.excount % 3 / 3 * self.settings['structure']['refractory_period']
        if method == 'direction':
            return (5 + self.substrate.direction)/10 * self.settings['structure']['refractory_period']


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    af = AFInterface()
    af.show()
    sys.exit(app.exec_())
