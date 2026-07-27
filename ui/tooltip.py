import pygame


def draw_item_tooltip(screen, font, hovered_item):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    bonuses = hovered_item.get_total_bonuses()
    damage = bonuses.get("damage", 0)

    lines = [
        hovered_item.name,
        f"Damage: +{damage}",
        f"Durability: {hovered_item.durability}",
        f"Quality: {hovered_item.quality}",
        hovered_item.short_description,
    ]

    if hovered_item.stackable:
        lines.append(f"Quantity: {hovered_item.quantity}")
    
    rendered_lines = [
        font.render(line, True, (255, 255, 255))
        for line in lines
    ]
    
    tip_width = max(line.get_width() for line in rendered_lines) +10
    tip_height = len(rendered_lines) * 30 +10
    
    tip_x = mouse_x + 15
    tip_y = mouse_y + 15

    pygame.draw.rect(screen, (20, 20, 20), (tip_x, tip_y, tip_width, tip_height))
    pygame.draw.rect(screen, (200, 200, 200), (tip_x, tip_y, tip_width, tip_height),2)
    for index, line_surface in enumerate(rendered_lines):
        screen.blit(line_surface, (tip_x + 5, tip_y + 5 + index * 30))