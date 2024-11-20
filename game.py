import pygame as pg
import random
import math
from sys import exit

from projetFourmiDev2.reine import Reine
from scripts.classes import *

pg.init()



# Configuration de l'écran
screen = pg.display.set_mode((1500, 800))
screen.fill((211,192,157))
pg.display.set_caption('Ant Sim')
clock = pg.time.Clock()

liste_colonies = []
liste_source = []
nombre_de_fourmis = 1500
quantite_nouriture = 15000
liste_colonies.append(Colonie(Reine(),nombre_de_fourmis))

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

        col_circle = pg.draw.circle(screen,(99,47,26),colonie.position,colonie.nbr_fourmis//(nombre_de_fourmis//10))
        r = colonie.action(screen,liste_source)
        if r is not None:
            print(r)
            liste_colonies.append(Colonie(r,colonie.nbr_fourmis//3,position=(random.randint(0,1500),random.randint(0,800))))
            colonie.nbr_fourmis = colonie.nbr_fourmis // 3
            colonie.new_col()
    for source in liste_source:
        col_circle = pg.draw.circle(screen, (0,255,0), source.position, source.quantite_nourriture//(quantite_nouriture//10))
    source_spawn = random.random()
    if source_spawn >= 0.99 and len(liste_source) < 5:
        liste_source.append(Nourriture())
        spawn = 1
    spawn += 1

    # Mise à jour de l'affichage
    pg.display.update()
    clock.tick(60)  # Limiter la boucle à 60 FPS