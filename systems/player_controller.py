import pygame
from ui.hud import WIDTH, HEIGHT

def update_player_movement(player, keys, width, height):
    """
    Takes user input to control the player character.
    """

    if player.health <= 0:
        return

    else:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_e] and player.inventory:
            player.equip_item(player.inventory[0])
            player.calculate_stats()

        if keys[pygame.K_w]:
            player.y -= player.speed

        if keys[pygame.K_s]:
            player.y += player.speed

        if keys[pygame.K_a]:
            player.x -= player.speed

        if keys[pygame.K_d]:
            player.x += player.speed

        if player.x < 0:
            player.x = 0

        if player.y < 0:
            player.y = 0

    if player.x > WIDTH - player.size:
        player.x = WIDTH - player.size

    if player.y > HEIGHT - player.size:
        player.y = HEIGHT - player.size