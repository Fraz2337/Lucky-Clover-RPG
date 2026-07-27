import pygame

def draw_drag_item(screen, font, dragging_item, drag_offset_x, drag_offset_y):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    x = mouse_x - drag_offset_x
    y = mouse_y - drag_offset_y

    w, h = 120,30

    pygame.draw.rect(screen,(30, 30, 30), (x, y, w, h))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, w, h),2)

    drag_text = font.render(
        dragging_item.name[:12],
        True,
        (255, 255, 255)
    )

    screen.blit(drag_text, (x +5, y + 5))