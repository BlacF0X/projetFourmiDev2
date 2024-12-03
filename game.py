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
nombre_de_fourmis = 500
quantite_nouriture = 2000
nbr_colonie = 0
liste_colonies.append(Colonie(Reine(),nombre_de_fourmis,numero=0))

frame_count = 0  # Ajout d'un compteur de frames
spawn = 0
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.fill((211, 192, 157))
    for colonie in liste_colonies:
        if colonie.nbr_fourmis <= 0:
            liste_colonies.remove(colonie)
        if colonie.nbr_fourmis // (nombre_de_fourmis // 10) < 1:
            col_circle = pg.draw.circle(screen, (99, 47, 26), colonie.position, 1)
        else:
            col_circle = pg.draw.circle(screen, (99, 47, 26), colonie.position,
                                        colonie.calculate_radius(nombre_de_fourmis))
        r = colonie.action(screen, liste_source)
        if r is not None:
            nbr_colonie += 1
            liste_colonies.append(Colonie(r, colonie.nbr_fourmis // 3,
                                          position=(random.randint(0, 1500), random.randint(0, 800)),
                                          numero=nbr_colonie))
            colonie.new_col()

        # Enregistrer les données toutes les 100 frames
        if frame_count % 100 == 0:
            colonie.save_data()

    for source in liste_source:
        col_circle = pg.draw.circle(screen, (0, 255, 0), source.position,
                                    source.quantite_nourriture // (quantite_nouriture // 10))

    source_spawn = random.random()
    if source_spawn >= 0.99 and len(liste_source) < 7:
        liste_source.append(Nourriture(quantite_nouriture))
        spawn = 1
    spawn += 1

    # Mise à jour de l'affichage
    pg.display.update()
    clock.tick(60)  # Limiter la boucle à 60 FPS

    frame_count += 1  # Incrément du compteur de frames



