import numpy as np
import pygame as pg
import operation as op

class Camera:
    def __init__(self, res, position = np.array([0,0,0,0]), orientation = np.array([0,5,0,0]), movement_speed=0.1, rotation_speed=0.1):
        self.position = position.astype(np.float32)
        self.res = res
        self.orientation = orientation.astype(np.float32)
        self.right = np.array([1, 0, 0, 0]).astype(np.float32)
        self.up = np.array([0, 1, 0, 0]).astype(np.float32)
        self.forward = np.array([0, 0, 1, 1]).astype(np.float32)
        self.movement_speed = movement_speed
        self.rotation_speed = rotation_speed
        self.nPlan = 0.1
        self.fPlan = 100
        self.FOV = np.pi / 3
        if self.res[1] != 0:
            self.w_FOV = self.res[0] / self.res[1]
        else:
            self.w_FOV = 16/9

        self.anglePitch = 0
        self.angleYaw = 0
        self.angleRoll = 0

    def get_view_matrix(self):
        R = self.right
        U = self.up
        D = self.forward
        return np.array([
            [R[0], R[1], R[2], -op.dot(R, self.position)],
            [U[0], U[1], U[2], -op.dot(U, self.position)],
            [D[0], D[1], D[2], -op.dot(D, self.position)],
            [0,0,0,1]
        ])

    def update_vectors(self):
        self.forward = np.array(self.orientation) - np.array(self.position)
        self.forward = op.normalize(self.forward)

        self.up = np.array(op.cross(self.forward, self.right))

        self.right = op.cross(self.up, self.forward)
        self.right = op.normalize(self.right)

    def move(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_q]:
            self.position -= self.movement_speed * self.right
        if keys[pg.K_d]:
            self.position += self.movement_speed * self.right
        if keys[pg.K_z]:
            self.position += self.movement_speed * self.forward
        if keys[pg.K_s]:
            self.position -= self.movement_speed * self.forward
        if keys[pg.K_a]:
            self.position += self.movement_speed * self.up
        if keys[pg.K_e]:
            self.position -= self.movement_speed * self.up









        



