from PyQt5.QtGui import QCloseEvent
from PyQt5.QtOpenGL import QGLWidget
from pyglet.gl import *
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget
from OpenGL.GL import *
from PyQt5.QtCore import Qt
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import trimesh
from trimesh.rendering import *
from trimesh import transformations
from trimesh.visual.material import *
import math
import scipy
import threading
import time
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider,)
from PIL import Image
stop_event = threading.Event()
class QPygletWidget(QGLWidget):
    def __init__(self, scene:trimesh.Scene, parent=None):
        super(QPygletWidget, self).__init__(parent)
        self.scene = scene
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.setFocusPolicy(Qt.StrongFocus)
        animation_thread = threading.Thread(target=self.run_animation,args=(0,stop_event))
        animation_thread.start()

    def initializeGL(self):
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, [0.5, 0.5, 1.0, 0.0])  # Light position

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)  # Move back
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)
        glRotatef(self.zRot, 0.0, 0.0, 1.0)
        if self.scene:
            print(len(self.scene.geometry.values()))
            cur=0
            for name, mesh in self.scene.geometry.items():
                material:PBRMaterial=mesh.visual.material
                print(f"{cur};{material.main_color}")
                cur+=1
                self.render_mesh(mesh)
        
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
    def run_animation(self,asd,stop_event:threading.Event):
        num_frames = 1000  # Number of frames in the animation
        angle_increment = 1  # Angle increment per frame

        for frame in range(num_frames):
            if stop_event.is_set():
                print("Animation stopped")
                return

            # Clear the scene and print the current frame number
            print(f"Frame {frame+1}/{num_frames}")

            # Define the rotation matrix for the current frame
            angle =math.pi /100  # Angle for the current frame
            axis = [0, 1, 0]  # y-axis
            center = [0, 0, 0]  # origin
            matrix = trimesh.transformations.rotation_matrix(angle, axis, center)

            # Apply the rotation to each mesh in the scene
            for name, mesh in self.scene.geometry.items():
                mesh.apply_transform(matrix)

            # Render the scene (you may want to display it in a viewer or save frames as images)
            # Here, we'll just pause for a short time to simulate animation
            self.update()
            time.sleep(0.05)

        # Animation loop finished
        print("Animation finished")
        self.run_animation(0,stop_event=stop_event)
    def asda(self):
        print("sfd")
        if False:
            angle = 90  # degrees
            axis = [0, 1, 0]  # y-axis
            center = [0, 0, 0]  # origin
            matrix = trimesh.transformations.rotation_matrix(angle, axis, center)
            # Apply the transformation to the scene
            for name, mesh in self.scene.geometry.items():
                mesh.apply_transform(matrix)
        if True:
            num_frames = 100  # Number of frames in the animation
            angle_increment = 360 / num_frames  # Angle increment per frame

            # Loop for the animation
            for frame in range(num_frames):
                # Clear the scene and print the current frame number
                print(f"Frame {frame+1}/{num_frames}")

                # Define the rotation matrix for the current frame
                angle = angle_increment * frame  # Angle for the current frame
                axis = [0, 1, 0]  # y-axis
                center = [0, 0, 0]  # origin
                matrix = trimesh.transformations.rotation_matrix(angle, axis, center)

                # Apply the rotation to each mesh in the scene
                for name, mesh in self.scene.geometry.items():
                    mesh.apply_transform(matrix)

                # Render the scene (you may want to display it in a viewer or save frames as images)
                # Here, we'll just pause for a short time to simulate animation
                time.sleep(1)  # Adjust the sleep time as needed for your desired animation speed

            # Animation loop finished
            print("Animation finished")
    def render_mesh(self, mesh):
        if isinstance(mesh, trimesh.Trimesh):
            # Enable vertex array
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, mesh.vertices.flatten())
            
            # Enable normal array
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, mesh.vertex_normals.flatten())

            material:PBRMaterial=mesh.visual.material
            #print(material.main_color[:3])
            #print(list(material.main_color[:3]))
            #print([0.0, 0.5, 0.5])
            # Enable color array
            default_color = [0.0, 0.5, 0.5]
            color=list(material.main_color[:3])
            
            if color not in [[36,140,204],[204,172,0],[255,4,0],[0,0,0] ,[0,12,38], [1,0,33],[204,172,0]]:
                print(f"én{color}")
                color=[0.5,0.5,0.5]
                glColor3fv(color)
                glDrawElements(GL_TRIANGLES, len(mesh.faces) * 3, GL_UNSIGNED_INT, mesh.faces.flatten())
            else:
                
                glColor3fv(color)
                glDrawElements(GL_TRIANGLES, len(mesh.faces) * 3, GL_UNSIGNED_INT, mesh.faces.flatten())
            # Draw the mesh
            
            # Disable arrays
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_NORMAL_ARRAY)
            glDisableClientState(GL_COLOR_ARRAY)
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

        layout = QHBoxLayout()

        sidebar_layout = QVBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(10)
        slider.setSingleStep(1)


        vbox = QVBoxLayout()
        vbox.addWidget(slider)
        vbox.addStretch(1)

        btn_render_cube = QPushButton("Szimuláció elkezdése", self)
        btn_render_cube.clicked.connect(self.toggle_cube_visibility)
        sidebar_layout.addWidget(btn_render_cube)
        sidebar_layout.addWidget(slider)

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(200)

        scene = trimesh.load("W:/vadasz_deni/submarine.glb")

        # Create a QPygletWidget and add it to the layout

        self.pygletWidget = QPygletWidget(scene=scene)
        layout.addWidget(sidebar_widget)
        layout.addWidget(self.pygletWidget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_cube_visibility(self):
        self.glWidget.cubeVisible = not self.glWidget.cubeVisible
        self.glWidget.update()
    def closeEvent(self, event):
        print(f"closing PyQtTest")
        stop_event.set()
        # report_session()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec_())