import sys
import trimesh
import threading
import time
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QScrollArea, QLabel, QListWidget, QOpenGLWidget
from PyQt5.QtCore import Qt, QRect
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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
            angle = 3.14 / 100
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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Gyöngykeresés")
        self.setGeometry(50, 150, 1920, 1080)
        
        main_layout = QHBoxLayout()
        
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.listView_2 = QListWidget()
        self.label_5 = QLabel("Label 5")
        self.rootlabel = QLabel("Root Label")
        
        self.sidebar_layout_setup(sidebar_layout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.sidebar.setLayout(sidebar_layout)

        self.pygletWidget = QPygletWidget(scene=trimesh.load("submarine.glb"))
        
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pygletWidget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def sidebar_layout_setup(self, layout):
        self.velocity = QSlider(Qt.Horizontal)
        self.time = QSlider(Qt.Horizontal)
        self.label_4 = QLabel("Dimensions")
        self.x_slider = QSlider(Qt.Horizontal)
        self.y_slider = QSlider(Qt.Horizontal)
        self.z_slider = QSlider(Qt.Horizontal)
        self.listView = QListWidget()
        self.startSim = QPushButton("Start Simulation")
        self.label = QLabel("Settings")
        self.label_2 = QLabel("Velocity")
        self.loadFileButton = QPushButton("Load File")
        self.label_3 = QLabel("Time")
        
        layout.addWidget(self.label)
        layout.addWidget(self.loadFileButton)
        layout.addWidget(self.label_2)
        layout.addWidget(self.velocity)
        layout.addWidget(self.label_3)
        layout.addWidget(self.time)
        layout.addWidget(self.label_4)
        layout.addWidget(self.x_slider)
        layout.addWidget(self.y_slider)
        layout.addWidget(self.z_slider)
        layout.addWidget(self.listView)
        layout.addWidget(self.startSim)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
