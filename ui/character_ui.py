import pygame

CHARACTER_X = 700
CHARACTER_Y = 80
CHARACTER_WIDTH = 450
CHARACTER_HEIGHT = 600

equipment_layout = {
                #Left Side equipment slots
                "helmet": (720,120),
                "neck": (720, 170),
                "shoulders": (720, 220),
                "back": (720, 270),
                "chest": (720, 320),

                #Right Side equipment slots
                "gloves": (950, 170),
                "legs": (950, 220),
                "ring_1": (950, 270),
                "ring_2": (950, 320),
                "trinket_1": (950, 370),
                "trinket_2": (950, 420),

                #Bottom center equipment slots
                "weapon": (800, 500),
                "shield": (900, 500),
                "totem": (1000, 500)
            }

def draw_character(screen, player, font, dragging_item, invalid_drop):
    pygame.draw.rect(
        screen,
        (50, 50, 50),
        (CHARACTER_X, CHARACTER_Y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    )

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for slot, pos in equipment_layout.items():
        x, y = pos

        rect = pygame.Rect(x, y, 90, 30)

        highlight = False

        if dragging_item is not None and rect.collidepoint(mouse_x, mouse_y):
            highlight = True

        color = (100, 100, 100)

        if highlight:
            color = (0, 200, 0)

        pygame.draw.rect(
            screen,
            color,
            (x, y, 90, 30),
            2
        )

        item = player.equipment.get(slot)

        if item:
            text = font.render(item.name[:10], True, (255, 255, 255))
            screen.blit(text, (x + 5, y + 5))
        else:
            label = font.render(slot.replace("_", " ").title(), True, (150, 150, 150))
            screen.blit(label, (x + 5, y + 5))

    if invalid_drop:
        pygame.draw.rect(screen, (200, 0, 0), (CHARACTER_X, CHARACTER_Y, CHARACTER_WIDTH, CHARACTER_HEIGHT), 3)

    stats_x = CHARACTER_X + 25
    stats_y = CHARACTER_Y + 450
    line_height = 24

    stats_lines = []

    stat_labels = {
        "damage": "Damage",
        "health": "Health",
        "mana": "Mana",
        "accuracy": "Accuracy",
        "attack_speed": "Attack Speed",
        "crit_chance": "Crit Chance",
        "physical_defence": "AC",
        "magic_defence": "MAC"
    }
    
        
    stats_lines.append("Base Attributes")
    stats_lines.append("-"*20) # base attribute loop
    for key, value in player.base_stats.items():
        stats_lines.append(f"{key.replace("_", " ").title()}: {value:+}")
    stats_lines.append("")
    
    stats_lines.append("Equipment Bonuses")
    stats_lines.append("-"*20) # equipment attributes loop
    for key, value in player.equipment_stats.items():
        stats_lines.append(f"{key.replace("_", " ").title()}: {value:+}")
    stats_lines.append("")

    stats_lines.append("Final Stats")
    stats_lines.append("-"*20) #final stats loop
    for key, value in player.final_stats.items():
        if key in stat_labels:
            label = stat_labels[key]
        else:
            label = key.replace("_", " ").title()

        if key == "attack_speed":
            stats_lines.append(f"{label}: {value:.2f}")
        elif key == "crit_chance":
            stats_lines.append(f"{label}: {value:.1f}%")
        else:
            stats_lines.append(f"{label}: {value:+}")
            
    #     f"Damage: {player.final_stats['damage']}",
    #     f"Health: {player.final_stats['health']}",
    #     f"Mana: {player.final_stats['mana']}",
    #     f"Accuracy: {player.final_stats['accuracy']}",
    #     f"Attack Speed: {player.final_stats['attack_speed']:.2f}",
    #     f"Crit Chance: {player.final_stats['crit_chance']:.1f}%",
    #     f"AC: {player.final_stats['physical_defence']}",
    #     f"MAC: {player.final_stats['magic_defence']}",
    # ]

    for index, line in enumerate(stats_lines):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (stats_x, stats_y + index * line_height))