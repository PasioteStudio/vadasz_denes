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
    def __init__(self, scene: trimesh.Scene, parent=None,fps=1/12):
        super(QPygletWidget, self).__init__(parent)
        self.buvarhajoMeshes=[]
        self.stop_event = threading.Event()
        self.gyongyok=[]
        self.akvarium=0
        self.utak=[]
        self.scene = scene
        self.fps=fps
        # Globális változók a kamera pozíciójának és forgatásának
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.camera_position = [0,0,-2.5]
        self.position={
            "x":0,
            "y":0,
            "z":0
        }
        self.rotation={
            "x":0,
            "y":0,
        }
        
        if self.scene:
            for name, mesh in self.scene.geometry.items():
                self.buvarhajoMeshes.append(mesh)
                y_angle=-math.atan(1)*2
                y_direction = [0, 1, 0]
                center = [0, 0, 0]
                y_rot_matrix = trimesh.transformations.rotation_matrix(y_angle, y_direction, center)
                mesh.apply_transform(y_rot_matrix)
                mesh.apply_scale(1/2)
        self.setFocusPolicy(Qt.StrongFocus)
        animation_thread = threading.Thread(target=self.run_animation, args=(self.stop_event,False,False,False,-1,self.fps,1))
        animation_thread.start()
        
    def initializeGL(self):
        glClearColor(float(str(0.5)), 0.5, 0.5, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, [-0.5, -0.5, -1.0, 0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [1, 1, 1, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.camera_position[0],self.camera_position[1],self.camera_position[2])
        
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)
        glRotatef(self.zRot, 0.0, 0.0, 1.0)
        if self.scene:
            for name, mesh in self.scene.geometry.items():
                self.render_mesh(mesh)
        for mesh in self.gyongyok:
            self.render_mesh(mesh)
        for ut in self.utak:
            self.render_path(ut)
        if self.akvarium != 0:
            self.render_mesh(self.akvarium)
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        
    def run_animation(self, stop_event: threading.Event, starting_point: dict, ending_point: dict, step=False, how_long_sec: float = -1, fps: float = 1 / 12,scale:float=10):
        # Kiszámolni a kezdő és vég között a távolságot
        # És egy kicsinyítést teszünk rá, hogy ne legyen hatalmas
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
        # Fő animáció:
        while current_time * fps < how_long_sec or how_long_sec == -1:
            if stop_event.is_set():
                return
            axis = [0, 1, 0]
            center = [0, 0, 0]
            if not step:
                angle = math.pi / 100
                matrix = trimesh.transformations.rotation_matrix(angle, axis, center)
                self.rotation["y"]+=angle
                for name, mesh in self.scene.geometry.items():
                    if mesh in self.buvarhajoMeshes:
                        mesh:trimesh.Trimesh=mesh
                        mesh.apply_transform(matrix)
            else:
                translation_vector = np.array([deltaX, deltaY, deltaZ])

                # A jelenlegi pozíció frissítése
                self.position["x"] += deltaX
                self.position["y"] += deltaY
                self.position["z"] += deltaZ

                # Hozzáadjuk az eltolást a testhez
                for name, mesh in self.scene.geometry.items():
                    if mesh in self.buvarhajoMeshes:
                        mesh:trimesh.Trimesh
                        mesh.apply_translation(translation_vector)
            self.update()
            current_time += 1
            time.sleep(fps)

        if step:
            self.run_animation(stop_event,starting_point,ending_point,step,how_long_sec,self.fps,scale)


    def reset_to_starting_point2(self, starting_point: dict, scale, ending_point: dict):
        
        translation_vector = np.array([
            starting_point["x"] / scale - self.position["x"],
            starting_point["y"] / scale - self.position["y"],
            starting_point["z"] / scale - self.position["z"]
        ])
        for name, mesh in self.scene.geometry.items():
            if mesh in self.buvarhajoMeshes:
                mesh: trimesh.Trimesh
                mesh.apply_translation(translation_vector)
        # Pozíció frissítése
        self.position = {
            "x": starting_point["x"] / scale,
            "y": starting_point["y"] / scale,
            "z": starting_point["z"] / scale,
        }
        
        self.update()
    def addGyongyok(self,gyongyok:list[dict],scale):
        for gyongy in gyongyok:
            gyongyObject = trimesh.creation.capsule(0,gyongy["e"]/scale/10)
            translation_vector = np.array([
                gyongy["x"] / scale,
                gyongy["y"] / scale,
                gyongy["z"] / scale
            ])
            gyongyObject.apply_translation(translation_vector)
            self.gyongyok.append(gyongyObject)
    def setPathes(self,ut_pontok:list[dict],scale:float):
        for id in range(len(ut_pontok)-1):
            start_point = [ut_pontok[id]["x"]/scale, ut_pontok[id]["y"]/scale,ut_pontok[id]["z"]/scale]
            end_point=[ut_pontok[id+1]["x"]/scale, ut_pontok[id+1]["y"]/scale,ut_pontok[id+1]["z"]/scale]
            self.utak.append([start_point, end_point])
    def AkvariumRajzolasa(self,x,y,z,scale):
        self.akvarium  = trimesh.creation.box(extents=[x/scale, y/scale, z/scale])
        translation_vector = np.array([
                z/scale/2,
                y/scale/2,
                x/scale/2
        ])
        self.akvarium.apply_translation(translation_vector)
    def resetSimulation(self):
        self.utak=[]
        self.gyongyok=[]
        self.akvarium=0
    def render_path(self,ut):
        glPointSize(5)
        glBegin(GL_LINES)
        glColor3d(1, 0, 0)
        glVertex4f(ut[0][0], ut[0][1], ut[0][2],1)
        glVertex4f(ut[1][0], ut[1][1], ut[1][2],1)
        glEnd()
    def render_mesh(self, mesh):
        if isinstance(mesh, trimesh.Trimesh):
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, mesh.vertices.flatten())
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, mesh.vertex_normals.flatten())
            if mesh in self.buvarhajoMeshes:
                material = mesh.visual.material
                color = list(material.main_color[:3])
                
                color = colors[str(color)]
                glColor3fv(color)
            if mesh == self.akvarium:             
                glColor4f(0, 0, 0.5, 0.1)
                # Megjelenítjük a testet
                glBegin(GL_QUADS)
                for face in mesh.faces:
                    for vertex in face:
                        glVertex3fv(mesh.vertices[vertex])
                glEnd()
                mesh.visual.vertex_colors = [255, 255, 255, 255]
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
        elif event.key() == Qt.Key_W:
            self.camera_position[2]+=0.1
        elif event.key() == Qt.Key_A:
            self.camera_position[0]+=0.1
        elif event.key() == Qt.Key_S:
            self.camera_position[2]-=0.1
        elif event.key() == Qt.Key_D:
            self.camera_position[0]-=0.1
        elif event.key() == Qt.Key_Space:
            self.camera_position[1]-=0.1
        elif event.key() == Qt.Key_Shift:
            self.camera_position[1]+=0.1
        self.update()