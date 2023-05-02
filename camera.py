import pygame as pg
import numpy as np
from vect_operations import *

class Camera:

    def __init__(self, position, orientation, up, FOV, ratio, nPlan, fPlan, speed=.10, rotation_speed=1.0):
        self.position = np.array(position, dtype=np.float32)
        self.orientation = np.array(orientation, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        self.FOV = FOV
        self.ratio = ratio
        self.nPlan = nPlan
        self.fPlan = fPlan
        self.speed = speed
        self.rotation_speed = rotation_speed

    def get_view_matrix(self):
        # Calcul de la direction de la caméra
        direction = self.orientation - self.position
        direction = direction / np.linalg.norm(direction)

        # Calcul de la direction droite de la caméra
        right = np.cross(direction, self.up)
        right = right / np.linalg.norm(right)

        # Calcul de la direction vers le haut de la caméra
        up = np.cross(right, direction)
        up = up / np.linalg.norm(up)

        # Création de la matrice de vue
        view_matrix = np.eye(4)
        view_matrix[0, 0:3] = right
        view_matrix[1, 0:3] = up
        view_matrix[2, 0:3] = -direction
        view_matrix[0:3, 3] = -np.dot(view_matrix[0:3, 0:3], self.position)

        return view_matrix

    def get_proj_matrix(self):
        w = np.tan(self.FOV / 2) * self.nPlan
        h = w / self.ratio

        self.P = np.array([2 * self.nPlan / w, 0, 0, 0,
                      0, 2 * self.nPlan / h, 0, 0,
                      0, 0, -(self.fPlan + self.nPlan) / (self.fPlan - self.nPlan), -2 * self.fPlan * self.nPlan / (self.fPlan - self.nPlan),
                      0, 0, -1, 0], dtype=np.float32)

        return np.reshape(self.P, (4, 4))
    

    def zoom(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:  # scroll up
                    self.FOV += .01
                elif event.button == 5:  # scroll down
                    self.FOV -= .01

    def move(self, direction):
        self.position += direction

    def handle_events(self):
        keys = pg.key.get_pressed()

        # Mouvement de la caméra
        if keys[pg.K_z]:
            direction = self.orientation - self.position
            direction = direction / np.linalg.norm(direction)
            self.move(direction)

        if keys[pg.K_q]:
            direction = np.cross(self.up, self.orientation - self.position)
            direction = direction / np.linalg.norm(direction)
            self.move(direction)

        if keys[pg.K_s]:
            direction = self.position - self.orientation
            direction = direction / np.linalg.norm(direction)
            self.move(direction)

        if keys[pg.K_d]:
            direction = np.cross(self.orientation - self.position, self.up)
            direction = direction / np.linalg.norm(direction)
            self.move(direction)

        # Rotation de la caméra
        if keys[pg.K_u]:
            axis = np.cross(self.orientation - self.position, self.up)
            self.orientation = rotate(self.orientation, axis, self.rotation_speed)

        if keys[pg.K_j]:
            axis = np.cross(self.orientation - self.position, self.up)
            self.orientation = rotate(self.orientation, axis, -self.rotation_speed)

        if keys[pg.K_h]:
            axis = self.up
            self.orientation = rotate(self.orientation, axis, self.rotation_speed)

        if keys[pg.K_l]:
            axis = self.up
            self.orientation = rotate(self.orientation, axis, -self.rotation_speed)

        # Mise à jour de la matrice de vue
        self.view_matrix = self.get_view_matrix()


