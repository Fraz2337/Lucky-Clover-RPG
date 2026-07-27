from entities.entity import Entity

class Player(Entity):
    def __init__(self):
        super().__init__(
            x = 100,
            y = 100,
            size = 50,
            speed = 5,
            health = 100,
            damage = 10
        )

        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 25
        self.gold = 0
        self.inventory = []
        self.inventory_limit = 20
        self.attack_cooldown = 0.5
        self.last_attack_time = 0
        self.defence_percent = 0.10
        self.armour_slots = {
            "helmet": None,
            "chest": None,
            "legs": None,
            "boots": None,
            "gloves": None,
            "weapon": None,
            "shield": None,
        }
        self.equipment = {
            "helmet": None,
            "neck": None,
            "shoulders": None,
            "chest": None,
            "back": None,
            "legs": None,
            "gloves": None,
            "boots": None,
            "weapon": None,
            "shield_ranged": None,
            "ring_1": None,
            "ring_2": None,
            "trinket_1": None,
            "trinket_2": None,
        }
        self.base_stats = {
            "strength": 5,
            "dexterity": 5,
            "intelligence": 5,
            "vitality": 5,
            "luck": 1,
        }
        self.final_stats = {
            "damage": 0,
            "health": 0,
            "mana": 0,
            "accuracy": 0,
            "attack_speed": 0,
            "crit_chance": 0,
            "physical_defence": 0,
            "magic_defence": 0,
        }
        
        self.equipment_stats = {
            "strength": 0,
            "dexterity": 0,
            "intelligence": 0,
            "vitality": 0,
            "luck": 0,

            "damage": 0,
            "physical_defence": 0,
            "magic_defence": 0,
            "crit_chance": 0,
            "attack_speed": 0,
            "accuracy": 0,
        }
        self.calculate_stats()
    

    def calculate_stats(self):
        # reset equipment_stats to zero
        for key in self.equipment_stats:
            self.equipment_stats[key] = 0 

        # iterate bonuses and add to equipment_stats
        for item in self.equipment.values():
            if item is not None:
                for key, value in item.get_total_bonuses().items():
                    self.equipment_stats[key] += value 

        # combine base + equipment stats
        strength = self.base_stats["strength"] + self.equipment_stats["strength"]
        dexterity = self.base_stats["dexterity"] + self.equipment_stats["dexterity"]
        intelligence = self.base_stats["intelligence"] + self.equipment_stats["intelligence"]
        vitality = self.base_stats["vitality"] + self.equipment_stats["vitality"]
        luck = self.base_stats["luck"] + self.equipment_stats["luck"]

        # calculate final stats
        self.final_stats["damage"] = (
            10
            + strength * 2
            + self.equipment_stats["damage"]
        )
        self.final_stats["health"] = (
            100
            + vitality * 10
        )
        self.final_stats["mana"] = (
            50
            + intelligence * 10
        )
        self.final_stats["accuracy"] = (
            75
            + dexterity * 2
            + luck
            + self.equipment_stats["accuracy"]
        )
        self.final_stats["attack_speed"] = (
            1.0
            + dexterity * 0.02
            + self.equipment_stats["attack_speed"]
        )
        self.final_stats["crit_chance"] = (
            5
            + dexterity * 0.5
            + luck * 0.5
            + self.equipment_stats["crit_chance"]
        )
        self.final_stats["physical_defence"] = self.equipment_stats["physical_defence"]
        self.final_stats["magic_defence"] = self.equipment_stats["magic_defence"]
        

    def equip_item(self, item):
        if item.slot is None:
            print(f"{item.name} cannot be equipped.")
            return

        self.equipment[item.slot] = item
        self.calculate_stats()
        print(self.final_stats)
        print(f"Equipped {item.name} in {item.slot}")
    
    def get_total_damage(self):
        total_damage = self.damage

        weapon = self.equipment["weapon"]

        if weapon is not None:
            total_damage += weapon.damage

        return total_damage