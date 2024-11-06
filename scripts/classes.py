import pygame as pg
import random
import math


# Classe Ant
class Ant:
    def __init__(self, numero, ant_type="test"):
        self.__num = numero
        self.__position = [750, 400]  # Position de départ
        self.__rotation = random.uniform(0, 360)  # Angle de rotation initial en degrés
        self.__type = ant_type
        self.__speed = 1.5  # Vitesse légèrement réduite pour un déplacement fluide
        self.image = pg.image.load('scripts/images/ants.png').convert_alpha()
        self.original_image = self.image  # Conserver l'image d'origine pour rotation
        self.rect = self.image.get_rect(center=self.__position)

        # Liste des positions pour la traînée
        self.trail = []
        self.max_trail_length = 20  # Longueur maximale de la traînée

    def move(self):
        # Changement d'angle progressif
        if random.random() < 0.1:
            new_rot = random.uniform(-25, 25)
            self.__rotation += new_rot
        else:
            self.__rotation += random.uniform(-5, 5)

        # Mise à jour de l'image en fonction de la rotation
        self.image = pg.transform.rotate(self.original_image, -self.__rotation)
        self.rect = self.image.get_rect(center=self.__position)

        # Calcul des nouvelles coordonnées de mouvement
        rad_rotation = math.radians(self.__rotation)
        mvmt_X = math.cos(rad_rotation) * self.__speed
        mvmt_Y = math.sin(rad_rotation) * self.__speed
        self.__position[0] += mvmt_X
        self.__position[1] += mvmt_Y

        # Ajouter la position actuelle à la traînée
        self.trail.append(tuple(self.__position))  # Ajouter en tant que tuple pour éviter les modifications
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)  # Supprimer la plus ancienne position si la traînée dépasse la longueur max

        # Limiter les fourmis dans les limites de l'écran
        if self.__position[0] < 0 or self.__position[0] > 1500:
            self.__rotation = 180 - self.__rotation
        if self.__position[1] < 0 or self.__position[1] > 800:
            self.__rotation = -self.__rotation

        # Mettre à jour la position du rectangle pour blit
        self.rect.center = self.__position

    def draw_trail(self, screen):
        # Couleur de base de la traînée
        base_color = (255, 0, 0)  # Rouge par exemple

        # Dessiner chaque position dans la traînée avec une opacité décroissante
        for i, pos in enumerate(self.trail):
            alpha = 255 * (i / len(self.trail))  # Opacité décroissante
            color = (*base_color[:3], int(alpha))  # Couleur avec transparence
            trail_surface = pg.Surface((5, 5), pg.SRCALPHA)  # Surface avec canal alpha
            trail_surface.fill(color)
            screen.blit(trail_surface, pos)