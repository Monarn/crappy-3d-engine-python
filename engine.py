import numpy as np
import pygame as pg

from object import *
from camera import Camera

import math
import numpy as np
import time

class Projection:

    def __init__(self, render):
        near = render.camera.nPlan
        far = render.camera.fPlan
        right = math.tan(render.camera.w_FOV)
        left = -right
        top = math.tan(render.camera.FOV/2)
        bottom = -top

        m00 = 2 / (right - left)
        m11 = 2 / (top - bottom)
        m22 = (far + near) / (far - near)
        m32 = -2 * near * far / (far - near)

        self.projection_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])

        HW, HH = render.width/2, render.height/2
        self.to_screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])

class Renderer:

    def __init__(self, width = 1920, height = 1080, bg_color = [0,0,0]):
        pg.init()
        self.bg_color = bg_color
        self.res = self.width, self.height = width, height
        self.FPS = 25
        self.screen = pg.display.set_mode((self.res))
        self.clock = pg.time.Clock()
        self.camera = Camera(self.res)
        self.projection = Projection(self)
        self.objects = []
        pg.display.toggle_fullscreen()

    def create_obj(self, camera, projection, color, filename):
        new_obj = Object(camera, projection, color)
        new_obj.parse_file(filename)
        self.objects.append(new_obj)

    def create_sphere(self, radius, lat, long, color):
        new_obj = Sphere(radius, lat, long, self.camera, self.projection, color)
        new_obj.compute()
        self.objects.append(new_obj)

    def draw(self):
        for i in range(len(self.objects)):
            self.objects[i].trace(self.screen, self.objects[i].color)

    def run(self):
        axes = Axes(self.camera, self.projection, (255,0,0))
        while True:
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    break
            self.clock.tick(self.FPS)
            self.screen.fill(self.bg_color)
            self.draw()
            axes.trace(self.screen, axes.color)
            if keys[pg.K_u]:
                self.create_sphere(.3, 10, 10, (255, 0, 0))
            try:
                for i in range(len(self.objects)):
                    self.objects[i].rotate([0,1,0], np.pi/500)
                    self.objects[i].rotate([1,0,0], np.pi/300)
                    self.objects[0].controls()
            except IndexError:
                pass
            pg.display.flip()
            self.camera.move()
            


if __name__ == "__main__":
    app = Renderer(bg_color= [47, 12, 100])
    app.run()