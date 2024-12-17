class Larve:
    def __init__(self, speed, life, ratio, force, tm_to_spawn=100 ):
        self.time_to_spawn = float(tm_to_spawn)
        self.speed = float(speed)
        self.life = float(life)
        self.ratio = float(ratio)
        self.force = float(force)