class Larve:
    def __init__(self, speed, life, ratio, force, tm_to_spawn=100, reine=False, ):
        self.time_to_spawn = tm_to_spawn
        if reine:
            self.role = 'reine'
        else:
            self.role = 'ouvriere'
        self.speed = speed
        self.life = life
        self.ratio = ratio
        self.force = force