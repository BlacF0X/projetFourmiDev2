import pygame as pg
import math
import random
import os

# Importation de chaque classe

from classes.colonies import Colonie
from classes.nourriture import Nourriture
from classes.reine import Reine

pg.init()

screen = pg.display.set_mode((1500, 800))
screen.fill((211, 192, 157))
pg.display.set_caption('Ant Sim')
clock = pg.time.Clock()

liste_colonies = []
liste_source = []
nombre_de_fourmis = 500
quantite_nouriture = 2000
nbr_colonie = 0
liste_colonies.append([Colonie(Reine(), nombre_de_fourmis, numero=0),0])
nuke_image = pg.image.load("images/nuke_logo.png")
nuke_image = pg.transform.scale(nuke_image,(20,20))

colonie_selectionnee = None

nuke_active = False
pause = False
simulation_speed = 2
button_click_time = None
clicked_button = None

def draw_button(x, y, width, height, text, border_color, fill_color=None, text_color=(0, 0, 0)):
    mouse_x, mouse_y = pg.mouse.get_pos()
    is_hovered = x <= mouse_x <= x + width and y <= mouse_y <= y + height
    border_width = 4 if is_hovered else 2

    if fill_color:
        pg.draw.rect(screen, fill_color, (x, y, width, height))

    pg.draw.rect(screen, border_color, (x, y, width, height), border_width)

    font = pg.font.Font(None, 28)
    label = font.render(text, True, text_color)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

def handle_buttons(mouse_pos):
    global pause, simulation_speed, button_click_time, clicked_button

    if 1300 <= mouse_pos[0] <= 1450 and 10 <= mouse_pos[1] <= 40:
        pause = not pause
        clicked_button = "pause"
        button_click_time = pg.time.get_ticks()

    elif 1300 <= mouse_pos[0] <= 1450 and 50 <= mouse_pos[1] <= 80:
        simulation_speed = min(simulation_speed + 1, 7)
        clicked_button = "accelerate"
        button_click_time = pg.time.get_ticks()

    elif 1300 <= mouse_pos[0] <= 1450 and 90 <= mouse_pos[1] <= 120:
        simulation_speed = max(simulation_speed - 1, 1)
        clicked_button = "slow_down"
        button_click_time = pg.time.get_ticks()

spawn = 1

def nuke_town(pos):
    for i in range(-800,600,1):
        if i < 0:
            pg.draw.circle(screen, (0, 119, 0), pos, math.sqrt(abs(i)))
        else:
            pg.draw.circle(screen, (255,255,255), pos, abs(i)*2)
        pg.display.update()
        if i < 0:
            pg.draw.circle(screen, (211, 192, 157), pos, math.sqrt(abs(i)))



def save_colonies(liste_colonies):
    """
    Sauvegarde les données de toutes les colonies dans un fichier texte en écrasant les anciennes données.
    PRE : liste colonies est une liste contenant les colonies de la simulation sous la forme [colonie object,int]
    POST : crée et modifie les fichier textes correspondant a chaques colonies
    """

    for col in liste_colonies:
        colonie = col[0]
        filename = f'data/data_col_{colonie.number}.txt'
        with open(filename, "a") as file:  # Mode "w" pour écraser
            file.write(f"Colonie {colonie.number} :\n")
            file.write(f"  Nombre de fourmis : {colonie.nbr_fourmis}\n")
            file.write(f"  Stock de nourriture : {colonie._Colonie__stock_nourriture}\n")
            file.write("\n")


for file in os.listdir('data'):
    os.remove(os.path.join('data', file))
while True:
    mouse_pos = pg.mouse.get_pos()
    colonie_hover = None

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_n:
                nuke_active = True
        elif event.type == pg.MOUSEBUTTONDOWN and nuke_active:
            nuke_town(mouse_pos)
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
    if nuke_active:
        screen.blit(nuke_image,mouse_pos)

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

        if not pause:
            r = colonie.action(screen, liste_source)
            if r is not None:
                nbr_colonie += 1
                liste_colonies.append(
                    Colonie(r, colonie.nbr_fourmis // 3, position=(random.randint(0, 1500), random.randint(0, 800)),
                            numero=nbr_colonie))
                colonie.new_col()
        r = colonie.action(screen, liste_source)
        if r is not None and len(liste_colonies) <= 7:
            nbr_colonie += 1
            print(r)
            liste_colonies.append([
                Colonie(r, colonie.nbr_fourmis // 3, position=(random.randint(0, 1500), random.randint(0, 800)),
                        numero=nbr_colonie),0])
            colonie.new_col()


    for source in liste_source:
        pg.draw.circle(screen, (0, 255, 0), source.position,
                       source.quantite_nourriture // (quantite_nouriture // 10))

    if not pause:
        source_spawn = random.random()
        if source_spawn >= 0.99 and len(liste_source) < 7:
            liste_source.append(Nourriture(quantite_nouriture))
            spawn = 1
        spawn += 1
        pg.draw.circle(screen, (0, 255, 0), source[0].position,
                       source[0].quantite_nourriture // (quantite_nouriture // 10))
        if source[0].quantite_nourriture <= 0 and source[1] <= 0:
            liste_source.remove(source)
    source_spawn = random.random()
    if source_spawn >= 0.99 and len(liste_source) < 7:
        liste_source.append([Nourriture(quantite_nouriture),0])
        spawn = 1
    spawn += 1


    if colonie_selectionnee:

        rect_width, rect_height = 200, 100
        rect_x = colonie_selectionnee.position[0] - rect_width // 2
        rect_y = colonie_selectionnee.position[1] - colonie_selectionnee.calculate_radius(
            nombre_de_fourmis) - rect_height - 10
        rect_x = max(0, min(rect_x, screen.get_width() - rect_width))
        rect_y = max(0, rect_y)

        pg.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))
        pg.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height), 2)


        font = pg.font.Font(None, 36)
        text = font.render(f'Colonie #{colonie_selectionnee.number}', True, (0, 0, 0))
        screen.blit(text, (rect_x + 10, rect_y + 10))
        text = font.render(f'Fourmis: {colonie_selectionnee.nbr_fourmis}', True, (0, 0, 0))
        screen.blit(text, (rect_x + 10, rect_y + 50))

    current_time = pg.time.get_ticks()

    pause_fill = (200, 200, 200) if clicked_button == "pause" and current_time - button_click_time < 500 else None
    accel_fill = (200, 200, 200) if clicked_button == "accelerate" and current_time - button_click_time < 500 else None
    slow_fill = (200, 200, 200) if clicked_button == "slow_down" and current_time - button_click_time < 500 else None

    draw_button(1300, 10, 150, 30, "Reprendre" if pause else "Pause", (0, 0, 0), pause_fill)
    draw_button(1300, 50, 150, 30, "Accélérer", (0, 0, 0), accel_fill)
    draw_button(1300, 90, 150, 30, "Ralentir", (0, 0, 0), slow_fill)

    if not pause:
        pg.time.delay(int(50 / simulation_speed))

    if spawn % 120 == 0:
        save_colonies(liste_colonies)
    pg.display.update()
    clock.tick(60)

