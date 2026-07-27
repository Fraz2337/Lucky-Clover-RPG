import random

from items.item_database import create_item
from items.loot import Loot

def roll_loot(loot_table):
    """
    Roll each entry in a loot table and return the item that dropped.
    
    Args:
        loot_table: A dictionary containing item IDs and drop chances.
    
    Returns:
        list: The item objects that successfully dropped.
    """

    dropped_items = []

    for item_id, drop_chance in loot_table.items():
        roll = random.random()

        if roll <= drop_chance:
            dropped_items.append(create_item(item_id))

    return dropped_items


def award_enemy_rewards(player, enemy):
    """
    Award an enemy's XP and gold to the player.
    """

    player.xp += enemy.xp_reward
    player.gold += enemy.gold_reward

    print(
        f"{enemy.__class__.__name__} defeated! "
        f"{enemy.xp_reward} XP, "
        f"{enemy.gold_reward} gold"
    )


def process_level_up(player):
    """
    Process a player level-up when enough XP has been earned.
    
    Returns:
        bool: True if the player levelled up, otherwise False.
    """

    if player.xp < player.xp_to_next_level:
        return False

    player.xp -= player.xp_to_next_level
    player.level += 1
    player.xp_to_next_level *= 2

    print(f"Level up! You are now level {player.level}")

    return True


def process_enemy_death(player, enemy, loot_items, loot_table):
    """
    Process loot, rewards and levelling when an enemy dies.
    
    Returns:
        bool: True if the enemy's death was processed.
        False if the enemy is alive or was already processed.
    """

    if enemy.health > 0:
        return False

    if enemy.reward_given:
        return False

    enemy.health = 0
    enemy.reward_given = True

    dropped_items = roll_loot(loot_table)

    for item in dropped_items:
        loot_items.append(
            Loot(
                item=item,
                x=enemy.x,
                y=enemy.y,
            )
        )

    award_enemy_rewards(player, enemy)
    process_level_up(player)

    return True