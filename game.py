import pygame as pg
import random
import math
from sys import exit
from scripts.classes import *

pg.init()

# Configuration de l'écran
screen = pg.display.set_mode((1500, 800))
pg.display.set_caption('Ant Sim')
clock = pg.time.Clock()

# Liste des fourmis
liste_fourmis = []
for i in range(100):
    liste_fourmis.append(Ant(i))

# Boucle principale
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    # Remplir l'écran avec une légère transparence pour créer l'effet de traînée
    overlay = pg.Surface((1500, 800), pg.SRCALPHA)
    overlay.fill((211, 192, 157, 15))  # Couleur du fond avec faible opacité
    screen.blit(overlay, (0, 0))

    # Mettre à jour chaque fourmi
    for f in liste_fourmis:
        f.move()
        f.draw_trail(screen)  # Dessiner la traînée avant de dessiner la fourmi elle-même
        screen.blit(f.image, f.rect)  # Dessiner la fourmi

    # Mise à jour de l'affichage
    pg.display.update()
    clock.tick(60)  # Limiter la boucle à 60 FPS