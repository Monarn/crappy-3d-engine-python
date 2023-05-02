from object import *
import math

class Sphere(Object):

    def __init__(self, radius, lats, longs):
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

        self.vertices = vertices
        self.indices = indices

