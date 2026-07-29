import pygame

from systems.enemy_ai import update_enemy_ai
from systems.loot_system import process_enemy_death
from systems.combat import enemy_attack

def update_enemies(enemies, player):
    for enemy in enemies:
        update_enemy_ai(enemy, player)

def process_enemy_deaths(
        enemies,
        player,
        loot_items,
        loot_table,
):
    for enemy in enemies:
        process_enemy_death(
            player,
            enemy,
            loot_items,
            loot_table,
        )

def update_enemy_attacks(
        enemies,
        player,
        player_rect,
        current_time,
):
    for enemy in enemies:
        if enemy.health <= 0:
            continue

        enemy_rect = pygame.Rect(
            enemy.x,
            enemy.y,
            enemy.size,
            enemy.size,
        )

        enemy_attack(
            enemy,
            player,
            current_time,
            player_rect.colliderect(enemy_rect)
        )