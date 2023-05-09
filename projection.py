import math
import numpy as np

class Projection:

    def __init__(self, render):
        near = render.camera.nPlan
        far = render.camera.fPlan
        right = math.tan(render.camera.w_FOV)
        left = -right
        top = math.tan(render.camera.FOV/2)
        bottom = -top

        self.projection_matrix = np.array([
            [(2*near)/(right-left), 0, (right+left)/(right-left), 0],
            [0, (2*near)/(top-bottom), (top+bottom)/(top-bottom), 0],
            [0, 0, -(far+near)/(far-near), (-2*far*near)/(far-near)],
            [0, 0, -1, 0]
        ])

        HW, HH = render.h_width, render.h_height
        self.to_screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])
