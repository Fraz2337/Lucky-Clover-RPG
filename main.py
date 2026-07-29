import pygame

from entities.player import Player
from entities.goblin import Goblin

from items.loot_tables import GOBLIN_LOOT_TABLE


# from items.item_database import create_item
from systems.enemy_system import update_enemy_attacks, process_enemy_deaths, update_enemies, handle_player_attack

from systems.input_handler import handle_keydown
from systems.inventory import collect_loot
from systems.mouse_handler import handle_mouse_event
from systems.player_controller import update_player_movement


from ui.character_ui import (
    draw_character,
    equipment_layout,
)
from ui.drag_drop import draw_drag_item
from ui.drag_state import DragState
from ui.hud import WIDTH, HEIGHT, draw_hud
from ui.tooltip import draw_item_tooltip
from ui.inventory_ui import (
    SLOT_SIZE,
    SLOT_PADDING,
    draw_inventory,
)



pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Henry RPG Game")

clock = pygame.time.Clock()





# rusty_sword = create_item("rusty_sword")

player = Player()


enemies = [
    Goblin(500,300),
    Goblin(700,100),
    Goblin(200,500)
]

loot_items = []

font = pygame.font.SysFont(None, 36)

show_inventory = False
show_character = False
running = True
drag_state = DragState()


# Inventory logic click
def get_inventory_slot_at_mouse(player, mouse_x, mouse_y):
    inventory_x = 175
    inventory_y = 170

    for i in range(player.inventory_limit):
        row = i // 5
        col = i % 5

        slot_x = inventory_x + col * (SLOT_SIZE + SLOT_PADDING)
        slot_y = inventory_y + row * (SLOT_SIZE + SLOT_PADDING)

        slot_rect = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)

        if slot_rect.collidepoint(mouse_x, mouse_y):
            return i
    return None

# Equipment slot
def get_equipment_slot_at_mouse(mouse_x, mouse_y):
    for slot, pos in equipment_layout.items():
        x, y = pos

        slot_rect = pygame.Rect(x, y, 90, 30)

        if slot_rect.collidepoint(mouse_x, mouse_y):
            return slot
        
    return None

while running:
    
    current_time = pygame.time.get_ticks() / 1000
    keys = pygame.key.get_pressed()

    update_player_movement(
            player,
            keys,
            WIDTH,
            HEIGHT
        )

    player_rect = pygame.Rect(
            player.x,
            player.y,
            player.size,
            player.size
        )
    
    update_enemies(enemies, player)

    handle_player_attack(
        player,
        enemies,
        current_time,
        keys[pygame.K_1],
    )

    

    # if keys[pygame.K_1]:
    #     for enemy in enemies:
    #         enemy_rect = pygame.Rect(
    #             enemy.x,
    #             enemy.y,
    #             enemy.size,
    #             enemy.size,
    #         )

    #         if player_rect.colliderect(enemy_rect):
    #             player_attack(
    #                 player,
    #                 enemy,
    #                 current_time,
    #                 True,
    #             )
    #             break
    
        
    process_enemy_deaths(
        enemies,
        player,
        loot_items,
        GOBLIN_LOOT_TABLE,
    )

    # goblin attack player if collide.
    update_enemy_attacks(
        enemies,
        player,
        player_rect,
        current_time,
    )
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            show_inventory, show_character = handle_keydown(
                event,
                show_inventory,
                show_character,
            )

        handle_mouse_event(
            event,
            player,
            show_inventory,
            drag_state,
            get_inventory_slot_at_mouse,
            get_equipment_slot_at_mouse,
            SLOT_SIZE,
            SLOT_PADDING,
        )


    # Draw background
    screen.fill((30, 30, 30))

    # Draw player
    pygame.draw.rect(
        screen, # where to draw
        (255, 255, 255), # colour
        (player.x, player.y, player.size, player.size) # position and size
    )

    # Draw goblin
    for enemy in enemies:
        if enemy.health <= 0:
            continue

        pygame.draw.rect(
            screen,
            enemy.colour,
            (
                enemy.x,
                enemy.y,
                enemy.size,
                enemy.size,
            )
        )

    # Draw loot rendering
    for loot in loot_items:
        if loot.collected:
            continue

        pygame.draw.rect(
            screen,
            loot.colour,
            (
                loot.x,
                loot.y,
                loot.size,
                loot.size,
            ),
        )

    # Loot collection
    for loot in loot_items:
            if loot.collected:
                continue

            loot_rect = pygame.Rect(
                loot.x,
                loot.y,
                loot.size,
                loot.size
            )

            if player_rect.colliderect(loot_rect):
                if collect_loot(player, loot):
                    print(f"Picked up {loot.item.name}")
                else:
                    print(f"Inventory full! Delete or drop an item first.")

    # Display item tooltip
    hovered_item = None
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if show_inventory:
        slot_index = get_inventory_slot_at_mouse(player, mouse_x, mouse_y)

        if slot_index is not None and slot_index < len(player.inventory):
            hovered_item = player.inventory[slot_index]

    # Draw Inventory screen
    if show_inventory:
        draw_inventory(screen, player, font)

    # Draw Character screen
    if show_character:   
        draw_character(
            screen,
            player,
            font,
            drag_state.dragging_item,
            drag_state.invalid_drop,
        )
        
            

    

    draw_hud(screen, player, font)

    # Draw tooltip
    if hovered_item is not None:
        draw_item_tooltip(screen, font, hovered_item)
        #print(f"Hovering over: {hovered_item.name}")

    if drag_state.dragging_item is not None:
        draw_drag_item(
            screen,
            font,
            drag_state.dragging_item,
            drag_state.drag_offset_x,
            drag_state.drag_offset_y,
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
