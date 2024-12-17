class Larve:
    def __init__(self, speed, life, ratio, force, tm_to_spawn=100 ):
        self.time_to_spawn = tm_to_spawn
        self.speed = speed
        self.life = life
        self.ratio = ratio
        self.force = force