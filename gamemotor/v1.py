import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Peliobjektin luokka
class GameObject:
    def __init__(self, position, size, color):
        self.position = np.array(position, dtype=float)
        self.size = np.array(size, dtype=float)
        self.color = color

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glBegin(GL_QUADS)
        glColor3f(*self.color)
        for vertex in self.get_vertices():
            glVertex3f(*vertex)
        glEnd()
        glPopMatrix()

    def get_vertices(self):
        """Palauta kuution kulmapisteet"""
        x, y, z = self.size / 2
        return [
            [-x, -y, -z],
            [x, -y, -z],
            [x, y, -z],
            [-x, y, -z],
            [-x, -y, z],
            [x, -y, z],
            [x, y, z],
            [-x, y, z],
        ]

# Fysiikan moottori
class PhysicsEngine:
    def __init__(self):
        self.gravity = np.array([0, -0.01, 0])
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self):
        for obj in self.objects:
            obj.position += self.gravity

# Pelimoottorin pääluokka
class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.running = True
        self.objects = []
        self.physics = PhysicsEngine()

    def init_window(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        gluPerspective(45, (self.width / self.height), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -10)

    def add_object(self, obj):
        self.objects.append(obj)
        self.physics.add_object(obj)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

    def update(self):
        self.physics.update()

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for obj in self.objects:
            obj.render()
        pygame.display.flip()

    def run(self):
        self.init_window()
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.time.wait(16)  # 60 FPS

# Käyttö
if __name__ == "__main__":
    engine = GameEngine(800, 600)

    # Lisää objekteja pelimoottoriin
    cube = GameObject(position=[0, 0, 0], size=[1, 1, 1], color=[1, 0, 0])  # Punainen kuutio
    engine.add_object(cube)

    ground = GameObject(position=[0, -2, 0], size=[5, 0.5, 5], color=[0, 1, 0])  # Vihreä taso
    engine.add_object(ground)

    # Käynnistä moottori
    engine.run()
