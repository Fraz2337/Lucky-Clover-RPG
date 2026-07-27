import pygame

INVENTORY_X = 50
INVENTORY_Y = 50
INVENTORY_WIDTH = 500
INVENTORY_HEIGHT = 500
SLOT_SIZE = 50
SLOT_PADDING = 10

def draw_inventory(screen, player, font):

    pygame.draw.rect(
        screen,
        (50, 50, 50),
        (INVENTORY_X, INVENTORY_Y,
         INVENTORY_WIDTH,
         INVENTORY_HEIGHT)
    )

    inventory_x = 175
    inventory_y = 170

    for i in range(player.inventory_limit):

        row = i // 5
        col = i % 5

        slot_x = inventory_x + col * (SLOT_SIZE + SLOT_PADDING)
        slot_y = inventory_y + row * (SLOT_SIZE + SLOT_PADDING)

        pygame.draw.rect(
            screen,
            (150, 150, 150),
            (slot_x,slot_y,SLOT_SIZE,SLOT_SIZE),
            2
        )

        if i < len(player.inventory):

            item = player.inventory[i]

            if item.stackable:
                text = f"{item.name} x {item.quantity}"
            else:
                text = item.name

            surface = font.render(
                text[:12],
                True,
                (255,255,255)
            )

            screen.blit(
                surface,
                (slot_x+5,slot_y+15)
            )
