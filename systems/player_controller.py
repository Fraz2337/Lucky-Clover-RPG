import pygame


def update_player_movement(player, keys, width, height):
    """
    Takes user input to control the player character.
    """

    if player.health <= 0:
        return
        
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

    player.x = max(0, min(player.x, width - player.size))
    player.y = max(0, min(player.y, height - player.size))