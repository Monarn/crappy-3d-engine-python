# Créé par szczepaniak, le 14/03/2023 en Python 3.7

import numpy as np
import pygame
from vect_operations import *
from camera import Camera

class Object:

    def define(self, vertices = [], indices = []):
        self.indices = indices
        self.vertices = vertices

    def project(self, T):
        transformed = []
        for point in self.vertices:
            transformed.append(T @ point)
        return transformed


    def rotate(self, angle, axis):
        axis = normalize(axis)
        rotation_matrix = np.zeros((4, 4))
        x, y, z = axis
        c = np.cos(angle)
        s = np.sin(angle)
        t = 1 - c
        rotation_matrix[0][0] = t * x ** 2 + c
        rotation_matrix[0][1] = t * x * y - s * z
        rotation_matrix[0][2] = t * x * z + s * y
        rotation_matrix[1][0] = t * x * y + s * z
        rotation_matrix[1][1] = t * y ** 2 + c
        rotation_matrix[1][2] = t * y * z - s * x
        rotation_matrix[2][0] = t * x * z - s * y
        rotation_matrix[2][1] = t * y * z + s * x
        rotation_matrix[2][2] = t * z ** 2 + c
        rotation_matrix[3][3] = 1
        for i in range(len(self.vertices)):
            self.vertices[i] = rotation_matrix @ np.array(self.vertices[i])

    def trace(self, transformed, window, color):
        window.fill((0,0,0))
        for i in range(0, len(self.indices), 3):
            p1 = transformed[self.indices[i] - 1][:2]
            p2 = transformed[self.indices[i+1] - 1][:2]
            p3 = transformed[self.indices[i+2] - 1][:2]
            pygame.draw.polygon(window, color, [p1, p2, p3])



