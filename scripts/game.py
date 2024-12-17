import pygame as pg
import math
import random

# Importation de chaque classe
from classes.colonies import Colonie
from classes.nourriture import Nourriture
from classes.reine import Reine
from classes.Araignee import Araignee

pg.init()

# Initialisation de l'écran
screen = pg.display.set_mode((1500, 800))
screen.fill((211, 192, 157))
pg.display.set_caption('Ant Sim')
clock = pg.time.Clock()

# Initialisation des variables
liste_colonies = []
liste_source = []
nombre_de_fourmis = 500
quantite_nourriture = 2000
nbr_colonie = 0
liste_colonies.append([Colonie(Reine(), nombre_de_fourmis, numero=0), 0])

colonie_selectionnee = None

spawn = 1

# Initialisation de l'araignée
araignee = Araignee()
araignee_spawned = False  # Indique si l'araignée est déjà apparue

while True:
    mouse_pos = pg.mouse.get_pos()
    colonie_hover = None

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            colonie_selectionnee = None
            for col in liste_colonies:
                colonie = col[0]
                distance = math.sqrt((mouse_pos[0] - colonie.position[0]) ** 2 +
                                     (mouse_pos[1] - colonie.position[1]) ** 2)
                if distance <= colonie.calculate_radius(nombre_de_fourmis):
                    colonie_selectionnee = colonie
                    print(f'Colonie numéro {colonie.number} : {colonie.nbr_fourmis} fourmis')

    screen.fill((211, 192, 157))

    # Apparition aléatoire unique de l'araignée
    if not araignee_spawned and random.random() < 0.01:
        araignee.apparaître()
        araignee_spawned = True

    # Déplacer l'araignée et la faire attaquer les fourmis
    araignee.deplacer()
    araignee.tuer_fourmis(liste_colonies)

    # Dessin de l'araignée
    araignee.dessiner(screen)
    araignee.disparaitre()

    # Gestion des colonies
    for col in liste_colonies:
        colonie = col[0]
        distance = math.sqrt((mouse_pos[0] - colonie.position[0]) ** 2 +
                             (mouse_pos[1] - colonie.position[1]) ** 2)
        if distance <= colonie.calculate_radius(nombre_de_fourmis):
            colonie_hover = colonie

        if colonie.nbr_fourmis <= 0:
            liste_colonies.remove(colonie)
        if colonie.nbr_fourmis // (nombre_de_fourmis // 10) < 1:
            pg.draw.circle(screen, (99, 47, 26), colonie.position, 1)
        else:
            if colonie == colonie_hover:
                pg.draw.circle(screen, (0, 0, 255), colonie.position,
                               colonie.calculate_radius(nombre_de_fourmis) + 5, 3)  # Contour doré
            pg.draw.circle(screen, (99, 47, 26), colonie.position, colonie.calculate_radius(nombre_de_fourmis))

        r = colonie.action(screen, liste_source)
        if r is not None:
            nbr_colonie += 1
            print(r)
            liste_colonies.append([Colonie(r, colonie.nbr_fourmis // 3, position=(random.randint(0, 1500), random.randint(0, 800)),
                                           numero=nbr_colonie), 0])
            colonie.new_col()

    # Gestion des sources de nourriture
    for source in liste_source:
        pg.draw.circle(screen, (0, 255, 0), source[0].position,
                       source[0].quantite_nourriture // (quantite_nourriture // 10))
        if source[0].quantite_nourriture <= 0 and source[1] <= 0:
            liste_source.remove(source)
    source_spawn = random.random()
    if source_spawn >= 0.99 and len(liste_source) < 7:
        liste_source.append([Nourriture(quantite_nourriture), 0])
        spawn = 1
    spawn += 1

    # Affichage de l'interface de la colonie sélectionnée
    if colonie_selectionnee:
        rect_width, rect_height = 200, 100
        rect_x = colonie_selectionnee.position[0] - rect_width // 2
        rect_y = colonie_selectionnee.position[1] - colonie_selectionnee.calculate_radius(nombre_de_fourmis) - rect_height - 10

        rect_x = max(0, min(rect_x, screen.get_width() - rect_width))
        rect_y = max(0, rect_y)

        pg.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))
        pg.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height), 2)

        font = pg.font.Font(None, 36)
        text = font.render(f'Colonie #{colonie_selectionnee.number}', True, (0, 0, 0))
        screen.blit(text, (rect_x + 10, rect_y + 10))
        text = font.render(f'Fourmis: {colonie_selectionnee.nbr_fourmis}', True, (0, 0, 0))
        screen.blit(text, (rect_x + 10, rect_y + 50))

    pg.display.update()
    clock.tick(60)
