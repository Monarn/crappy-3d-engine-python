import math
import numpy as np

def normalize(vec):
    norm = (vec[0]*vec[1]*vec[2])**(1/3)
    if norm == 0:
        return vec
    return vec / norm

def dot(vec1, vec2):
    return (vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2])

def cross(a, b):
    return np.array([a[1]*b[2] - a[2]*b[1],
                     a[2]*b[0] - a[0]*b[2],
                     a[0]*b[1] - a[1]*b[0],
                     0.0], dtype=np.float32)

def vector_sub(vec1, vec2):
    return [vec1[0] - vec2[0], vec1[1] - vec2[1], vec1[2] - vec2[2]]

def vector_add(vec1, vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2]]

def vector_mult(a, b):
    return np.array([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])

def vector_mult_by_scal(vec2, scal):
    return [scal * vec2[0], scal * vec2[1], scal * vec2[2]]

def rotate(vector, axis, angle):
    axis = np.array(normalize(axis))
    a = np.cos(angle / 2.0)
    b, c, d = -axis * np.sin(angle / 2.0)
    rotation_matrix = np.array([[a*a + b*b - c*c - d*d, 2*(b*c - a*d), 2*(b*d + a*c), 0],
                                [2*(b*c + a*d), a*a + c*c - b*b - d*d, 2*(c*d - a*b), 0],
                                [2*(b*d - a*c), 2*(c*d + a*b), a*a + d*d - b*b - c*c, 0],
                                [0, 0, 0, 1]])
    rotated_vector = np.dot(rotation_matrix, vector)
    return rotated_vector

def translate(pos):
    tx, ty, tz = pos
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ])


def rotate_x(a):
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(a), math.sin(a), 0],
        [0, -math.sin(a), math.cos(a), 0],
        [0, 0, 0, 1]
    ])


def rotate_y(a):
    return np.array([
        [math.cos(a), 0, -math.sin(a), 0],
        [0, 1, 0, 0],
        [math.sin(a), 0, math.cos(a), 0],
        [0, 0, 0, 1]
    ])


def rotate_z(a):
    return np.array([
        [math.cos(a), math.sin(a), 0, 0],
        [-math.sin(a), math.cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


