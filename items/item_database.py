from items.item import Item

def create_item(item_id):
    item_data = ITEM_DATABASE[item_id]

    return Item(
        name=item_data["name"],
        # damage=item_data["damage"],
        armour=item_data["armour"],
        slot=item_data["slot"],
        stackable=item_data["stackable"],
        durability=item_data["durability"],
        quality=item_data["quality"],
        short_description=item_data["short_description"],
        bonuses=item_data.get("bonuses", {})
    )

ITEM_DATABASE = {
    "rusty_sword": {
        "name": "Rusty Sword",
        # "damage":2,
        "armour": 0,
        "slot": "weapon",
        "stackable": False,
        "durability": 100,
        "quality": "common",
        "short_description": "A weak but useful tool carried by novice adventurers.",
        "bonuses": {
            "damage": 2,
            "strength": 1,
        }
    },
    "iron_sword": {
        "name": "Iron Sword",
        "damage": 10,
        "armour": 0,
        "slot": "weapon",
        "stackable": False,
        "durability": 100,
        "quality": "good",
        "short_description": "A strong and reliable iron blade carred by novice adventurers.",
        "bonuses": {
            "damage": 8,
            "strength": 2,
        }
    },
    "health_potion": {
        "name": "Health Potion",
        "damage": 0,
        "armour": 0,
        "slot": None,
        "stackable": True,
    },
    "iron_ore": {
        "name": "Iron Ore",
        "damage": 0,
        "armour": 0,
        "slot": None,
        "stackable": True,
    },
}