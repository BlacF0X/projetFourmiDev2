import pygame as pg
import random

from scripts.classes.nourriture import Nourriture
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

        """
        Calcule le rayon de la colonie et le met à jour. Basé sur la quantité de fourmis

        Pré : nbr_fourmis doit être un int et strictement positif

        Post : retourne le rayon calculé

        """
        self.radius = self.nbr_fourmis // (nbr_fourmis // 10)
        return self.nbr_fourmis // (nbr_fourmis // 10)

    def new_col(self):

        """
        Divise le nombre de fourmis et la nourriture restante. Réduit donc la taille de la colonie.

        Pré : self.nbr_fourmis doit être un int strictement positif
              self.__stock_nourriture = doit être non nul

        Post : le nombre de fourmis est mis à jour
               le stock de nourriture est réduit de 90%


        """
        for i in range(self.nbr_fourmis - 1,self.nbr_fourmis // 3,-1):
            self.fourmis.pop(i)
        self.nbr_fourmis = len(self.fourmis)
        self.__stock_nourriture = self.__stock_nourriture // 10

    def remove_one(self):

        """
        Supprime une fourmi de la colonie

        Pre : la liste de fourmis doit contenir au moins une fourmi
              nbr_fourmis doit être strictement positif

        Post : Supprime la dernière fourmi de la liste des fourmis

        """
        self.fourmis.pop(self.nbr_fourmis - 1)
        self.nbr_fourmis -= 1

    def action(self, ecran, liste_nourriture=[],liste_col = []):
        """
        cette fonction fait toutes les actions pour la colonie et les fourmis afin de faire tourner la simulation
        PRE : - ecran est un ecran pygame sur lequel dessiné
              - liste_nourriture est une liste de sources de nourriture sous la forme [object source,int]
              - liste_colonies est une liste contenant les colonies de la simulation sous la forme [object colonie,int]
        POST : modifie les différents paramètres de la colonie ou des fourmis et/ou retourne  une nouvelle reine si une nouvelle colonie doit être créée
        """
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
                self.depot_action(liste_nourriture, f)
            else:
                if len(self.pos_enemy) == 0:
                    f.angers = False
                if not f.porte:
                    self.enemy_col_action(liste_col,f)
                    self.depot_action(liste_nourriture,f)
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
        print('enemy_pos:',self.pos_enemy)
        print('nombre de fourmis: ' + str(self.nbr_fourmis))
        print('stock de nourriture: ' + str(self.__stock_nourriture))
        print('nombre de larves: ' + str(len(self.larves)))
        return None

    def compute_princess_proba(self):

        """
        Calcule la probalité de création d'une autre reine en créant une princesse.

        Pre : stock de nourriture doit être un entier non nul
              le nombre de fourmi doit être positif
              et reine doit être une instance de la classe Reine


        Post : Retourne 0 ou 1 en fonction du résultat du calcul. 1 si nouvelle princesse, 0 si pas.
        """

        return self.reine.reproduction_rate *(self.__stock_nourriture / self.nbr_fourmis)

    def enemy_col_action(self,liste_colo,fourmi):
        '''
        cette fonction fait des checks pour chaque colonie de la simulation avec la fourmi et modifie le comportement de la foutmi en fonction
        PRE : - liste_colo est une liste contenant les colonies de la simulation sous la forme [object colonie,int]
              - fourmi est une instance de la classe fourmi
        POST : modifie le comportement de la fourmi si elle entre en contact avec une colonie ennemie
        '''
        for colonie in liste_colo:
            col = colonie[0]
            if fourmi.check_proximity(col,col.radius) and col != self:
                if col.position not in self.pos_enemy:
                    print('added')
                    self.pos_enemy.append(col.position)
                    colonie[1] += 1
                if col.reine.force >= self.reine.force:
                    self.remove_one()
                elif col.reine.force <= self.reine.force:
                    col.remove_one()
                if col.nbr_fourmis <= 0:
                    self.pos_enemy.remove(col.position)
                    colonie[1] -= 1


    def depot_action(self,liste_nour,fourmi):
        '''
        Cette fonction fait des checks pour chaque source de nourriture de la simulation avec la fourmi et modifie le comportement de la fourmi en fonction
        PRE : - liste_colo est une liste contenant les colonies de la simulation sous la forme [object source,int]
              - fourmi est une instance de la classe fourmi
        POST : modifie le comportement de la fourmi si elle entre en contact avec une source de nourriture
        '''
        for depot_nourriture in liste_nour:
            depot: Nourriture = depot_nourriture[0]
            if fourmi.check_proximity(depot, 15):
                if depot.position not in self.pos_nourriture and depot.quantite_nourriture > 0:
                    self.pos_nourriture.append(depot.position)
                    depot_nourriture[1] += 1
                fourmi.porte = True
                fourmi.color = (255, 0, 0)
                depot.remove_nourriture(fourmi.force)
                fourmi.destination = self.position
                if depot.quantite_nourriture <= 0 and depot.position in self.pos_nourriture:
                    depot_nourriture[1] -= 1
                    self.pos_nourriture.remove(depot.position)
                return None


    def f_porte_action(self,fourmi):
        '''
        cette fonction est la liste d'actiona réalisé si la fourmi porte de la nourriture
        PRE : fourmi est une instance de la classe fourmi
        POST : modifie les different attributs de la fourmi et son comportement
        '''
        fourmi.destination = self.position
        fourmi.move_to_dest()
        fourmi.color = (255, 0, 0)
        if fourmi.check_proximity(self):
            fourmi.porte = False
            fourmi.color = (0, 0, 0)
            self.__stock_nourriture += fourmi.force
            fourmi.life += fourmi.besoin_nourriture
            self.__stock_nourriture -= fourmi.besoin_nourriture

    def f_not_porte_action(self,fourmi):
        '''
        cette fonction est la liste d'actiona réalisé si la fourmi ne porte pas de nourriture
        PRE : fourmi est une instance de la classe fourmi
        POST : modifie les different attributs de la fourmi et son comportement
        '''
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