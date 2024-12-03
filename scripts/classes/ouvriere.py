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