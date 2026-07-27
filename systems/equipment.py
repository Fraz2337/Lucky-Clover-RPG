def equipment_inventory_item(player, inventory_index, target_slot):
    """
    Equip an inventory item into the requested equipment slot.
    
    Returns:
        bool: True if the item was equipped successfully.
    """

    if inventory_index is None:
        return False

    if inventory_index < 0 or inventory_index >= len(player.inventory):
        return False

    item = player.inventory[inventory_index]

    if item.slot != target_slot:
        return False

    previously_equipped_item = player.equipment[target_slot]

    player.equipment[target_slot] = item

    if previously_equipped_item is not None:
        player.inventory[inventory_index] = previously_equipped_item
    else:
        player.inventory.pop(inventory_index)

    player.calculate_stats()
    return True