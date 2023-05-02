import pygame
import numpy as np
from object import Object
from camera import Camera   
from sphere import Sphere
from vect_operations import *

pygame.init()

clock = pygame.time.Clock()

width, height = 800,600
color = [235, 25, 113]

sphere = Sphere(100, 10, 10)
sphere.define()
sphere.compute()

pygame.display.set_caption(u'Pyramid')
window = pygame.display.set_mode((width, height))

run = True

camera = Camera( [1, 1, 1], [-0, 0, -1], [0, 5, 0], np.pi/2, width/height, 0.1, 100)

i = 0



while run:

    i = i + 0.01

    color[0] = abs((np.sin(i) * (255 + i * 100) % 255))
    color[1] = abs((np.sin(i+0.3) * (135 + i * 100) % 255))
    color[2] = abs((np.sin(i+0.25) * (75 + i * 100) % 255))

    key = pygame.key.get_pressed()

    camera.handle_events()
    camera.zoom()

    try:
        if key[pygame.K_UP]:
            sphere.radius -= 1 
            sphere.compute()
        elif key[pygame.K_DOWN]:
            sphere.radius += 1 
            sphere.compute()

        if key[pygame.K_LALT] and key[pygame.K_LEFT]:
            sphere.lats -= 1
            sphere.compute()
        if key[pygame.K_LALT] and key[pygame.K_RIGHT]:
            sphere.lats += 1
            sphere.compute()

        if key[pygame.K_LCTRL] and key[pygame.K_LEFT]:
            sphere.longs -= 1
            sphere.compute()
        if key[pygame.K_LCTRL] and key[pygame.K_RIGHT]:
            sphere.longs += 1
            sphere.compute()

        if key[pygame.K_a]:
            sphere.rotate(np.pi/60, [0,1,0])
        if key[pygame.K_e]:
            sphere.rotate(-np.pi/60, [0,1,0])
    
    except ZeroDivisionError:
        pass
        

    sphere.rotate(np.pi/100, [1,0,0])
    sphere.rotate(np.pi/500, [0,1,0])
    sphere.rotate(np.pi/250, [0,0,1])

    # Récupérer les matrices de projection et de vue de la caméra
    
    V = camera.get_view_matrix()
    P = camera.get_proj_matrix()

    T = V @ P

    # Appliquer la transformation à chaque point de la pyramide
    trans = sphere.project(T)

    # # Dessiner chaque point de la pyramide
    sphere.trace(trans, window, color)


    # Rafraîchir la fenêtre
    pygame.display.update()

    # Gérer les événements de la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # Limiter le nombre de FPS pour réduire l'utilisation CPU/GPU
    clock.tick(30)

    print(camera.position)
    
# Quitter Pygame
pygame.quit()