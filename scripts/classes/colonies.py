import pygame as pg
import random

# Importation des classes utilisées

from scripts.classes.reine import Reine
from scripts.classes.ouvriere import Ouvriere
from scripts.classes.larve import Larve

class Colonie:
    def __init__(self, reine: Reine, nbr_ants=0, position=(750, 400),numero = 0):
        self.number = numero
        self.nbr_fourmis = nbr_ants
        self.__stock_nourriture = 0
        self.position = position
        self.__larves = 0
        self.reine = reine
        self.radius = 10
        self.fourmis = []
        self.angry = False
        for i in range(self.nbr_fourmis):
            self.fourmis.append(
                Ouvriere(i, self.reine.speed, self.reine.life, self.position, ratio_besoin=self.reine.ratio,
                         force=self.reine.force))
        self.larves = []
        self.pos_nourriture = []
        self.pos_enemy = []
        self.larve_max = 50


    def calculate_radius(self,nbr_fourmis):
        self.radius = self.nbr_fourmis // (nbr_fourmis // 10)
        return self.nbr_fourmis // (nbr_fourmis // 10)

    def new_col(self):
        for i in range(self.nbr_fourmis - 1,self.nbr_fourmis // 3,-1):
            self.fourmis.pop(i)
        self.nbr_fourmis = len(self.fourmis)
        self.__stock_nourriture = self.__stock_nourriture // 10

    def remove_one(self):
        self.fourmis.pop(self.nbr_fourmis - 1)
        self.nbr_fourmis -= 1

    def action(self, ecran, liste_nourriture=[],liste_col = []):
        nourriture_mult = 1
        if self.__larves > 0:
            nourriture_mult += 0.15
        if self.__stock_nourriture > self.nbr_fourmis / 5:
            if self.nbr_fourmis > 500:
                princesse_chance = self.compute_princess_proba()
            else:
                princesse_chance = 0
            self.__stock_nourriture -= self.reine.reproduction_rate * nourriture_mult
            if princesse_chance > 1:
                print('new_reine')
                return self.reine.create_princess()
            elif len(self.larves) < self.larve_max:
                self.larves.append(Larve(
                    self.reine.speed + random.uniform(-self.reine.gene_change_chance, self.reine.gene_change_chance),
                    self.reine.life + random.uniform(-self.reine.gene_change_chance, self.reine.gene_change_chance),
                    self.reine.ratio + random.uniform(-self.reine.gene_change_chance, self.reine.gene_change_chance),
                    self.reine.force + random.uniform(-self.reine.gene_change_chance, self.reine.gene_change_chance)))
        for f in self.fourmis:
            pg.draw.circle(ecran, f.color, f.position, 1)
            if self.__stock_nourriture < 0:
                self.__stock_nourriture = 0
            if len(self.pos_nourriture) == 0:
                f.random_move()
                for depot_nourriture in liste_nourriture:
                    if abs(f.position[0] - depot_nourriture.position[0]) < 15 and abs(
                            f.position[1] - depot_nourriture.position[1]) < 15:
                        if depot_nourriture.position not in self.pos_nourriture:
                            self.pos_nourriture.append(depot_nourriture.position)
                        f.porte = True
                        f.color = (255, 0, 0)
                        depot_nourriture.quantite_nourriture -= f.force
                        f.destination = self.position
                        break
            else:
                if len(self.pos_enemy) == 0:
                    f.angers = False
                if not f.porte:
                    for col in liste_col:
                        if abs(f.position[0] - col.position[0]) < (col.radius//2) and abs(
                                f.position[1] - col.position[1]) < (col.radius//2) and col != self:
                            if col.position not in self.pos_enemy:
                                self.pos_enemy.append(col.position)
                            pass
                            if col.reine.force >= self.reine.force:
                                self.remove_one()
                            elif col.reine.force <= self.reine.force:
                                col.remove_one()
                            else:
                                f.life -= col.reine.force
                            if col.nbr_fourmis <=0 :
                                self.pos_enemy.remove(col.position)
                                liste_col.remove(col)
                    for depot_nourriture in liste_nourriture:
                        if abs(f.position[0] - depot_nourriture.position[0]) < 15 and abs(
                                f.position[1] - depot_nourriture.position[1]) < 15:
                            if depot_nourriture.position not in self.pos_nourriture:
                                self.pos_nourriture.append(depot_nourriture.position)
                            f.porte = True
                            f.color = (255, 0, 0)
                            depot_nourriture.quantite_nourriture -= f.force
                            f.destination = self.position
                            if depot_nourriture.quantite_nourriture <= 0:
                                liste_nourriture.remove(depot_nourriture)
                                self.pos_nourriture.remove(depot_nourriture.position)
                            break
                    self.f_not_porte_action(f)
                elif f.porte:
                    self.f_porte_action(f)
            if f.life <= 0:
                self.fourmis.remove(f)
                self.nbr_fourmis = len(self.fourmis)

        for l in self.larves:
            l.time_to_spawn -= 1
            if l.time_to_spawn == 0:
                self.larves.remove(l)
                self.fourmis.append(
                    Ouvriere(self.nbr_fourmis + 1, l.speed, l.life, pos=self.position, ratio_besoin=l.ratio))
                self.nbr_fourmis = len(self.fourmis)
        print()
        print('nombre de fourmis: ' + str(self.nbr_fourmis))
        print('stock de nourriture: ' + str(self.__stock_nourriture))
        print('nombre de larves: ' + str(len(self.larves)))
        return None

    def compute_princess_proba(self):
        """
        compute change of getting a princess
        :return:
        """
        return self.reine.reproduction_rate *(self.__stock_nourriture / self.nbr_fourmis)

    def f_porte_action(self,fourmi):
        fourmi.destination = self.position
        fourmi.move_to_dest()
        fourmi.color = (255, 0, 0)
        if abs(fourmi.position[0] - self.position[0]) <= 10 and abs(fourmi.position[1] - self.position[1]) <= 10:
            fourmi.porte = False
            fourmi.color = (0, 0, 0)
            self.__stock_nourriture += fourmi.force
            fourmi.life += fourmi.besoin_nourriture
            self.__stock_nourriture -= fourmi.besoin_nourriture

    def f_not_porte_action(self,fourmi):
        if fourmi.life <= 20:
            if fourmi.check_proximity(self,5):
                while fourmi.life <= 75 and fourmi.life >= 0:
                    if self.__stock_nourriture > 0:
                        fourmi.life += fourmi.besoin_nourriture * 10
                        self.__stock_nourriture -= fourmi.besoin_nourriture * 10
                    else:
                        fourmi.life -= (fourmi.besoin_nourriture / 5)
            else:
                fourmi.destination = self.position
                fourmi.move_to_dest()
        elif len(self.pos_enemy) > 0 and fourmi.check_proximity(self):
            dest = random.choice(self.pos_enemy)
            fourmi.destination = dest
            fourmi.angers = True
            fourmi.life += fourmi.besoin_nourriture * 10
            self.__stock_nourriture -= fourmi.besoin_nourriture * 10
            fourmi.color = (255, 0, 255)
            fourmi.move_to_dest()
        elif fourmi.angers:
            fourmi.color = (255, 0, 255)
            fourmi.move_to_dest()
        elif fourmi.check_proximity(self):
            dest = random.choice(self.pos_nourriture)
            fourmi.destination = dest
            fourmi.life += fourmi.besoin_nourriture * 10
            self.__stock_nourriture -= fourmi.besoin_nourriture * 10
            fourmi.color = (0, 0, 255)
            fourmi.move_to_dest()
        elif fourmi.destination not in self.pos_nourriture:
            fourmi.random_move()
        else:
            fourmi.move_to_dest()