import sys
from PyQt5 import QtWidgets, QtGui
# from PyQt5.QtCore import Qt
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
        playAct.triggered.connect(self.show_phase)
        self.toolbar.addAction(playAct)


        self.setGeometry(300,100,750,600)
        self.setWindowTitle('AF Viewer')

        self.show()

    # def plot(self):
    #     data = [np.random.random() for i in range(10)]
    #     ax = self.figure.add_subplot(111)
    #     ax.plot(data)
    #
    #     self.canvas.draw()

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
        self.sizeq= QtWidgets.QLineEdit(str(config.settings['structure']['size']))
        self.sizeq.editingFinished.connect(self.printer)
        form.addRow(QtWidgets.QLabel('Dimensions'), self.sizeq)

        form.addRow(QtWidgets.QLabel('Linkage'), QtWidgets.QLineEdit())
        refrt = QtWidgets.QLineEdit('220')
        form.addRow(QtWidgets.QLabel('Refractory Period'), refrt)

        self.setLayout(form)
        self.setWindowTitle('Configuration Settings')

        

    def printer(self):
        print(np.array(self.dim.text()))


class makeCanvas(FigureCanvas):
    def __init__(self):
        self.figure = Figure()
        super().__init__(self.figure)
        self.compute_initial_figure()

        self.toolbar = NavigationToolbar(self, self)

    def compute_initial_figure(self):
        pass


class makePhases(makeCanvas):

    def compute_initial_figure(self):
        names = ['Phase_Spaces\\1_200_200.npy', 'Phase_Spaces\\2_200_200.npy',
                 'Phase_Spaces\\4_200_200.npy', 'Phase_Spaces\\8_200_200.npy',
                 'Phase_Spaces\\16_200_200.npy', 'Phase_Spaces/32_200_200.npy']
        compilation = []
        for i in names:
            compilation.append(np.load(i)[:, :, 2])

        for num, i in enumerate(compilation):
            ax = self.figure.add_subplot(200 + len(names)/2 * 10 + 1 + num)
            ax.set_title(names[num][13:-4])
            ax.imshow(i, extent=(0,1,0,1), origin='lower')

class Animation(makeCanvas):

    def compute_initial_figure(self):
        self.crosspos = 50      # Placeholder
        self.substrate = model.Model(**config.settings['structure'])

        gs = GridSpec(1, 2, width_ratios=config.settings['structure']['size'][-2::-1])
        self.ax1 = self.figure.add_subplot(gs[0])
        self.ax2 = self.figure.add_subplot(gs[1])
        image = self.ax1.imshow(self.substrate.model_array[0], animated=True, cmap='Oranges_r',
                                 vmin=0, vmax=config.settings['structure']['refractory_period'],
                                 origin = 'lower', alpha =1, extent=(0,200,0,200))
        image2 = self.ax1.imshow(self.substrate.model_array[-1], animated=True, cmap='Greys_r',
                                  vmin=0, vmax=config.settings['structure']['refractory_period'],
                                  origin = 'lower', alpha = 0.5, extent=(0,200,0,200))
        crossim = self.ax2.imshow(np.swapaxes(self.substrate.model_array[:,:,self.crosspos], 0,1), animated=True,
                                  vmin=0, vmax=config.settings['structure']['refractory_period'],
                                  origin = 'lower', cmap='Greys_r')
        line = self.ax1.axvline(x=self.crosspos, color='cyan', zorder=10, animated=True, linestyle='--')

        def func(t):
            if t % config.settings['sim']['pacemaker_period'] == 0:
                self.substrate.activate_pacemaker()
            self.ax1.set_title('seed={}, t={}'.format(self.substrate.seed, t))
            arr = self.substrate.iterate()
            return [image.set_data(arr[0]), image2.set_data(arr[-1]),
                    crossim.set_data(np.swapaxes(arr[:,:,self.crosspos], 0,1)),
                    line.set_xdata(self.crosspos)]
        self.ani = FuncAnimation(self.figure,func, interval=1, blit=False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    af = AFInterface()
    # af.show()
    sys.exit(app.exec_())