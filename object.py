import numpy as np
import pygame as pg
import math
import operation as op

class Object:

    def __init__(self, camera, projection, color, vertices = np.array([]).astype(np.float64), indices = np.array([]).astype(np.int32)):
        self.camera = camera
        self.color = color
        self.projection = projection
        self.vertices = vertices
        self.indices = indices
        self.position = np.array([0,0,0,0]).astype(np.float64)
        self.transformed = np.array([])

    def translate(self, axis, value):
        self.position += axis.astype(np.float64)*value

    def parse_file(self, filename):
        vertices, indices = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex = [float(i) for i in line.split()[1:]]
                    vertex.append(1)
                    vertices.append(vertex)
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    indices.extend([int(face_.split('/')[0]) - 1 for face_ in faces_])
        self.vertices = np.array(vertices)
        self.indices = np.array(indices)



    def rotate(self, axis, angle):
        for i in range(len(self.vertices)):
            self.vertices[i] = op.rotate(self.vertices[i], axis, angle)


    def homogenize(self, point):
        v = np.array(point)
        w = v[3]
        return v / w


    def scale(self, axis, value):
        pass

    def project(self):
        self.transformed = []
        # Calculer la matrice de transformation de vue
        view_matrix = self.camera.get_view_matrix()
        # Calculer la matrice de transformation de projection
        projection_matrix = self.projection.projection_matrix
        # Appliquer la transformation de vue et de projection à tous les sommets
        for vertex in self.vertices:
            vertex = np.array(vertex)
            vertex = np.array(vertex).astype(np.float64)
            vertex += self.position
            # Transformer le sommet en coordonnées homogènes
            homogenized = self.homogenize(vertex)
            # Appliquer la transformation de vue
            view_transformed = -view_matrix @ homogenized
            # Appliquer la transformation de projection
            projection_transformed = projection_matrix @ view_transformed
            # Ajouter le sommet transformé à la liste des sommets transformés
            self.transformed.append(projection_transformed)
        # Appliquer la transformation pour passer en coordonnées écran
        self.transformed @= self.projection.to_screen_matrix


    def trace(self, window, color):
        self.project()
        for i in range(0, len(self.indices), 2):
            p1 = self.transformed[self.indices[i] - 1][:2]
            p2 = self.transformed[self.indices[i+1] - 1][:2]
            pg.draw.line(window, color, p1, p2)

    def controls(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_i]:
            self.translate(np.array([1,0,0,0]), .01)
        if keys[pg.K_k]:
            self.translate(np.array([1,0,0,0]), -.01)
        if keys[pg.K_j]:
            self.translate(np.array([0,1,0,0]), .01)
        if keys[pg.K_l]:
            self.translate(np.array([0,1,0,0]), -.01)

class Sphere(Object):

    def __init__(self, radius, lats, longs, camera, projection, color):
        super().__init__(camera, projection, color)
        self.color = color
        self.projection = projection
        self.camera = camera
        self.radius = radius
        self.lats = lats
        self.longs = longs
        

    def compute(self):
        vertices = []
        indices = []

        # create vertices
        for lat in range(self.lats+1):
            theta = lat * math.pi / self.lats
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)

            for lon in range(self.longs+1):
                phi = lon * 2 * math.pi / self.longs
                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)

                x = cos_phi * sin_theta
                y = cos_theta
                z = sin_phi * sin_theta

                vertices.append([self.radius * x, self.radius * y, self.radius * z, 1.0])

        # create triangles
        for lat in range(self.lats):
            for lon in range(self.longs):

                first = lat * (self.longs+1) + lon
                second = first + self.longs + 1

                indices.extend([first, second, first+1, second, second+1, first+1])

        # add triangles to close the sphere
        north_pole = len(vertices)
        vertices.append([0.0, self.radius, 0.0, 1.0])
        south_pole = len(vertices)
        vertices.append([0.0, -self.radius, 0.0, 1.0])

        for lon in range(self.longs):
            indices.extend([north_pole, lon+1, lon])
            indices.extend([south_pole, (self.lats-1) * (self.longs+1) + lon, (self.lats-1) * (self.longs+1) + lon+1])
            
        # adjust indices
        indices = [i+1 for i in indices]

        self.vertices = vertices
        self.indices = indices


class Axes(Object):

    def __init__(self, camera, projection, color):
        super().__init__(camera, projection, color = (255,0,0))
        self.vertices = np.array([
            [0,0,0,1],
            [1,0,0,1],
            [0,1,0,1],
            [0,0,1,1]
        ])

        self.indices = np.array([0,1,0,2,0,3])

        self.color = color
        self.projection = projection
        self.camera = camera
