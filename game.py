import pygame as pg
import random
import math
from sys import exit
from scripts.classes import *

pg.init()



# Configuration de l'écran
screen = pg.display.set_mode((1500, 800))
screen.fill((211,192,157))
pg.display.set_caption('Ant Sim')
clock = pg.time.Clock()

liste_colonies = []
liste_source = []
liste_colonies.append(Colonie(Reine(),500))

# Boucle principale
spawn = 1
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    screen.fill((211,192,157))
    for colonie in liste_colonies:
        if colonie.nbr_fourmis <= 0:
            liste_colonies.remove(colonie)
            pass
        col_circle = pg.draw.circle(screen,(99,47,26),colonie.position,colonie.nbr_fourmis // 50)
        r = colonie.action(screen,liste_source)
        if r != None:
            liste_colonies.append(Colonie(r,colonie.nbr_fourmis//2))
            colonie.nbr_fourmis = colonie.nbr_fourmis // 2
            colonie.remove()
    for source in liste_source:
        col_circle = pg.draw.circle(screen, (0,255,0), source.position, source.quantite_nourriture//100)
    source_spawn = random.random()
    if source_spawn >= 0.99 and len(liste_source) < 5:
        liste_source.append(Nourriture(1500))
        spawn = 1
    spawn += 1

    # Mise à jour de l'affichage
    pg.display.update()
    clock.tick(60)  # Limiter la boucle à 60 FPS