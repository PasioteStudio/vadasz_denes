import os
from PyQt5 import QtCore, QtGui, QtWidgets
import trimesh
import kinezet.pyglet as pyglet
max_sidebars_width=400
info_spacing=80
class Ui_MainWindow(object):
    def __init__(self) -> None:
        self.ertekek:dict={
            "sebesseg":1,
            "ido":100,
            "x":100,
            "y":100,
            "z":100
        }
        self.max_ertekek={
            "sebesseg":10,
            "ido":1000,
            "x":10000,
            "y":10000,
            "z":10000
        }
        self.fps=12
    def setupUi(self, MainWindow:QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(611, 466)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout:QtWidgets.QGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        MainWindow.setStyleSheet(MainWindow.styleSheet()+"""
                            #elozoLepes,#kovetkezoLepes{
                                border:none;
                                color:white;                            
                            }
                            """)
        self.centralwidget.setLayout(self.gridLayout)
        self.centralLayout=QtWidgets.QGridLayout()
        self.pygletWidget:pyglet.QPygletWidget = pyglet.QPygletWidget(scene=trimesh.load(self.ut+"/submarine.glb"),fps=1/self.fps)
        self.pygletWidget.setMinimumSize(100,100)
        self.centralLayout.addWidget(self.pygletWidget)
        self.gridLayout.addLayout(self.centralLayout,0,1,3,1)
        
        
        
        self.footer = QtWidgets.QHBoxLayout()
        self.footer.setContentsMargins(-1, 45, -1, -1)
        self.footer.setObjectName("footer")
        self.elozoLepes = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.elozoLepes.setObjectName("elozoLepes")
        self.elozoLepes.setMinimumSize(150,50)
        self.elozoLepes.setMaximumSize(200,100)
        self.elozoLepes.setFont(QtGui.QFont('Arial', 30))
        self.elozoLepes.setBaseSize(150,50)
        self.footer.addStretch(1)
        self.footer.addWidget(self.elozoLepes,0)
        self.mostaniLepes:QtWidgets.QLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.mostaniLepes.setObjectName("mostaniLepes")
        self.mostaniLepes.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.mostaniLepes.setMinimumSize(150,50)
        self.mostaniLepes.setMaximumSize(200,100)
        self.mostaniLepes.setBaseSize(150,50)
        self.footer.addWidget(self.mostaniLepes,0)
        self.kovetkezoLepes = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.kovetkezoLepes.setObjectName("kovetkezoLepes")
        self.kovetkezoLepes.setMinimumSize(150,50)
        self.kovetkezoLepes.setMaximumSize(200,100)
        self.kovetkezoLepes.setFont(QtGui.QFont('Arial', 30))
        self.kovetkezoLepes.setBaseSize(150,50)
        self.footer.addWidget(self.kovetkezoLepes,0)
        self.gridLayout.addLayout(self.footer, 3, 0, 1, 3)
        self.footer.addStretch(1)
        
        self.leftsidebarWidget=QtWidgets.QWidget(self.gridLayoutWidget)
        self.leftsidebarWidget.setMaximumWidth(max_sidebars_width)
        self.leftsidebar = QtWidgets.QVBoxLayout()
        self.leftsidebar.setObjectName("leftsidebar")
        self.leftsidebarWidget.setLayout(self.leftsidebar)
        self.leftsidebar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.SetValueChangers()
        
        self.horizontalSliderFps=QtWidgets.QSlider(self.gridLayoutWidget)
        self.horizontalSliderFps.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderFps.setMaximum(60)
        self.horizontalSliderFps.setMinimum(1)
        self.horizontalSliderFps.setValue(self.fps)
        self.labelInfoFps = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelInfoFps.setObjectName("labelInfoFps")
        self.labelInfoFps.setText(f"Fps: {self.fps}")
        self.horizontalSliderFps.valueChanged.connect(lambda: self.setFps(self.labelInfoFps,self.horizontalSliderFps))
        self.fpsContainer=QtWidgets.QHBoxLayout()
        self.fpsContainer.addWidget(self.labelInfoFps)
        self.fpsContainer.addWidget(self.horizontalSliderFps)
        self.leftsidebar.addLayout(self.fpsContainer)
        
        self.startSimulacio = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.startSimulacio.setObjectName("startSimulacio")
        self.leftsidebar.addWidget(self.startSimulacio)
        self.gridLayout.addWidget(self.leftsidebarWidget, 0, 0, 3, 1)
        
        
        
        self.rightsidebarWidget=QtWidgets.QWidget(self.gridLayoutWidget)
        self.rightsidebar = QtWidgets.QVBoxLayout()
        self.rightsidebarWidget.setLayout(self.rightsidebar)
        self.rightsidebar.setObjectName("rightsidebar")
        self.scrollArea:QtWidgets.QScrollArea=QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollItems:QtWidgets.QVBoxLayout=QtWidgets.QVBoxLayout(self.scrollArea)
        self.scrollBox = QtWidgets.QGroupBox()
        self.scrollBox.setLayout(self.scrollItems)
        self.scrollArea.setWidget(self.scrollBox)
        self.scrollArea.setObjectName("scroll_area")
        
        self.rightsidebar.addWidget(self.scrollArea)
        self.rightsidebarWidget.setMaximumWidth(max_sidebars_width)
        self.gridLayout.addWidget(self.rightsidebarWidget, 0, 2, 3, 1)
        
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 611, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        return 
    def setFps(self,label:QtWidgets.QLabel,horizantalSlider:QtWidgets.QSlider):
        self.fps = horizantalSlider.value()
        label.setText(f"Fps: {self.fps}")
        self.pygletWidget.fps=1/self.fps
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.elozoLepes.setText(_translate("MainWindow", "⏮"))
        self.mostaniLepes.setText(_translate("MainWindow", "nth.lépés"))
        self.kovetkezoLepes.setText(_translate("MainWindow", "⏯️"))
        self.startSimulacio.setText(_translate("MainWindow", "Start Szimuláció"))
    def ValidateValues(self,lineEdit:QtWidgets.QLineEdit,horizantalSlider:QtWidgets.QSlider,Value:str):
        previousValue=self.ertekek[Value]
        if str(previousValue) == lineEdit.text():
            lineEdit.setText(str(horizantalSlider.value()))  
        elif str(previousValue) == str(horizantalSlider.value()):
            #Megnézzük, hogy a lineEdit int-e
            if lineEdit.text() == "":
                horizantalSlider.setValue(0)
                lineEdit.setText(str(horizantalSlider.value()))
            else:
                if not lineEdit.text().isnumeric():
                    lineEdit.setText(str(previousValue))
                    horizantalSlider.setValue(int(lineEdit.text()))
                else:
                    if int(lineEdit.text()) > self.max_ertekek[Value]:
                        lineEdit.setText(str(previousValue))
                    horizantalSlider.setValue(int(lineEdit.text()))    
        self.ertekek[Value]=horizantalSlider.value()
    def SetValueChangers(self):
        _translate = QtCore.QCoreApplication.translate
        self.textLayoutIdo=QtWidgets.QHBoxLayout()
        self.labelIdo = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelIdo.setObjectName("labelIdo")
        self.textLayoutIdo.addWidget(self.labelIdo)
        self.lineEditIdo = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditIdo.setObjectName("lineEditIdo")
        self.textLayoutIdo.addWidget(self.lineEditIdo)
        self.leftsidebar.addLayout(self.textLayoutIdo)
        self.horizontalSliderIdo = QtWidgets.QSlider(self.gridLayoutWidget)
        self.horizontalSliderIdo.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderIdo.setObjectName("horizontalSliderIdo")
        self.leftsidebar.addWidget(self.horizontalSliderIdo)
        self.labelInfoIdo = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelInfoIdo.setObjectName("labelInfoIdo")
        self.labelInfoIdo.setText(f"1{' '*(info_spacing-len(str(self.max_ertekek['ido'])))}{self.max_ertekek['ido']}")
        self.leftsidebar.addWidget(self.labelInfoIdo)
        self.lineEditIdo.setText(str(self.ertekek["ido"]))
        self.horizontalSliderIdo.setMaximum(self.max_ertekek["ido"])
        self.horizontalSliderIdo.setMinimum(1)
        self.horizontalSliderIdo.setValue(self.ertekek["ido"])
        self.lineEditIdo.textEdited.connect(lambda: self.ValidateValues(self.lineEditIdo,self.horizontalSliderIdo,"ido"))
        self.horizontalSliderIdo.valueChanged.connect(lambda: self.ValidateValues(self.lineEditIdo,self.horizontalSliderIdo,"ido"))
        self.labelIdo.setText(_translate("MainWindow", "Idő:"))

        self.textLayoutSebesseg=QtWidgets.QHBoxLayout()
        self.labelSebesseg = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelSebesseg.setObjectName("labelSebesseg")
        self.textLayoutSebesseg.addWidget(self.labelSebesseg)
        self.lineEditSebesseg = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditSebesseg.setObjectName("lineEditSebesseg")
        self.textLayoutSebesseg.addWidget(self.lineEditSebesseg)
        self.leftsidebar.addLayout(self.textLayoutSebesseg)
        self.horizontalSliderSebesseg = QtWidgets.QSlider(self.gridLayoutWidget)
        self.horizontalSliderSebesseg.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderSebesseg.setObjectName("horizontalSliderSebesseg")
        self.leftsidebar.addWidget(self.horizontalSliderSebesseg)
        self.labelInfoSebesseg = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelInfoSebesseg.setObjectName("labelInfoSebesseg")
        self.labelInfoSebesseg.setText(f"1{' '*(info_spacing-len(str(self.max_ertekek['sebesseg'])))}{self.max_ertekek['sebesseg']}")
        self.leftsidebar.addWidget(self.labelInfoSebesseg)
        self.lineEditSebesseg.setText(str(self.ertekek["sebesseg"]))
        self.horizontalSliderSebesseg.setMaximum(self.max_ertekek["sebesseg"])
        self.horizontalSliderSebesseg.setMinimum(1)
        self.horizontalSliderSebesseg.setValue(self.ertekek["sebesseg"])
        self.lineEditSebesseg.textEdited.connect(lambda: self.ValidateValues(self.lineEditSebesseg,self.horizontalSliderSebesseg,"sebesseg"))
        self.horizontalSliderSebesseg.valueChanged.connect(lambda: self.ValidateValues(self.lineEditSebesseg,self.horizontalSliderSebesseg,"sebesseg"))
        self.labelSebesseg.setText(_translate("MainWindow", "Sebesség:"))
        
        self.textLayoutX=QtWidgets.QHBoxLayout()
        self.labelX = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelX.setObjectName("labelX")
        self.textLayoutX.addWidget(self.labelX)
        self.lineEditX = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditX.setObjectName("lineEditX")
        self.textLayoutX.addWidget(self.lineEditX)
        self.leftsidebar.addLayout(self.textLayoutX)
        self.horizontalSliderX = QtWidgets.QSlider(self.gridLayoutWidget)
        self.horizontalSliderX.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderX.setObjectName("horizontalSliderX")
        self.leftsidebar.addWidget(self.horizontalSliderX)
        self.labelInfoX = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelInfoX.setObjectName("labelInfoX")
        self.labelInfoX.setText(f"1{' '*(info_spacing-len(str(self.max_ertekek['x'])))}{self.max_ertekek['x']}")
        self.leftsidebar.addWidget(self.labelInfoX)
        self.lineEditX.setText(str(self.ertekek["x"]))
        self.horizontalSliderX.setMaximum(self.max_ertekek["x"])
        self.horizontalSliderX.setMinimum(1)
        self.horizontalSliderX.setValue(self.ertekek["x"])
        self.lineEditX.textEdited.connect(lambda: self.ValidateValues(self.lineEditX,self.horizontalSliderX,"x"))
        self.horizontalSliderX.valueChanged.connect(lambda: self.ValidateValues(self.lineEditX,self.horizontalSliderX,"x"))
        self.labelX.setText(_translate("MainWindow", "Akvárium x hosszúsága:"))
        
        self.textLayoutY=QtWidgets.QHBoxLayout()
        self.labelY = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelY.setObjectName("labelY")
        self.textLayoutY.addWidget(self.labelY)
        self.lineEditY = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditY.setObjectName("lineEditY")
        self.textLayoutY.addWidget(self.lineEditY)
        self.leftsidebar.addLayout(self.textLayoutY)
        self.horizontalSliderY = QtWidgets.QSlider(self.gridLayoutWidget)
        self.horizontalSliderY.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderY.setObjectName("horizontalSliderY")
        self.leftsidebar.addWidget(self.horizontalSliderY)
        self.labelInfoY = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelInfoY.setObjectName("labelInfoY")
        self.labelInfoY.setText(f"1{''*(info_spacing-len(str(self.max_ertekek['y'])))}{self.max_ertekek['y']}")
        self.leftsidebar.addWidget(self.labelInfoY)
        self.lineEditY.setText(str(self.ertekek["y"]))
        self.horizontalSliderY.setMaximum(self.max_ertekek["y"])
        self.horizontalSliderY.setMinimum(1)
        self.horizontalSliderY.setValue(self.ertekek["y"])
        self.lineEditY.textEdited.connect(lambda: self.ValidateValues(self.lineEditY,self.horizontalSliderY,"y"))
        self.horizontalSliderY.valueChanged.connect(lambda: self.ValidateValues(self.lineEditY,self.horizontalSliderY,"y"))
        self.labelY.setText(_translate("MainWindow", "Akvárium y hosszúsága:"))
        
        self.textLayoutZ=QtWidgets.QHBoxLayout()
        self.labelZ = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelZ.setObjectName("labelZ")
        self.textLayoutZ.addWidget(self.labelZ)
        self.lineEditZ = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEditZ.setObjectName("lineEditZ")
        self.textLayoutZ.addWidget(self.lineEditZ)
        self.leftsidebar.addLayout(self.textLayoutZ)
        self.horizontalSliderZ = QtWidgets.QSlider(self.gridLayoutWidget)
        self.horizontalSliderZ.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderZ.setObjectName("horizontalSliderZ")
        self.leftsidebar.addWidget(self.horizontalSliderZ)
        self.labelInfoZ = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelInfoZ.setObjectName("labelInfoZ")
        self.labelInfoZ.setText(f"1{' '*(info_spacing-len(str(self.max_ertekek['z'])))}{self.max_ertekek['z']}")
        self.leftsidebar.addWidget(self.labelInfoZ)
        self.lineEditZ.setText(str(self.ertekek["z"]))
        self.horizontalSliderZ.setMaximum(self.max_ertekek["z"])
        self.horizontalSliderZ.setMinimum(1)
        self.horizontalSliderZ.setValue(self.ertekek["z"])
        self.lineEditZ.textEdited.connect(lambda: self.ValidateValues(self.lineEditZ,self.horizontalSliderZ,"z"))
        self.horizontalSliderZ.valueChanged.connect(lambda: self.ValidateValues(self.lineEditZ,self.horizontalSliderZ,"z"))
        self.labelZ.setText(_translate("MainWindow", "Akvárium z hosszúsága:"))
        
        self.gyongyokKivalasztasa = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.gyongyokKivalasztasa.setObjectName("gyongyokKivalasztasa")
        self.gyongyokKivalasztasa.setText("Gyöngyök Kiválasztása")
        self.leftsidebar.addWidget(self.gyongyokKivalasztasa)