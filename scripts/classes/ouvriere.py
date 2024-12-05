import random

class Ouvriere:
    def __init__(self, nbr, speed=1.0, vie=100.0, pos=[0, 0], ratio_besoin=0.1, force=28.0):
        self.life = vie
        self.speed = speed
        self.ratio_besoin = ratio_besoin
        self.position = pos
        self.force = force
        self.color = (0, 0, 0)
        self.besoin_nourriture = speed * ratio_besoin
        self.destination = pos
        self.porte = False
        self.numero = nbr
        self.direction = random.randint(0, 360)
        self.angers = False

    def move_to_dest(self):
        """
        Cette fonction fait bouger la fourmi vers sa destination en utilisant sa vitesse
        post : modifie la position de la fourmi self en la rapprochant de sa cible (self.cible)
        """
        dep_dir_x = 0
        dep_dir_y = 0
        if abs(self.destination[0] - self.position[0]) != 0:
            dep_dir_x = (self.destination[0] - self.position[0]) / abs(self.destination[0] - self.position[0])
        if abs(self.destination[1] - self.position[1]) != 0:
            dep_dir_y = (self.destination[1] - self.position[1]) / abs(self.destination[1] - self.position[1])
        if abs(self.destination[0] / self.position[0]) <= 2:
            dep_dist_x = self.speed + 0.1
        else:
            dep_dist_x = abs(self.destination[0] / self.position[0]) * self.speed
        if abs(self.destination[1] / self.position[1]) <= 2:
            dep_dist_y = self.speed + 0.1
        else:
            dep_dist_y = abs(self.destination[1] / self.position[1]) * self.speed
        self.position = [self.position[0] + (dep_dir_x * dep_dist_x), self.position[1] + (dep_dir_y * dep_dist_y)]
        if self.porte:
            self.life -= (self.besoin_nourriture * self.force) / (self.force * 10)
        else:
            self.life -= self.besoin_nourriture /10

    def random_move(self):
        """
        cette fonction fais bouger la fourmi de manière aléatoire vers une driection de base
        POST : modifie la position de la fourmi self en la rapprochant d'une cible définie aléatoirement via sa direction(self.direction)
        """
        self.color = (0, 0, 0)
        f_deplacement = [random.randint(1, 15), random.randint(1, 15)]
        self.direction += random.randint(-15, 15)
        if self.direction >= 360:
            self.direction -= 360
        elif self.direction < 0:
            self.direction += 360
        cadran = self.direction // 90
        dic = [(1, -1), (1, 1), (-1, 1), (-1, -1)]
        self.destination = [self.position[0] + (f_deplacement[0] * self.speed * dic[cadran][0]),
                            self.position[1] + (f_deplacement[1] * self.speed * dic[cadran][1])]
        self.move_to_dest()

    def check_proximity(self,cible,distance = 10):
        return abs(self.position[0] - cible.position[0]) < distance  and abs(self.position[1] - cible.position[1]) < distance
