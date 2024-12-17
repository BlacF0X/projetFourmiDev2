import unittest
from scripts.classes.larve import Larve
from scripts.classes.ouvriere import Ouvriere

class MockCible:

    def __init__(self, position):
        self.position = position


class test_larve(unittest.TestCase):
    def setUp(self):

        self.larve = Larve(speed=1.5, life=50, ratio=0.3, force=10, tm_to_spawn=80)

    def test_initialisation(self):

        self.assertEqual(self.larve.speed, 1.5)
        self.assertEqual(self.larve.life, 50)
        self.assertEqual(self.larve.ratio, 0.3)
        self.assertEqual(self.larve.force, 10)
        self.assertEqual(self.larve.time_to_spawn, 80)

    def test_default_time_to_spawn(self):

        larve_default = Larve(speed=1.0, life=40, ratio=0.2, force=5)
        self.assertEqual(larve_default.time_to_spawn, 100)

    def test_invalid_values(self):

        with self.assertRaises(ValueError):
            Larve(speed='tamerlaput', life=50, ratio=0.3, force=10)

        with self.assertRaises(ValueError):
            Larve(speed=1.5, life='cui', ratio=0.3, force=10)

        with self.assertRaises(ValueError):
            Larve(speed=1.5, life=50, ratio='aaaaaaaaaaaaaa', force=10)

        with self.assertRaises(ValueError):
            Larve(speed=1.5, life=50, ratio=0.3, force='oui')


class test_ouvriere(unittest.TestCase):
    def setUp(self):

        self.ouvriere = Ouvriere(nbr=1, speed=2.0, vie=100.0, pos=(0, 2), ratio_besoin=0.1, force=30.0)

    def test_initialisation(self):

        self.assertEqual(self.ouvriere.numero, 1)
        self.assertEqual(self.ouvriere.speed, 2.0)
        self.assertEqual(self.ouvriere.life, 100.0)
        self.assertEqual(self.ouvriere.position, [0, 2])
        self.assertEqual(self.ouvriere.ratio_besoin, 0.1)
        self.assertEqual(self.ouvriere.force, 30.0)
        self.assertEqual(self.ouvriere.color, (0, 0, 0))
        self.assertEqual(self.ouvriere.besoin_nourriture, 2.0 * 0.1)
        self.assertEqual(self.ouvriere.destination, (0,2 ))
        self.assertFalse(self.ouvriere.porte)
        self.assertIsInstance(self.ouvriere.direction, int)

    def test_move_to_dest(self):

        self.ouvriere.destination = (3, 0)
        self.ouvriere.move_to_dest()
        self.assertGreater(self.ouvriere.position[0], 0)
        self.assertEqual(self.ouvriere.position[1], 0)
        self.assertLess(self.ouvriere.life, 100.0)

    def test_random_move(self):

        initial_position = self.ouvriere.position[:]
        self.ouvriere.random_move()

        self.assertNotEqual(initial_position, self.ouvriere.position)

    def test_check_proximity(self):

        cible_proche = MockCible(position=(5, 5))
        cible_lointaine = MockCible(position=(100, 100))

        self.assertTrue(self.ouvriere.check_proximity(cible_proche, distance=10))
        self.assertFalse(self.ouvriere.check_proximity(cible_lointaine, distance=10))


if __name__ == "__main__":
    unittest.main()
