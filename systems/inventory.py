def add_item(player, item):
    """
    Add an item to the Player's inventory.
    
    Returns:
        True if the item was added successfully.
        False if the inventory is full.
    """

    if item.stackable:
        for inventory_item in player.inventory:
            if inventory_item.name == item.name:
                inventory_item.quantity += item.quantity
                return True

    if len(player.inventory) >= player.inventory_limit:
        return False

    player.inventory.append(item)
    return True

def collect_loot(player, loot):
    """
    Transfer a loot item's contents into the player's inventory.
    
    Returns:
        Bool: True when the loot was collected, otherwise False.
    """

    if loot.collected:
        return False

    if not add_item(player, loot.item):
        return False

    loot.collected = True
    return True
