import unittest
import random
from scripts.classes.reine import Reine

class TestReine(unittest.TestCase):
    def setUp(self):

        self.reine = Reine(speed=2.0, vie=100.0, rep_rate=0.7, ratio_besoin=0.1, force=22.0)
        random.seed(42)

    def test_initialisation(self):
        """Test que la reine est correctement initialisée avec les bonnes valeurs."""
        self.assertEqual(self.reine.speed, 2.0)
        self.assertEqual(self.reine.life, 100.0)
        self.assertEqual(self.reine.reproduction_rate, 0.7)
        self.assertEqual(self.reine.ratio, 0.1)
        self.assertEqual(self.reine.force, 22.0)

    def test_besoin_nourriture(self):
        """Test que le besoin de nourriture est correctement calculé."""
        self.assertEqual(self.reine.besoin_nourriture, 2.0 * 0.1)

    def test_create_princess(self):
        """Test que create_princess retourne une nouvelle reine avec des variations dans les gènes."""
        princess = self.reine.create_princess()

        # Test des variations dans les limites
        self.assertAlmostEqual(princess.speed, 2.0, delta=self.reine.gene_change_chance)
        self.assertAlmostEqual(princess.life, 100.0, delta=self.reine.gene_change_chance)
        self.assertAlmostEqual(princess.reproduction_rate, 0.7, delta=self.reine.gene_change_chance / 5)
        self.assertAlmostEqual(princess.ratio, 0.1, delta=self.reine.gene_change_chance)
        self.assertAlmostEqual(princess.force, 22.0, delta=self.reine.gene_change_chance * 5)

    def test_str_method(self):
        """Test que la méthode __str__ renvoie la bonne chaîne."""
        result = str(self.reine)
        expected = "vie : 100.0 || speed : 2.0 || reproduction_rate : 0.7 || ratio : 0.1"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()