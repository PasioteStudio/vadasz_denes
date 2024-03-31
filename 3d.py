import sys
import trimesh
import threading
import time
import numpy as np
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QScrollArea, QLabel, QListWidget, QListView, QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from gui import Ui_MainWindow


colors = {
    "[36, 140, 204]": [36, 140, 204],
    "[0, 0, 0]": [0, 0, 0],
    "[255, 0, 0]": [255, 0, 0],
    "[0, 12, 38]": [0, 12, 38],
    "[1, 0, 33]": [1, 0, 33],
    "[204, 172, 0]": [204, 172, 0],
    "[13, 13, 13]": [13, 13, 13],
    "[255, 4, 0]": [255, 4, 0],
}

stop_event = threading.Event()

class QPygletWidget(QOpenGLWidget):
    def __init__(self, scene: trimesh.Scene, parent=None):
        super(QPygletWidget, self).__init__(parent)
        self.scene = scene
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.setFocusPolicy(Qt.StrongFocus)
        animation_thread = threading.Thread(target=self.run_animation, args=(0, stop_event))
        animation_thread.start()

    def initializeGL(self):
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, [0.5, 0.5, 1.0, 0.0])

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)
        glRotatef(self.zRot, 0.0, 0.0, 1.0)
        if self.scene:
            for name, mesh in self.scene.geometry.items():
                material = mesh.visual.material
                color = list(material.main_color[:3])
                color = colors[str(color)]
                glColor3fv(color)
                self.render_mesh(mesh)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def run_animation(self, asd, stop_event: threading.Event):
        num_frames = 1000
        angle_increment = 1
        for frame in range(num_frames):
            if stop_event.is_set():
                return
            angle = math.pi / 100
            axis = [0, 1, 0]
            center = [0, 0, 0]
            matrix = trimesh.transformations.rotation_matrix(angle, axis, center)
            for name, mesh in self.scene.geometry.items():
                mesh.apply_transform(matrix)
            self.update()
            time.sleep(0.05)

    def render_mesh(self, mesh):
        if isinstance(mesh, trimesh.Trimesh):
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, mesh.vertices.flatten())
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, mesh.vertex_normals.flatten())
            material = mesh.visual.material
            default_color = [0.0, 0.0, 0.0]
            color = list(material.main_color[:3])
            color = colors[str(color)]
            glColor3fv(color)
            glDrawElements(GL_TRIANGLES, len(mesh.faces) * 3, GL_UNSIGNED_INT, mesh.faces.flatten())
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_NORMAL_ARRAY)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.yRot -= 5
        elif event.key() == Qt.Key_Right:
            self.yRot += 5
        elif event.key() == Qt.Key_Up:
            self.xRot -= 5
        elif event.key() == Qt.Key_Down:
            self.xRot += 5
        self.update()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.pygletWidget = QPygletWidget(scene=trimesh.load("submarine.glb"))

        self.startSim.clicked.connect(self.start_simulation)
        self.loadFileButton.clicked.connect(self.load_file)
        self.startbutton.clicked.connect(self.start_simulation)
        self.prevbutton.clicked.connect(self.previous_simulation)
        self.nextbutton.clicked.connect(self.next_simulation)

    def start_simulation(self):
        # Logic for starting the simulation
        print("Starting simulation...")

    def load_file(self):
        # Logic for loading a file
        print("Loading file...")

    def previous_simulation(self):
        # Logic for previous simulation
        print("Previous simulation...")

    def next_simulation(self):
        # Logic for next simulation
        print("Next simulation...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
