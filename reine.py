import random


class Reine:
    def __init__(self, speed=2.0, vie=100.0, rep_rate=0.7, ratio_besoin=0.1, force=22.0):
        self.life = vie
        self.reproduction_rate = rep_rate
        self.speed = speed
        self.gene_change_chance = 0.1
        self.ratio = ratio_besoin
        self.besoin_nourriture = speed * ratio_besoin
        self.force = force

    def create_princess(self):
        return Reine(
            self.speed + random.uniform(-self.gene_change_chance, self.gene_change_chance),
            self.life + random.uniform(-self.gene_change_chance, self.gene_change_chance),
            self.reproduction_rate + (
                    random.uniform(-self.gene_change_chance, self.gene_change_chance) / 5),
            self.ratio + random.uniform(-self.gene_change_chance, self.gene_change_chance),
            self.force + (random.uniform(-self.gene_change_chance, self.gene_change_chance)*5))

    def __str__(self):
        return f'vie : {self.life} || speed : {self.speed} || reproduction_rate : {self.reproduction_rate} || ratio : {self.ratio}'