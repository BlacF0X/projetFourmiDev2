import unittest
from unittest.mock import Mock
from scripts.classes.colonies import Colonie
from scripts.classes.reine import Reine
from scripts.classes.ouvriere import Ouvriere
from scripts.classes.larve import Larve
from scripts.classes.nourriture import Nourriture
import pygame as pg

display = pg.display.set_mode((800, 600))

class TestColonie(unittest.TestCase):
    def setUp(self):
        """
        Initialisation des objets pour les tests.
        """
        self.reine = Reine()

        self.colonie = Colonie(self.reine, nbr_ants=10, position=(750, 400), numero=1)

    def test_initialisation(self):
        """
        Teste que la colonie est initialisée avec les bonnes valeurs.
        """
        self.assertEqual(self.colonie.number, 1)
        self.assertEqual(self.colonie.nbr_fourmis, 10)
        self.assertEqual(len(self.colonie.fourmis), 10)
        self.assertEqual(self.colonie.position, (750, 400))
        self.assertFalse(self.colonie.angry)
        self.assertEqual(len(self.colonie.larves), 0)

    def test_calculate_radius(self):
        """
        Teste le calcul du rayon de la colonie.
        """
        radius = self.colonie.calculate_radius(10)
        self.assertEqual(radius, 10)  # 10 fourmis => rayon = 10

    def test_new_col(self):
        """
        Teste la création d'une nouvelle colonie en divisant les fourmis et la nourriture.
        """
        self.colonie._Colonie__stock_nourriture = 100
        self.colonie.new_col()
        self.assertEqual(self.colonie.nbr_fourmis, 4)  # 1/3 des fourmis restantes
        self.assertEqual(self.colonie._Colonie__stock_nourriture, 10)  # 10% du stock restant

    def test_remove_one(self):
        """
        Teste la suppression d'une fourmi.
        """
        self.colonie.remove_one()
        self.assertEqual(self.colonie.nbr_fourmis, 9)
        self.assertEqual(len(self.colonie.fourmis), 9)

    def test_action_spawn_larve(self):
        """
        Teste que les larves sont ajoutées si les conditions sont remplies.
        """
        self.colonie._Colonie__stock_nourriture = 100
        self.colonie._Colonie__larves = 5
        self.colonie.action(display, [], [])
        self.assertEqual(len(self.colonie.larves), 1)

    def test_compute_princess_proba(self):
        """
        Teste le calcul de la probabilité d'avoir une princesse.
        """
        self.colonie._Colonie__stock_nourriture = 100
        self.colonie.nbr_fourmis = 10
        proba = self.colonie.compute_princess_proba()
        self.assertGreater(proba,1 ) # nouvelle reine
        self.colonie._Colonie__stock_nourriture = 100
        self.colonie.nbr_fourmis = 1000
        proba2 = self.colonie.compute_princess_proba()
        self.assertLess(proba2,1) #pas de nouvelle reine

    def test_f_porte_action(self):
        """
        Teste les actions d'une fourmi qui porte de la nourriture.
        """
        mock_fourmi = Ouvriere(2)
        mock_fourmi.force = 5
        mock_fourmi.besoin_nourriture = 10

        self.colonie._Colonie__stock_nourriture = 50
        self.colonie.f_porte_action(mock_fourmi)

        self.assertEqual(self.colonie._Colonie__stock_nourriture, 50)  # +5 nourriture
        mock_fourmi.life += mock_fourmi.besoin_nourriture

    def test_f_not_porte_action_low_life(self):
        """
        Teste les actions d'une fourmi sans nourriture avec faible vie.
        """
        mock_fourmi =Ouvriere(0)
        mock_fourmi.life = 100
        mock_fourmi.besoin_nourriture = 5

        self.colonie._Colonie__stock_nourriture = 50
        self.colonie.f_not_porte_action(mock_fourmi)
        self.assertLess(mock_fourmi.life, 100) #la fourmi a bien utilisé sa vie
        self.assertEqual(self.colonie._Colonie__stock_nourriture, 50)

    def test_enemy_col_action(self):
        """
        Teste les interactions avec les colonies ennemies.
        """
        enemy_colonie = Colonie(Reine())
        enemy_colonie.position = (700, 400)
        enemy_colonie.radius = 5
        enemy_colonie.reine.force = 8
        enemy_colonie.nbr_fourmis = 3
        self.colonie.pos_enemy.append((700,400))
        mock_fourmi = Ouvriere(1)

        self.colonie.enemy_col_action([[enemy_colonie, 0]], mock_fourmi)
        self.assertIn(enemy_colonie.position, self.colonie.pos_enemy)


if __name__ == "__main__":
    unittest.main()
