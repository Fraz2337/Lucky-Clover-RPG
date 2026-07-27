class Loot:
    def __init__(self, item, x, y):
        self.item = item
        self.x = x
        self.y = y
        self.size = 20
        self.colour = (255, 215, 0)
        self.collected = False

    def __repr__(self):
        return self.item.name
