import random


class Reine:
    def __init__(self, speed=1.0, vie=100.0, rep_rate=0.1, ratio_besoin=0.1, force=25.0):
        self.life = vie
        self.reproduction_rate = rep_rate
        self.speed = speed
        self.gene_change_chance = 0.1
        self.ratio = ratio_besoin
        self.besoin_nourriture = speed * ratio_besoin
        self.force = force

    def create_princess(self):
        return Reine(
            self.life + random.uniform(-self.gene_change_chance, self.gene_change_chance),
            self.speed + random.uniform(-self.gene_change_chance, self.gene_change_chance),
            self.reproduction_rate + (
                    random.uniform(-self.gene_change_chance, self.gene_change_chance) / 5),
            self.ratio + random.uniform(-self.gene_change_chance, self.gene_change_chance))
