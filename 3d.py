import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtCore
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from kinezet.ui_mainwindow import Ui_MainWindow
import segedprogramok.algoritmus as algoritmus
from functools import reduce
import threading
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.currentStep=-1
        self.path_distances=[]
        self.path_times=[]
        self.path_points=[]
        self.path_value=[]
        self.setupUi(self)
        #self.loadFileButton.clicked.connect(self.load_file)
        self.startSimulacio.clicked.connect(self.start_simulation)
        self.elozoLepes.clicked.connect(self.previous_simulation)
        self.kovetkezoLepes.clicked.connect(self.next_simulation)
        self.StepStopEvent=threading.Event()
    def loadStep(self,step:int):
        print(step)
        self.currentStep=step
        self.mostaniLepes.setText(f"{step+1}.lépés")

        self.StepStopEvent.set()
        self.StepStopEvent = threading.Event()
        animation_thread = threading.Thread(target=self.pygletWidget.run_animation2, args=(self.StepStopEvent,self.path_points[step],self.path_points[step+1],True, self.path_times[step],1/12,5))
        animation_thread.start()
    def start_simulation(self):
        # Logic for starting the simulation
        print("Starting simulation...")
        self.path_distances,self.path_times,self.path_points,self.path_value=algoritmus.main(self.ertekek["ido"],self.ertekek["sebesseg"],True,False)
        self.updateSimulation()
        #Load the first step
        self.loadStep(0)
    def load_file(self):
        # Logic for loading a file
        print("Loading file...")
    def updateSimulation(self):
        self.pygletWidget.stop_event.set()
        #Kitörölni
        print(self.scrollItems.count())
        for i in range(self.scrollItems.count()):  
            self.scrollItems.itemAt(i).widget().deleteLater()
        self.osszes_lepes = QtWidgets.QLabel(f"Összes lépés:{len(self.path_points)-1}",self.scrollArea)
        self.osszes_lepes.setObjectName("elerheto")
        self.scrollItems.addWidget(self.osszes_lepes)

        for id,point in enumerate(self.path_points):
            if id == len(self.path_points)-1:
                continue
            
            self.gridLayoutWidget_2 = QtWidgets.QWidget(self.scrollArea)
            self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 10, 160, 80))
            self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
            self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
            self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_4.setObjectName("gridLayout_4")
            self.labelTimePath=QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.labelTimePath.setText(f"t:{self.path_times[id]} s:{self.path_distances[id]}")
            self.gridLayout_4.addWidget(self.labelTimePath,0,0,1,1)
            self.layoutContainerDirection=QtWidgets.QHBoxLayout()
            self.labelDirection=QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.labelDirection.setText(f"{id+1}.lépés: {point}->{self.path_points[id+1]}")
            self.pushButtonStep=QtWidgets.QPushButton(self.gridLayoutWidget_2)
            self.pushButtonStep.setText("▶️")
            self.pushButtonStep.setProperty("nth",id)
            self.pushButtonStep.setFixedSize(30,30)
            self.pushButtonStep.clicked.connect(lambda:self.loadStep(self.sender().property("nth")))
            self.layoutContainerDirection.addWidget(self.labelDirection)
            self.layoutContainerDirection.addWidget(self.pushButtonStep)
            self.gridLayout_4.addLayout(self.layoutContainerDirection,1,0,1,1)
            self.labelValue=QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.labelValue.setText(f"pontszám:{self.path_value[id+1]} összespontszám eddig:{reduce(lambda x, y:x+y, self.path_value[1:(id+2)])}")
            self.gridLayout_4.addWidget(self.labelValue,2,0,1,1)
            self.scrollItems.addWidget(self.gridLayoutWidget_2)
            if id == 0 or id == len(self.path_points)-2:
                point={
                "x":0,
                "y":0,
                "z":0,
                "e":0,
                }
                if id==0:
                    self.labelDirection.setText(f"{id+1}.lépés: {point}->{self.path_points[id+1]}")
                else:
                    self.labelDirection.setText(f"{id+1}.lépés: {self.path_points[id]}->{point}")
                
        self.osszegzes = QtWidgets.QLabel(f"Összes t:{reduce(lambda x, y:x+y, self.path_times)}/{self.ertekek["ido"]}\nÖsszes s:{reduce(lambda x, y:x+y, self.path_distances)}",self.scrollArea)
        self.osszegzes.setObjectName("osszegzes")
        self.scrollItems.addWidget(self.osszegzes)
    
    def previous_simulation(self):
        # Logic for previous simulation
        print("Previous simulation...")
        if self.currentStep ==0 :
            prev=len(self.path_points)-2
        else:
            prev=self.currentStep-1
        self.loadStep(prev)
    def next_simulation(self):
        # Logic for next simulation
        print("Next simulation...")
        if self.currentStep < len(self.path_points)-2:
            next=self.currentStep + 1
        else:
            next=0
        self.loadStep(next)
    def closeEvent(self,event):
        self.StepStopEvent.set()
        self.pygletWidget.stop_event.set()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
