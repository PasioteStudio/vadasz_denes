import trimesh
import threading
import time
import math
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QScrollArea, QLabel, QListWidget, QListView, QOpenGLWidget
import numpy as np
colors = {
    "[36, 140, 204]": [0, 140, 204], #fülke
    "[0, 0, 0]": [0, 0, 0],
    "[255, 0, 0]": [255, 0, 0],
    "[0, 12, 38]": [0, 12, 38],
    "[1, 0, 33]": [1, 0, 33],
    "[204, 172, 0]": [204, 0, 0],
    "[13, 13, 13]": [13, 13, 13],
    "[255, 4, 0]": [100, 4, 0],
}
class QPygletWidget(QOpenGLWidget):
    def __init__(self, scene: trimesh.Scene, parent=None):
        super(QPygletWidget, self).__init__(parent)
        self.stop_event = threading.Event()
        self.scene = scene
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.position={
            "x":0,
            "y":0,
            "z":0
        }
        self.rotation={
            "x":"",
            "y":"",
        }
        self.had=False
        self.setFocusPolicy(Qt.StrongFocus)
        animation_thread = threading.Thread(target=self.run_animation, args=(self.stop_event,False,False,False,-1,1/12,1))
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
                self.render_mesh(mesh)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        
    def run_animation(self, stop_event: threading.Event, starting_point: dict, ending_point: dict, step=False, how_long_sec: float = -1, fps: float = 1 / 12,scale:float=10):
        # Calculate deltas for translation
        # Apply scaling to starting and ending points
        if step:
            scaled_starting_point = {
                "x": starting_point["x"] / scale,
                "y": starting_point["y"] / scale,
                "z": starting_point["z"] / scale
            }
            scaled_ending_point = {
                "x": ending_point["x"] / scale,
                "y": ending_point["y"] / scale,
                "z": ending_point["z"] / scale
            }
            self.reset_to_starting_point2(starting_point,scale,ending_point)
            deltaX = (scaled_ending_point["x"] - scaled_starting_point["x"]) / how_long_sec * fps
            deltaY = (scaled_ending_point["y"] - scaled_starting_point["y"]) / how_long_sec * fps
            deltaZ = (scaled_ending_point["z"] - scaled_starting_point["z"]) / how_long_sec * fps
        current_time=0
        # Main animation loop
        while current_time * fps < how_long_sec or how_long_sec == -1:
            if stop_event.is_set():
                return
            axis = [0, 1, 0]
            center = [0, 0, 0]
            if not step:
                angle = math.pi / 100
                matrix = trimesh.transformations.rotation_matrix(angle, axis, center)
                for name, mesh in self.scene.geometry.items():
                    mesh:trimesh.Trimesh=mesh
                    mesh.apply_transform(matrix)
            else:
                # Calculate translation vector
                translation_vector = np.array([deltaX, deltaY, deltaZ])

                # Update position
                self.position["x"] += deltaX
                self.position["y"] += deltaY
                self.position["z"] += deltaZ

                # Apply translation to meshes
                for name, mesh in self.scene.geometry.items():
                    mesh:trimesh.Trimesh
                    mesh.apply_translation(translation_vector)
            self.update()
            current_time += 1
            time.sleep(fps)

        # If step is True, reset position to starting point
        if step:
            self.run_animation(stop_event,starting_point,ending_point,step,how_long_sec,fps,scale)


    def reset_to_starting_point2(self, starting_point: dict, scale, ending_point: dict):
        # Reset the rotation based on the current rotation "tracker"
        if self.rotation["x"]!="":
            print(self.rotation)
            x_angle = np.pi*2- self.rotation["x"]
            y_angle = np.pi*2-self.rotation["y"]
            x_direction = [1, 0, 0] #x
            y_direction = [0, 1, 0] #y
            center = [0, 0, 0]

            x_rot_matrix = trimesh.transformations.rotation_matrix(x_angle, x_direction, center)
            y_rot_matrix = trimesh.transformations.rotation_matrix(y_angle, y_direction, center)
            for name, mesh in self.scene.geometry.items():
                mesh: trimesh.Trimesh
                mesh.apply_transform(np.dot(y_rot_matrix, x_rot_matrix))
            self.rotation={
                "x":0,
                "y":0
            }
        #Set the rotation
        if not self.had:
            x_angle = math.pi / 4
            y_angle = math.pi / 4
            x_direction = [1, 0, 0] #x
            y_direction = [0, 1, 0] #y
            center = [0, 0, 0]

            x_rot_matrix = trimesh.transformations.rotation_matrix(x_angle, x_direction, center)
            y_rot_matrix = trimesh.transformations.rotation_matrix(y_angle, y_direction, center)

        # Calculate the translation vector
        translation_vector = np.array([
            starting_point["x"] / scale - self.position["x"],
            starting_point["y"] / scale - self.position["y"],
            starting_point["z"] / scale - self.position["z"]
        ])

        for name, mesh in self.scene.geometry.items():
            mesh: trimesh.Trimesh
            mesh.apply_translation(translation_vector)
            if not self.had:
                mesh.apply_transform(x_rot_matrix)
                mesh.apply_transform(y_rot_matrix)

        # Update position
        self.position = {
            "x": starting_point["x"] / scale,
            "y": starting_point["y"] / scale,
            "z": starting_point["z"] / scale,
        }
        if not self.had:
            print("sad")
            self.rotation={
                "x":x_angle,
                "y":y_angle
            }
            self.had=True
        else:
            pass
        self.update()
    def render_mesh(self, mesh):
        if isinstance(mesh, trimesh.Trimesh):
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, mesh.vertices.flatten())
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, mesh.vertex_normals.flatten())
            material = mesh.visual.material
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
