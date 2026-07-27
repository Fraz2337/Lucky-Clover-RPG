class Item:
    def __init__(self, name, damage=0, armour=0, slot=None, stackable=False, quantity=1, durability=100, quality=None, short_description="", bonuses=None):
        self.name = name
        self.damage = damage
        self.armour = armour
        self.slot = slot
        self.stackable = stackable
        self.quantity = quantity
        self.durability = durability
        self.quality = quality
        self.short_description = short_description
        self.bonuses = bonuses or {}
        self.forge_level = 0
        self.enchantments = []
        self.sockets = []
        self.owner = None
    
    def __repr__(self):
        if self.stackable:
            return f"{self.name} x{self.quantity}"
        return self.name
    
    def get_total_bonuses(self):
        return self.bonuses