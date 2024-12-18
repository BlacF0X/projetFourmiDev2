import pygame as pg
import random
import math


class Araignee:
    def __init__(self):
        self.position = (random.randint(0, 1500), random.randint(0, 800))
        self.image = pg.image.load(
            "C:/Users/Julien Falier/Downloads/3-2-spider-png-hd.png")

        # Redimensionner l'image pour la rendre plus petite (exemple de taille)
        self.image = pg.transform.scale(self.image, (50, 50))  # Taille réduite (50x50 pixels)

        self.rect = self.image.get_rect(center=self.position)
        self.visible = False
        self.apparition_time = None
        self.speed = 0.01  # Vitesse de déplacement
        self.direction = pg.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))  # Direction initiale
        self.velocity = pg.math.Vector2(0, 0)

    def apparaître(self):
        self.visible = True
        self.apparition_time = pg.time.get_ticks()

    def disparaitre(self):
        if self.visible and pg.time.get_ticks() - self.apparition_time > 10000:
            self.visible = False

    def deplacer(self):
        if self.visible:
            self.velocity += self.direction * self.speed  # Appliquer la direction et la vitesse
            self.position = (self.position[0] + self.velocity.x, self.position[1] + self.velocity.y)
            self.rect.center = self.position  # Mettre à jour la position de l'image

            # Gérer les collisions avec les bords de l'écran
            if self.position[0] < 0:
                self.position = (0, self.position[1])
                self.velocity.x = -self.velocity.x
            if self.position[0] > 1500:
                self.position = (1500, self.position[1])
                self.velocity.x = -self.velocity.x
            if self.position[1] < 0:
                self.position = (self.position[0], 0)
                self.velocity.y = -self.velocity.y
            if self.position[1] > 800:
                self.position = (self.position[0], 800)
                self.velocity.y = -self.velocity.y

            # Changer légèrement la direction pour un mouvement naturel
            if random.random() < 0.01:
                self.direction = pg.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

    def tuer_fourmis(self, liste_colonies):
        if self.visible:
            for col in liste_colonies:
                colonie = col[0]
                for fourmi in colonie.fourmis:
                    distance = math.sqrt((self.position[0] - fourmi.position[0]) ** 2 +
                                         (self.position[1] - fourmi.position[1]) ** 2)
                    if distance < 30:  # Si l'araignée est proche d'une fourmi, elle la tue
                        colonie.fourmis.remove(fourmi)

    def dessiner(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)  # Afficher l'image de l'araignée sans contour visible

