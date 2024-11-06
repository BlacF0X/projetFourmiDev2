import pygame as pg
from scripts.classes import *
from sys import exit

pg.init()

screen = pg.display.set_mode((1500, 800))
screen.fill((211,192,157))

pg.display.set_caption('Ant sim')
clock = pg.time.Clock()

liste_fourmis = []
counter = 0
for i in range(500):
    liste_fourmis.append(ant(i))


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    screen.fill((211,192,157))
    for f in liste_fourmis:
        if counter % 5 == 0:
            f.move()
        screen.blit(f.surface, f.rect)
    pg.display.update()
    clock.tick(120)
    counter += 1
