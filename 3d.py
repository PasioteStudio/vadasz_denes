import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from ui_mainwindow import Ui_MainWindow
import algoritmus

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #uic.loadUi('GUI.ui', self) # Load the .ui file
        self.setupUi(self)
        #self.startSim.clicked.connect(self.start_simulation)
        #self.loadFileButton.clicked.connect(self.load_file)
        self.startSimulacio.clicked.connect(self.start_simulation)
        self.elozoLepes.clicked.connect(self.previous_simulation)
        self.kovetkezoLepes.clicked.connect(self.next_simulation)
    def start_simulation(self):
        # Logic for starting the simulation
        print("Starting simulation...")
        algoritmus.

    def load_file(self):
        # Logic for loading a file
        print("Loading file...")

    def previous_simulation(self):
        # Logic for previous simulation
        print("Previous simulation...")

    def next_simulation(self):
        # Logic for next simulation
        print("Next simulation...")
    def closeEvent(self,event):
        self.pygletWidget.stop_event.set()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
