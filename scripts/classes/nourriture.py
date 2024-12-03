

class Nourriture:
    def __init__(self, quantite=3000):
        self.quantite_nourriture = quantite
        self.position = (random.randint(0, 1500), random.randint(0, 700))