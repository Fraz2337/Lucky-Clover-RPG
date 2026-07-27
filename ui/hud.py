#Screen Size
WIDTH = 1200
HEIGHT = 1000

def draw_hud(screen, player, font):
    health_text = font.render(
        f"Health: {player.health}",
        True,
        (255, 255, 255)
    )
    screen.blit(health_text, (10, 10))
    stats_text = font.render(
        f"Level: {player.level} XP: {player.xp}/{player.xp_to_next_level} Gold: {player.gold}",
        True,
        (255, 255, 255)
    )
    screen.blit(stats_text, (10, 45))

    if player.health == 0:
        game_over_text = font.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )
        screen.blit(game_over_text, (330, 280))