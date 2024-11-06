import random
import math
import pygame
class ant :
    def __init__(self,numero,ant_type = "test"):
        self.__num = numero
        self.__position = (750,400)
        self.__rotation = 0
        self.__type = ant_type
        self.__speed = 5
        self.image = 'scripts/imafes/ants.png'
        self.surface = pygame.image.load('scripts/imafes/ants.png')
        self.rect = self.surface.get_rect(center = self.__position)

    def move(self):
        new_rot = random.randrange(-15,15,1)
        print(self.__rotation)
        self.surface = pygame.transform.rotate(pygame.image.load(self.image),(self.__rotation + new_rot) - self.__rotation)
        self.__rotation += new_rot
        mvmt_Y = int(math.sin(self.__rotation)*self.__speed)
        mvmt_X = int(math.cos(self.__rotation)*self.__speed)
        self.__position = (self.__position[0] + mvmt_X,self.__position[1] + mvmt_Y)
        self.rect = self.surface.get_rect(center = self.__position)
