import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np


# Lataa tekstuuri
def load_texture(image_path):
    texture_surface = pygame.image.load(image_path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width, height = texture_surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id


# Peliobjektin luokka
class GameObject:
    def __init__(self, position, size, color=None, texture=None):
        self.position = np.array(position, dtype=float)
        self.size = np.array(size, dtype=float)
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.color = color
        self.texture = texture

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)

        if self.texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)

        glBegin(GL_QUADS)

        if self.color:
            glColor3f(*self.color)

        vertices = self.get_vertices()
        texture_coords = self.get_texture_coords()

        for i, vertex in enumerate(vertices):
            if self.texture:
                glTexCoord2f(*texture_coords[i])
            glVertex3f(*vertex)

        glEnd()

        if self.texture:
            glDisable(GL_TEXTURE_2D)

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

    def get_texture_coords(self):
        """Tekstuurikoordinaatit kuution pinnoille"""
        return [
            [0, 0], [1, 0], [1, 1], [0, 1],  # Front
            [0, 0], [1, 0], [1, 1], [0, 1],  # Back
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
            obj.velocity += self.gravity
            obj.position += obj.velocity

            # Törmäystarkistus muiden objektien kanssa
            for other in self.objects:
                if obj != other and self.check_collision(obj, other):
                    obj.velocity *= -0.5  # Kimmoisuuskerroin

    def check_collision(self, obj1, obj2):
        """Tarkista, törmäävätkö kaksi objektia"""
        min1 = obj1.position - obj1.size / 2
        max1 = obj1.position + obj1.size / 2
        min2 = obj2.position - obj2.size / 2
        max2 = obj2.position + obj2.size / 2
        return all(min1 <= max2) and all(max1 >= min2)


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

    # Lisää tekstuuri
    wood_texture = load_texture("wood.jpg")  # Varmista, että tiedosto 'wood.jpg' on olemassa

    # Lisää objekteja pelimoottoriin
    cube = GameObject(position=[0, 2, 0], size=[1, 1, 1], texture=wood_texture)  # Tekstuuroitu kuutio
    engine.add_object(cube)

    ground = GameObject(position=[0, -2, 0], size=[5, 0.5, 5], color=[0, 1, 0])  # Vihreä taso
    engine.add_object(ground)

    # Käynnistä moottori
    engine.run()
