import sys
from PyQt5 import QtWidgets, QtGui

from PyQt5.QtCore import Qt
from matplotlib import rcParams
# rcParams['animation.ffmpeg_path'] = "/Users/andrew/Downloads/ffmpeg-4.0.1/ffmpeg.exe"
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
import skimage.morphology as morph
import skimage.restoration as rest

import numpy as np
from pprint import pprint  # to get readable print output for dicts

import model
import config
import copy
import queue
import scipy.ndimage as spim


class AFInterface(QtWidgets.QMainWindow):
    """Parent class for interface. Defines menu options and button interactions.
    Atrial Fibrillation simulation class."""

    def __init__(self):
        super().__init__()
        self.settings = config.settings
        self.initUI()
        self.config = Config(self)

    def initUI(self):

        self.settings['play'] = True
        self.settings['step'] = False
        self.settings['view'] = 'activation'
        self.settings['skip'] = False
        self.settings['ablate'] = False
        self.settings['abradius'] = 2
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

        skipAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-end-32.png'), 'skip', self)
        skipAct.triggered.connect(self.skip)

        saveFile = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-save-as-50.png'), 'save', self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)

        self.ablateAct = QtWidgets.QAction(QtGui.QIcon('Icons/icons8-laser-beam-50.png'), 'ablate', self)
        self.ablateAct.setCheckable(True)
        self.ablateAct.setChecked(self.settings['ablate'])
        self.ablateAct.triggered.connect(self.ablate)

        # Creating menu bar
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(settAct)

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(phaseAct)

        # Adding animation toolbar
        self.toolbar = self.addToolBar('Animation')
        self.toolbar.addActions([playAct, phaseAct, settAct, resetAct, advAct, skipAct, saveFile, self.ablateAct])
        self.toolbar.setMaximumHeight(25)

        self.setGeometry(300, 150, 400, 680)
        self.setWindowTitle('AF Viewer')

        self.show()

    def toggle_pause(self):

        self.settings['play'] ^= True  # Toggle play setting

    def skip(self):
        self.settings['skip'] = True

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
        if self.config.seedCheck.isChecked():
            self.settings['structure']['seed'] = np.uint32(self.config.seedBox.text())
        else:
            self.settings['structure']['seed'] = None
        if self.config.dys_seedCheck.isChecked():
            self.settings['structure']['dys_seed'] = np.uint32(self.config.dys_seedBox.text())
        else:
            self.settings['structure']['dys_seed'] = None
        self.anim.close_event()  # Ends Current animation
        self.anim = Animation(self)  # Overwrites animation with new one
        self.setCentralWidget(self.anim)  # Replaces animation with new one
        self.config.seedBox.setText(np.str(self.anim.substrate.seed))
        self.config.dys_seedBox.setText(np.str(self.anim.substrate.dys_seed))
        print('\n\n New Settings \n')
        pprint(self.settings)

    def advance(self):
        self.settings['step'] = True

    def ablate(self):
        self.settings['ablate'] ^= True

    def file_save(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        print(name)
        anim2 = Animation(self)
        anim2.compute_initial_figure(recall=name[0] + '.mp4')
        try:
            anim2.close_event()
        except Exception:
            pass


class Config(QtWidgets.QWidget):
    """Configuration window class. Updates local version of config file.
    Can edit model settings without restarting interface"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = parent.settings
        self.setWindowIcon(QtGui.QIcon('icons8-settings-50.png'))
        self.sizeq = QtWidgets.QLineEdit(str(self.settings['structure']['size']))
        self.setWindowTitle('Configuration Settings')
        self.initUI()

    def initUI(self):
        x_dim = QtWidgets.QSpinBox()
        y_dim = QtWidgets.QSpinBox()
        z_dim = QtWidgets.QSpinBox()
        x_dim.setRange(1, 999)
        y_dim.setRange(1, 999)
        z_dim.setRange(1, 999)
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
        yz_linkage = QtWidgets.QDoubleSpinBox()

        x_linkage.setDecimals(3)
        yz_linkage.setDecimals(3)

        x_linkage.setRange(0.00, 1.00)
        yz_linkage.setRange(0, 1)

        x_linkage.setSingleStep(0.01)
        yz_linkage.setSingleStep(0.01)

        x_linkage.setValue(self.settings['structure']['x_coupling'])
        yz_linkage.setValue(self.settings['structure']['yz_coupling'])

        x_linkage.valueChanged.connect(self.update_x_linkage)
        yz_linkage.valueChanged.connect(self.update_yz_linkage)

        xyz_linkage = QtWidgets.QHBoxLayout()
        xyz_linkage.addWidget(QtWidgets.QLabel('x:'))
        xyz_linkage.addWidget(x_linkage)
        xyz_linkage.addWidget(QtWidgets.QLabel('yz:'))
        xyz_linkage.addWidget(yz_linkage)

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

        self.seedCheck = QtWidgets.QCheckBox()
        self.seedCheck.setCheckState(0)

        self.seedBox = QtWidgets.QLineEdit()
        validator = QtGui.QIntValidator(0, 4294967295)
        self.seedBox.setValidator(validator)
        self.seedBox.setText(np.str(self.parent.anim.substrate.seed))

        self.dys_seedCheck = QtWidgets.QCheckBox()
        self.dys_seedCheck.setCheckState(0)

        self.dys_seedBox = QtWidgets.QLineEdit()
        validator = QtGui.QIntValidator(0, 4294967295)
        self.dys_seedBox.setValidator(validator)
        self.dys_seedBox.setText(np.str(self.parent.anim.substrate.dys_seed))

        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        toggle = QtWidgets.QCheckBox()
        toggle.setTristate(False)
        toggle.setCheckState(2 * self.settings['structure']['angle_toggle'])
        toggle.stateChanged.connect(self.update_toggle)

        angle0 = QtWidgets.QSpinBox()
        angle1 = QtWidgets.QSpinBox()

        angle0.setRange(0, 180)
        angle1.setRange(0, 180)

        angle0.setSingleStep(10)
        angle1.setSingleStep(10)

        angle0.setValue(self.settings['structure']['angle_vars'][0])
        angle1.setValue(self.settings['structure']['angle_vars'][1])

        angle0.valueChanged.connect(self.update_angle0)
        angle1.valueChanged.connect(self.update_angle1)

        angles = QtWidgets.QHBoxLayout()
        angles.addWidget(QtWidgets.QLabel('Angle at min z:'))
        angles.addWidget(angle0)
        angles.addWidget(QtWidgets.QLabel('Angle at max z:'))
        angles.addWidget(angle1)

        anglemag = QtWidgets.QDoubleSpinBox()
        anglemag.setDecimals(3)
        anglemag.setRange(0.00, 1.00)
        anglemag.setSingleStep(0.01)
        anglemag.setValue(self.settings['structure']['angle_vars'][2])
        anglemag.valueChanged.connect(self.update_anglemag)

        seedHBox = QtWidgets.QHBoxLayout()
        seedHBox.addWidget(self.seedCheck)
        seedHBox.addWidget(self.seedBox)

        dys_seedHBox = QtWidgets.QHBoxLayout()
        dys_seedHBox.addWidget(self.dys_seedCheck)
        dys_seedHBox.addWidget(self.dys_seedBox)

        reset_button = QtWidgets.QPushButton()
        reset_button.setText('Reset with these settings')
        reset_button.pressed.connect(self.parent.reset)

        viewopts = QtWidgets.QComboBox()
        viewopts.addItems(['activation', 'count', 'direction', 'max_filter', 'gauss_filter', 'maxgauss', 'expt'])
        viewopts.currentTextChanged.connect(self.updateview)

        v_cross_pos_slider = QtWidgets.QSlider(Qt.Horizontal)
        v_cross_pos_spin = QtWidgets.QSpinBox()

        v_cross_pos_slider.setValue(self.settings['QTviewer']['x_cross_pos'])
        v_cross_pos_spin.setValue(self.settings['QTviewer']['x_cross_pos'])
        v_cross_pos_slider.setRange(0, self.settings['structure']['size'][1] - 1)
        v_cross_pos_spin.setRange(0, self.settings['structure']['size'][1] - 1)
        v_cross_pos_slider.valueChanged.connect(v_cross_pos_spin.setValue)  # Connect slider to spin boc
        v_cross_pos_spin.valueChanged.connect(v_cross_pos_slider.setValue)  # Connect spin box to slider
        v_cross_pos_slider.valueChanged.connect(self.update_v_cross_pos)  # Connect slider to position updater
        v_cross_pos_spin.valueChanged.connect(self.update_v_cross_pos)  # Connect spin box to position updater

        h_cross_pos_slider = QtWidgets.QSlider(Qt.Horizontal)
        h_cross_pos_spin = QtWidgets.QSpinBox()

        h_cross_pos_slider.setValue(self.settings['QTviewer']['y_cross_pos'])
        h_cross_pos_spin.setValue(self.settings['QTviewer']['y_cross_pos'])
        h_cross_pos_slider.setRange(0, self.settings['structure']['size'][2] - 1)
        h_cross_pos_spin.setRange(0, self.settings['structure']['size'][2] - 1)
        h_cross_pos_slider.valueChanged.connect(h_cross_pos_spin.setValue)  # Connect slider to spin boc
        h_cross_pos_spin.valueChanged.connect(h_cross_pos_slider.setValue)  # Connect spin box to slider
        h_cross_pos_slider.valueChanged.connect(self.update_h_cross_pos)  # Connect slider to position updater
        h_cross_pos_spin.valueChanged.connect(self.update_h_cross_pos)  # Connect spin box to position updater

        w_cross_pos_slider = QtWidgets.QSlider(Qt.Horizontal)
        w_cross_pos_spin = QtWidgets.QSpinBox()

        w_cross_pos_slider.setValue(self.settings['QTviewer']['z_cross_pos'])
        w_cross_pos_spin.setValue(self.settings['QTviewer']['z_cross_pos'])
        w_cross_pos_slider.setRange(0, self.settings['structure']['size'][0] - 1)
        w_cross_pos_spin.setRange(0, self.settings['structure']['size'][0] - 1)
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

        skipCheck = QtWidgets.QPushButton()
        skipCheck.setText('Skip')
        skipCheck.pressed.connect(self.parent.skip)

        angle0.setSingleStep(10)
        angle1.setSingleStep(10)

        angle0.setValue(self.settings['structure']['angle_vars'][0])
        angle1.setValue(self.settings['structure']['angle_vars'][1])

        angle0.valueChanged.connect(self.update_angle0)
        angle1.valueChanged.connect(self.update_angle1)

        angles = QtWidgets.QHBoxLayout()
        angles.addWidget(QtWidgets.QLabel('Angle at min z:'))
        angles.addWidget(angle0)
        angles.addWidget(QtWidgets.QLabel('Angle at max z:'))
        angles.addWidget(angle1)

        anglemag = QtWidgets.QDoubleSpinBox()
        anglemag.setDecimals(3)
        anglemag.setRange(0.00, 1.00)
        anglemag.setSingleStep(0.01)
        anglemag.setValue(self.settings['structure']['angle_vars'][2])
        anglemag.valueChanged.connect(self.update_anglemag)

        self.ablationToggle = QtWidgets.QPushButton()
        self.ablationToggle.setText('Ablate')
        self.ablationToggle.setCheckable(True)
        self.ablationToggle.setChecked(self.settings['ablate'])
        self.ablationToggle.pressed.connect(self.parent.ablate)

        ablationradius = QtWidgets.QSpinBox()
        ablationradius.setRange(1, 999)
        ablationradius.setValue(self.settings['abradius'])
        ablationradius.valueChanged.connect(self.update_abradius)

        config_box = QtWidgets.QGroupBox()
        config_box.setTitle('Substrate Configuration Settings')

        config_form = QtWidgets.QFormLayout()
        config_form.addRow(QtWidgets.QLabel('Dimensions'), xyz_dim)
        config_form.addRow(QtWidgets.QLabel('Linkage'), xyz_linkage)
        config_form.addRow(QtWidgets.QLabel('Refractory Period'), refractoryBox)
        config_form.addRow(QtWidgets.QLabel('Dysfunctional cells'), dysfunction)
        config_form.addRow(QtWidgets.QLabel('Dysfunctional Probability'), dysfunction_p)
        config_form.addWidget(separator)
        config_form.addRow(QtWidgets.QLabel('Toggle angle'), toggle)
        config_form.addRow(QtWidgets.QLabel('Angles'), angles)
        config_form.addRow(QtWidgets.QLabel('Average connectivity'), anglemag)

        config_form.addRow(QtWidgets.QLabel('Seed'), seedHBox)
        config_form.addRow(QtWidgets.QLabel('Dysfunction Seed'), dys_seedHBox)
        config_form.addWidget(reset_button)

        config_box.setLayout(config_form)

        anim_box = QtWidgets.QGroupBox()
        anim_box.setTitle('Animation Settings')

        anim_form = QtWidgets.QFormLayout()
        anim_form.addRow(QtWidgets.QLabel('Animation Style'), viewopts)
        anim_form.addRow(QtWidgets.QLabel('Vertical cross view position'), cross_pos)
        anim_form.addRow(QtWidgets.QLabel('Horizontal cross view position'), cross_pos2)

        anim_form.addRow(QtWidgets.QLabel('Depth cross view position'), cross_pos3)
        anim_form.addRow(QtWidgets.QLabel('Skip to breakthrough'), skipCheck)
        anim_box.setLayout(anim_form)

        ablation_box = QtWidgets.QGroupBox()
        ablation_box.setTitle('Ablation Settings')
        ablation_form = QtWidgets.QFormLayout()
        ablation_form.addRow(QtWidgets.QLabel('Ablate on click'), self.ablationToggle)
        ablation_form.addRow(QtWidgets.QLabel('Ablation radius (mm, 1 layer is 0.1mm thick)'), ablationradius)
        ablation_box.setLayout(ablation_form)

        box_list = QtWidgets.QVBoxLayout()
        box_list.addWidget(config_box)
        box_list.addWidget(anim_box)
        box_list.addWidget(ablation_box)

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

    def update_yz_linkage(self, val):
        self.settings['structure']['yz_coupling'] = val

    def update_refractory(self, val):
        self.settings['structure']['refractory_period'] = val

    def update_dysfunctional_param(self, val):
        self.settings['structure']['dysfunction_parameter'] = val

    def update_dysfunctional_prob(self, val):
        self.settings['structure']['dysfunction_probability'] = val

    def updateview(self, val):
        self.settings['view'] = val

    def update_v_cross_pos(self, val):
        self.settings['QTviewer']['x_cross_pos'] = val

    def update_h_cross_pos(self, val):
        self.settings['QTviewer']['y_cross_pos'] = val

    def update_w_cross_pos(self, val):
        self.settings['QTviewer']['z_cross_pos'] = val

    def update_toggle(self, val):
        self.settings['structure']['angle_toggle'] = val / 2

    def update_angle0(self, val):
        self.settings['structure']['angle_vars'][0] = val

    def update_angle1(self, val):
        self.settings['structure']['angle_vars'][1] = val

    def update_anglemag(self, val):
        self.settings['structure']['angle_vars'][2] = val

    def update_abradius(self, val):
        self.settings['abradius'] = val


class makeCanvas(FigureCanvas):
    """Parent class of all Canvases. Initiate a figure with a toolbar."""

    def __init__(self, parent):
        self.parent = parent
        self.figure = Figure()
        self.figure.set_size_inches(3.6, 6)
        super().__init__(self.figure)
        self.settings = parent.settings
        self.compute_initial_figure()

        self.toolbar = NavigationToolbar(self, self)

    def compute_initial_figure(self):
        pass


class makePhases(makeCanvas):
    """Class for window containing figures of risk for different substrates."""

    def compute_initial_figure(self):
        self.resize(400, 680)
        self.step = False
        names = ['data_analysis/phase_spaces/1_200_200.npy', 'data_analysis/phase_spaces/2_200_200.npy',
                 'data_analysis/phase_spaces/4_200_200.npy', 'data_analysis/phase_spaces/8_200_200.npy',
                 'data_analysis/phase_spaces/16_200_200.npy', 'data_analysis/phase_spaces/32_200_200.npy']
        compilation = []
        for i in names:
            compilation.append(np.load(i)[:, :, 2])

        for num, i in enumerate(compilation):
            ax = self.figure.add_subplot(200 + len(names) / 2 * 10 + 1 + num)
            ax.set_title(names[num][13:-4])
            ax.imshow(i, extent=(0, 1, 0, 1), origin='lower')


class Animation(makeCanvas):
    """Window with real-time Atrial Fibrillation animation."""

    def compute_initial_figure(self, recall=False):
        """Function to create figures"""
        # Sets initial plots and plot positions
        size = self.settings['structure']['size']
        # self.hist = queue.Queue(500)
        if not recall:
            self.hist = []
            self.substrate = model.Model(**self.settings['structure'])
            self.hist.append(copy.deepcopy(self.substrate))
        else:
            self.frozenhist = copy.copy(self.parent.anim.hist)
            self.i = 0
            self.substrate = self.frozenhist[self.i]

        # Transparent colourmaps if needed
        cm1 = LinearSegmentedColormap.from_list('100', [(0, 0, 0, 0), (1, 1, 1, 1)], N=50)
        cm2 = LinearSegmentedColormap.from_list('66', [(0, 0, 0, 0), (.5, .5, .5, 1)], N=50)
        cm3 = LinearSegmentedColormap.from_list('33', [(0, 0, 0, 1), (.25, .25, .25, 1)], N=50)

        cm1 = LinearSegmentedColormap.from_list('100', [(0, 0, 0, 0), (1, 1, 1, .6)], N=50)
        cm2 = LinearSegmentedColormap.from_list('66', [(0, 0, 0, 0), (1, .66, .5, .6)], N=50)
        cm3 = LinearSegmentedColormap.from_list('33', [(0, 0, 0, 1), (1, .33, .25, 1)], N=50)
        mastermap = 'jet'

        gs = GridSpec(3, 2,
                      width_ratios=[1, size[0] / size[1]],
                      height_ratios=[1, size[0] / size[2], 1])  # Setting grid layout for figures

        self.axtext = self.figure.add_subplot(gs[1])
        self.axtext.axis('off')
        if self.settings['structure']['angle_toggle']:
            s = '$\\theta_\mathrm{{min}} = {:.0f}$\n$\\theta_\mathrm{{max}} = {:.0f}$\n$\\nu_\mathrm{{ave}} = {:.3f}$'.format(
                *self.settings['structure']['angle_vars'])
        else:
            s = '$\\nu_x = {:.3f}$\n$\\nu_{{yz}}={:.3f}$'.format(self.substrate.nu_x,
                                                                 self.substrate.nu_yz)
        self.axtext.annotate(xy=(-0.8, 0.5), xycoords='axes fraction',
                             s=s)

        self.ax0 = self.figure.add_subplot(gs[4])
        self.im = self.ax0.imshow(self.substrate.model_array[self.settings['QTviewer']['z_cross_pos']],
                                  animated=True,
                                  cmap=mastermap,
                                  vmin=0,
                                  vmax=self.settings['structure']['refractory_period'],
                                  origin='lower',
                                  extent=(0, self.settings['structure']['size'][2],
                                          0, self.settings['structure']['size'][1]),
                                  interpolation='nearest',
                                  zorder=1
                                  )
        self.ax0.set_ylabel('y $(z={})$'.format(self.settings['QTviewer']['z_cross_pos']))
        self.ax0.set_xlabel('x')

        redmap = LinearSegmentedColormap.from_list('red', [(1, 0.2, 0.2, 0), (1, 0.2, 0.2, 1)], N=10)
        self.im_destroyed = self.ax0.imshow(self.substrate.destroyed[self.settings['QTviewer']['z_cross_pos']],
                                            animated=True,
                                            cmap=redmap,
                                            vmin=0,
                                            vmax=1,
                                            zorder=2,
                                            origin='lower',
                                            extent=(0, self.settings['structure']['size'][2],
                                                    0, self.settings['structure']['size'][1]),
                                            )
        # im2 = self.ax0.imshow(self.substrate.model_array[self.settings['QTviewer']['z_cross_pos']+1],
        #                          animated=True,
        #                          cmap=cm2,
        #                          vmin=0,
        #                          vmax=self.settings['structure']['refractory_period'],
        #                          origin='lower',
        #                          extent=(0, self.settings['structure']['size'][2],
        #                                  0, self.settings['structure']['size'][1]),
        #                          interpolation='nearest',
        #                          zorder=2
        #                          )
        # im3 = self.ax0.imshow(self.substrate.model_array[self.settings['QTviewer']['z_cross_pos']+2],
        #                          animated=True,
        #                          cmap=cm3,
        #                          vmin=0,
        #                          vmax=self.settings['structure']['refractory_period'],
        #                          origin='lower',
        #                          extent=(0, self.settings['structure']['size'][2],
        #                                  0, self.settings['structure']['size'][1]),
        #                          interpolation='nearest',
        #                          zorder=1
        #                          )

        self.linev = self.ax0.axvline(x=self.settings['QTviewer']['x_cross_pos'],
                                      color='cyan',
                                      linestyle='--',
                                      zorder=4,
                                      alpha=0
                                      )
        self.lineh = self.ax0.axhline(y=self.settings['QTviewer']['y_cross_pos'],
                                      color='cyan',
                                      linestyle='--',
                                      zorder=4,
                                      alpha=0
                                      )

        self.ax1 = self.figure.add_subplot(gs[0])
        clicked = self.figure.canvas.mpl_connect('button_press_event',
                                                 self.onclick)  # Clicking changes the cut through positions

        self.image = self.ax1.imshow(self.substrate.model_array[-1],  # View bottom layer
                                     animated=True,
                                     cmap=mastermap,
                                     vmin=0,
                                     vmax=self.settings['structure']['refractory_period'],
                                     origin='lower',
                                     extent=(0, size[2],
                                             0, size[1]),
                                     interpolation='nearest',
                                     zorder=3,
                                     )
        self.image_destroyed = self.ax1.imshow(self.substrate.destroyed[-1],  # View bottom layer
                                               animated=True,
                                               cmap=redmap,
                                               vmin=0,
                                               vmax=1,
                                               origin='lower',
                                               extent=(0, size[2],
                                                       0, size[1]),
                                               interpolation='nearest',
                                               zorder=4
                                               )
        self.ax1.set_ylabel('y $(z={})$'.format(size[0] - 1))
        self.ax1.get_xaxis().set_visible(False)

        # image2 = self.ax1.imshow(self.substrate.model_array[-2],
        #                          animated=True,
        #                          cmap=cm2,
        #                          vmin=0,
        #                          vmax=self.settings['structure']['refractory_period'],
        #                          origin='lower',
        #                          extent=(0, self.settings['structure']['size'][2],
        #                                  0, self.settings['structure']['size'][1]),
        #                          interpolation='nearest',
        #                          zorder=2
        #                          )
        # image3 = self.ax1.imshow(self.substrate.model_array[-3],
        #                          animated=True,
        #                          cmap=cm3,
        #                          vmin=0,
        #                          vmax=self.settings['structure']['refractory_period'],
        #                          origin='lower',
        #                          extent=(0, self.settings['structure']['size'][2],
        #                                  0, self.settings['structure']['size'][1]),
        #                          interpolation='nearest',
        #                          zorder=1
        #                          )

        # contour = self.ax1.contour(self.substrate.model_array[0],
        #                            animated=True,
        #                            zorder=5,
        #                            levels=[50])

        self.ax2 = self.figure.add_subplot(gs[5])  # Plot the x axis cut through
        self.ax2.set_xlabel('z $(x={})$'.format(self.settings['QTviewer']['x_cross_pos']))
        self.ax2.get_yaxis().set_visible(False)

        self.v_cross_view = self.ax2.imshow(np.swapaxes(self.substrate.model_array[:, :,
                                                        self.settings['QTviewer']['x_cross_pos']], 0, 1),
                                            animated=True,
                                            vmin=0,
                                            vmax=self.settings['structure']['refractory_period'],
                                            origin='lower',
                                            cmap=mastermap,
                                            interpolation='nearest',
                                            extent=(0, size[0],
                                                    0, size[1]),
                                            zorder=1,
                                            )

        self.v_cross_destroyed = self.ax2.imshow(np.swapaxes(self.substrate.destroyed[:, :,
                                                             self.settings['QTviewer']['x_cross_pos']], 0, 1),
                                                 animated=True,
                                                 origin='lower',
                                                 cmap=redmap,
                                                 vmin=0,
                                                 vmax=1,
                                                 interpolation='nearest',
                                                 extent=(0, self.settings['structure']['size'][0],
                                                         0, self.settings['structure']['size'][1]),
                                                 zorder=2
                                                 )

        self.ax3 = self.figure.add_subplot(gs[2])  # Plot the y axis cut through
        self.ax3.set_ylabel('z $(y={})$'.format(self.settings['QTviewer']['y_cross_pos']))
        self.ax3.get_xaxis().set_visible(False)
        self.h_cross_view = self.ax3.imshow(self.substrate.model_array[:, self.settings['QTviewer']['y_cross_pos'], :],
                                            animated=True,
                                            vmin=0,
                                            vmax=self.settings['structure']['refractory_period'],
                                            origin='lower',
                                            cmap=mastermap,
                                            interpolation='nearest',
                                            extent=(0, self.settings['structure']['size'][2],
                                                    0, self.settings['structure']['size'][0]),
                                            zorder=1
                                            )

        self.h_cross_destroyed = self.ax3.imshow(
            self.substrate.destroyed[:, self.settings['QTviewer']['y_cross_pos'], :],
            animated=True,
            origin='lower',
            cmap=redmap,
            vmin=0,
            vmax=1,
            interpolation='nearest',
            extent=(0, self.settings['structure']['size'][2],
                    0, self.settings['structure']['size'][0]),
            zorder=2
        )

        def func(framedata):
            """Function to iterate animation, All active changes here"""
            t, play = framedata
            if not recall:
                if self.substrate.time % self.settings['sim']['pacemaker_period'] == 0:
                    self.substrate.activate_pacemaker()
                if play:  # If viewer is not paused iterate each timestep.
                    self.substrate.iterate()  # advance simulation
                    self.hist.append(copy.deepcopy(self.substrate))
                # if t == 300:
                #     self.substrate.add_ablation(self.substrate.maxpos, 2)
                # if t == 1:
                #     self.substrate.add_ablation((0,100,100), 2)

                if self.settings['skip']:  # Skip without iterating animation
                    jumps = 0
                    while self.substrate.maxpos[-1] <= 1 and jumps < 1000:
                        if self.substrate.time % self.settings['sim']['pacemaker_period'] == 0:
                            self.substrate.activate_pacemaker()
                        self.substrate.iterate()
                        # self.hist.append(self.substrate.model_array.copy())
                        jumps += 1

                    self.settings['skip'] = False
                    self.parent.toggle_pause()
                    print(jumps)
            else:
                try:
                    self.i += 1
                    print(self.i)
                    self.substrate = self.frozenhist[self.i]
                    print(self.substrate.time)
                except:
                    return

            self.figure.suptitle(
                'seed={}, t={}, {}'.format(self.substrate.seed, self.substrate.time, self.substrate.maxpos), y=.03)
            self.ax0.set_ylabel('y $(z={})$'.format(self.settings['QTviewer']['z_cross_pos']))
            self.ax2.set_xlabel('z $(x={})$'.format(self.settings['QTviewer']['x_cross_pos']))
            self.ax3.set_ylabel('z $(y={})$'.format(self.settings['QTviewer']['y_cross_pos']))

            # # Update all the plot data with new variables

            arr = self.get_anim_array()  # get array for plotting
            dest_arr = self.substrate.destroyed.copy()

            arr_act = arr == 50
            a = 10 * (spim.filters.maximum_filter(50 * (arr > 40), (5, 5, 5), mode=('mirror', 'wrap', 'constant')))
            # a = 50 * spim.filters.gaussian_filter((50*(coarse_max==50)), 1)
            # self.ax1.clear()
            # contour = self.ax1.contourf(arr[0],
            #                            animated=True,
            #                            zorder=5,
            #                            levels=[40,50])

            output_ims = [self.linev.set_xdata(self.settings['QTviewer']['x_cross_pos']),
                          self.lineh.set_ydata(self.settings['QTviewer']['y_cross_pos']),
                          self.im.set_data(arr[self.settings['QTviewer']['z_cross_pos']]),
                          self.im_destroyed.set_data(dest_arr[self.settings['QTviewer']['z_cross_pos']]),
                          # im2.set_data(arr[self.settings['QTviewer']['z_cross_pos'] + 1]),
                          # im3.set_data(arr[self.settings['QTviewer']['z_cross_pos'] + 2]),
                          self.image.set_data(arr[-1]),
                          self.image_destroyed.set_data(dest_arr[-1]),
                          # image2.set_data(arr[-2]),
                          # image3.set_data(arr[-3]),
                          self.v_cross_view.set_data(
                              np.swapaxes(arr.copy()[:, :, self.settings['QTviewer']['x_cross_pos']], 0, 1)),
                          self.v_cross_destroyed.set_data(
                              np.swapaxes(dest_arr[:, :, self.settings['QTviewer']['x_cross_pos']], 0, 1)),
                          self.h_cross_view.set_data(arr[:, self.settings['QTviewer']['y_cross_pos'], :]),
                          self.h_cross_destroyed.set_data(dest_arr[:, self.settings['QTviewer']['y_cross_pos'], :])
                          ]
            # self.hist.append(frozenset([self.linev,self.lineh,self.im,destroyed,self.image,self.v_cross_view,self.v_cross_destroyed,self.h_cross_view,self.h_cross_destroyed]))

            return output_ims

        def frames():  # Iterator for animation, yield same time value while paused
            t = -1
            while True:
                play = False
                if self.settings['play'] or self.settings['step']:
                    self.settings['step'] = False  # enable one timestep only while paused
                    play = True  # let substrate iterate
                    t += 1
                yield (t, play)

        # def savefunk(t):
        #     return self.hist.get()

        if recall:
            self.saveani = FuncAnimation(self.figure, func, frames, interval=100,
                                         blit=False, save_count=len(self.frozenhist))
            self.i = 0
            self.saveani.save(recall, writer='ffmpeg')
            print('SAVED to {}'.format(recall))
        else:
            self.ani = FuncAnimation(self.figure, func, frames, interval=1, blit=False, save_count=500)
        # self.saveani = FuncAnimation(self.figure, savefunk, interval=5, save_count=500)

    def onclick(self, event):
        if event.xdata:
            self.parent.config.update_v_cross_pos(int(event.xdata))
            self.parent.config.update_h_cross_pos(int(event.ydata))
            if self.settings['ablate']:
                coordinate = (0, int(event.ydata), int(event.xdata))
                self.substrate.add_ablation(coordinate, radius=self.settings['abradius'])
                self.settings['ablate'] = False
                self.parent.ablateAct.setChecked(False)
                self.parent.config.ablationToggle.setChecked(False)

    def get_anim_array(self):
        method = self.settings['view']
        if method == 'activation':
            # self.im.set_cmap('viridis')
            return self.substrate.model_array
        if method == 'count':
            return self.substrate.excount % 3 / 3 * self.settings['structure']['refractory_period']
        if method == 'direction':
            return (5 + self.substrate.direction) / 10 * self.settings['structure']['refractory_period']
        if method == 'max_filter':
            return spim.filters.maximum_filter(self.substrate.model_array, (3, 2, 2),
                                               mode=('mirror', 'wrap', 'constant'))
        if method == 'gauss_filter':
            # self.im.set_cmap('jet')
            arr = np.copy(self.substrate.model_array)
            # arr[arr==50] = 200
            return 2 * spim.filters.gaussian_filter(arr, (5, 1, 1),
                                                    mode=('mirror', 'wrap', 'constant'))

        if method =='expt':
            out = spim.morphological_gradient(self.substrate.model_array, (3,3,3))
            out[(out>0)&(out<45)] = out[(out>0)&(out<45)]/1.5
            return 2 * spim.filters.gaussian_filter(out, (1.5, 1.5, 1.5),
                                                    mode=('mirror', 'wrap', 'constant'))

        # if method == 'expt':
        #     # strut = spim.generate_binary_structure(3,9)
        #     array = self.substrate.model_array
        #     mod_array = spim.grey_closing(array, size=(5,3,3), mode=('mirror', 'wrap', 'constant'))
        #     # out[(out>0)&(out<45)] = out[(out>0)&(out<45)]/1.5
        #     return mod_array

        if method == 'maxgauss':
            arr = np.copy(self.substrate.model_array)
            spim.maximum_filter(arr,size=(2,2,2), output=arr)
            # arr[arr==50] = 200
            return 2 * spim.filters.gaussian_filter(arr, (1.5, 1.5, 1.5),
                                                    mode=('mirror', 'wrap', 'constant'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    af = AFInterface()
    af.show()
    sys.exit(app.exec_())
