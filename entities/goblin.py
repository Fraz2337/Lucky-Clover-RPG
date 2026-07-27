from entities.entity import Entity

class Goblin(Entity):
    def __init__(self, x, y):
        super().__init__(
            x = x,
            y = y,
            size = 40,
            speed = 2,
            health = 30,
            damage = 20
        )

        self.spawn_x = x
        self.spawn_y = y

        self.detection_range = 250
        self.leash_range = 400

        self.state = "idle"
        
        self.attack_cooldown = 1.0
        self.last_attack_time = 0
        self.colour = (0, 180, 0)
        self.xp_reward = 25
        self.gold_reward = 10
        self.reward_given = False