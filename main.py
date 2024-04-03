import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtCore
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from kinezet.ui_mainwindow import Ui_MainWindow
import segedprogramok.algoritmus as algoritmus
from functools import reduce
import time
import threading
import pyqtgraph.opengl as gl
from multiprocessing.pool import AsyncResult, ThreadPool

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.jelenlegiLepes=-1
        self.ut_tavolsagok=[]
        self.ut_idok=[]
        self.ut_pontok=[]
        self.ut_ertekek=[]
        self.gyongyokFile="gyongyok.txt"
        self.kicsinyites=10
        self.ut = os.path.dirname(__file__)
        self.setupUi(self)
        #self.loadFileButton.clicked.connect(self.load_file)
        self.StepStopEvent=threading.Event()
        self.startSimulacio.clicked.connect(self.start_simulation)
        self.gyongyokKivalasztasa.clicked.connect(self.load_file)
        self.elozoLepes.clicked.connect(self.previous_simulation)
        self.kovetkezoLepes.clicked.connect(self.next_simulation)
    def loadStep(self,lepes:int):
        self.jelenlegiLepes=lepes
        self.mostaniLepes.setText(f"{lepes+1}.lépés")

        self.StepStopEvent.set()
        self.StepStopEvent = threading.Event()
        animation_thread = threading.Thread(target=self.pygletWidget.run_animation, args=(self.StepStopEvent,self.ut_pontok[lepes],self.ut_pontok[lepes+1],True, self.ut_idok[lepes],1/self.fps,self.kicsinyites))
        animation_thread.start()
    def start_simulation(self):
        # Logic for starting the simulation
        self.ut_tavolsagok,self.ut_idok,self.ut_pontok,self.ut_ertekek = algoritmus.main(self.gyongyokFile,self.ertekek["ido"],self.ertekek["sebesseg"],self.ertekek["x"],self.ertekek["y"],self.ertekek["z"] ,False)
        self.updateSimulation()
        #Load the first step
        self.loadStep(0)
    def load_file(self):
        # Logic for loading a file
        fname,type = QtWidgets.QFileDialog.getOpenFileName(self, 'Gyöngyök megnyitása', 
         'c:\\',"Szöveg fájlok (*.txt)")
        if fname:
            print(fname)
            self.gyongyokFile=fname
    def updateSimulation(self):
        self.pygletWidget.stop_event.set()
        #Kitörölni
        for i in range(self.scrollItems.count()):
            self.scrollItems.itemAt(i).widget().deleteLater()
            self.pygletWidget.reset_to_starting_point2({"x":0,"y":0,"z":0},self.kicsinyites,{"x":0,"y":0,"z":0})
        self.pygletWidget.resetSimulation()
        self.osszes_lepes = QtWidgets.QLabel(f"Összes lépés:{len(self.ut_pontok)-1}",self.scrollArea)
        self.osszes_lepes.setObjectName("elerheto")
        self.scrollItems.addWidget(self.osszes_lepes)
        
        
        self.pygletWidget.addGyongyok(algoritmus.getGyongy(self.gyongyokFile,self.ertekek["x"],self.ertekek["y"],self.ertekek["z"]),self.kicsinyites)
        self.pygletWidget.AkvariumRajzolasa(self.ertekek["x"],self.ertekek["y"],self.ertekek["z"],self.kicsinyites)
        self.pygletWidget.setPathes(self.ut_pontok,self.kicsinyites)
        for id,point in enumerate(self.ut_pontok):
            if id == len(self.ut_pontok)-1:
                continue
            
            self.gridLayoutWidget_2 = QtWidgets.QWidget(self.scrollArea)
            self.gridLayoutWidget_2.setGeometry(QtCore.QRect(20, 10, 160, 80))
            self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
            self.gridLayout_4 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
            self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_4.setObjectName("gridLayout_4")
            self.layoutContainerDirection=QtWidgets.QHBoxLayout()
            self.labelDirection=QtWidgets.QLabel(self.gridLayoutWidget_2)
            self.labelDirection.setText(f"t:{self.ut_idok[id]} s:{self.ut_tavolsagok[id]}\n{id+1}.lépés: {point}->{self.ut_pontok[id+1]}\npontszám:{self.ut_ertekek[id+1]} összespontszám eddig:{reduce(lambda x, y:x+y, self.ut_ertekek[1:(id+2)])}")
            self.pushButtonStep=QtWidgets.QPushButton(self.gridLayoutWidget_2)
            self.pushButtonStep.setText("▶️")
            self.pushButtonStep.setProperty("nth",id)
            self.pushButtonStep.setFixedSize(20,20)
            self.pushButtonStep.clicked.connect(lambda:self.loadStep(self.sender().property("nth")))
            self.layoutContainerDirection.addWidget(self.labelDirection)
            self.layoutContainerDirection.addWidget(self.pushButtonStep)
            self.gridLayout_4.addLayout(self.layoutContainerDirection,1,0,1,1)
            self.scrollItems.addWidget(self.gridLayoutWidget_2)
            if id == 0 or id == len(self.ut_pontok)-2:
                point={
                "x":0,
                "y":0,
                "z":0,
                "e":0,
                }
                if id==0:
                    self.labelDirection.setText(f"t:{self.ut_idok[id]} s:{self.ut_tavolsagok[id]}\n{id+1}.lépés: {point}->{self.ut_pontok[id+1]}\npontszám:{self.ut_ertekek[id+1]} összespontszám eddig:{reduce(lambda x, y:x+y, self.ut_ertekek[1:(id+2)])}")
                else:
                    self.labelDirection.setText(f"t:{self.ut_idok[id]} s:{self.ut_tavolsagok[id]}\n{id+1}.lépés: {self.ut_pontok[id]}->{point}\npontszám:{self.ut_ertekek[id+1]} összespontszám eddig:{reduce(lambda x, y:x+y, self.ut_ertekek[1:(id+2)])}")
                
        self.osszegzes = QtWidgets.QLabel(f"Összes t:{reduce(lambda x, y:x+y, self.ut_idok)}/{self.ertekek['ido']}\nÖsszes s:{reduce(lambda x, y:x+y, self.ut_tavolsagok)}",self.scrollArea)
        self.osszegzes.setObjectName("osszegzes")
        self.scrollItems.addWidget(self.osszegzes)
    def previous_simulation(self):
        # Logic for previous simulation
        if self.jelenlegiLepes != -1:
            if self.jelenlegiLepes ==0 :
                prev=len(self.ut_pontok)-2
            else:
                prev=self.jelenlegiLepes-1
            self.loadStep(prev)
    def next_simulation(self):
        # Logic for next simulation
        if self.jelenlegiLepes != -1:
            if self.jelenlegiLepes < len(self.ut_pontok)-2:
                next=self.jelenlegiLepes + 1
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
