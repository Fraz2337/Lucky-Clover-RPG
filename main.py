import pygame

from entities.player import Player
from entities.goblin import Goblin

from ui.tooltip import draw_item_tooltip
from ui.hud import draw_hud
from ui.character_ui import draw_character
from ui.character_ui import equipment_layout
from ui.drag_drop import draw_drag_item
from ui.inventory_ui import draw_inventory
from ui.inventory_ui import (
    SLOT_SIZE,
    SLOT_PADDING
)

from systems.combat import player_attack, enemy_attack
from systems.inventory import collect_loot
from systems.equipment import equipment_inventory_item
from items.item_database import ITEM_DATABASE
from items.item_database import create_item
from systems.loot_system import process_enemy_death
from systems.enemy_ai import update_enemy_ai
from ui.hud import WIDTH, HEIGHT
from systems.player_controller import update_player_movement
from systems.input_handler import handle_keydown
from ui.drag_state import DragState
from systems.mouse_handler import handle_mouse_event




pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Henry RPG Game")

clock = pygame.time.Clock()



GOBLIN_LOOT_TABLE = {
    "rusty_sword": 1.00, # item drop and drop chance
    "iron_sword": 1.00
}


rusty_sword = create_item("rusty_sword")

player = Player()
# print("=== Initial Player Stats ===")
# print(player.final_stats)

enemies = [
    Goblin(500,300),
    Goblin(700,100),
    Goblin(200,500)
]

loot_items = []

font = pygame.font.SysFont(None, 36)

show_inventory = False
show_character = False
selected_item = None
selected_index = None
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
    # Event handling
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

    current_time = pygame.time.get_ticks() / 1000

    keys = pygame.key.get_pressed()

    update_player_movement(
        player,
        keys,
        WIDTH,
        HEIGHT
    )

    for enemy in enemies:
        update_enemy_ai(enemy, player)

    player_rect = pygame.Rect(
        player.x,
        player.y,
        player.size,
        player.size
    )

    for enemy in enemies:
        enemy_rect = pygame.Rect(
        enemy.x,
        enemy.y,
        enemy.size,
        enemy.size
    )

    # player attack using key 1.

    if keys[pygame.K_1]:
        for enemy in enemies:
            enemy_rect = pygame.Rect(
                enemy.x,
                enemy.y,
                enemy.size,
                enemy.size,
            )

            if player_rect.colliderect(enemy_rect):
                player_attack(
                    player,
                    enemy,
                    current_time,
                    True,
                )
                break

    for enemy in enemies:
        process_enemy_death(
            player,
            enemy,
            loot_items,
            GOBLIN_LOOT_TABLE,
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
                )
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
        drag_state.invalid_drop)
        
            

    # goblin attack player if collide.
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
        player_rect.colliderect(enemy_rect),
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
