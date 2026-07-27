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


pygame.init()

#Screen Size
WIDTH = 1200
HEIGHT = 1000


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
goblin = Goblin(500,300)
enemies = []
enemies.append(Goblin(500,300))
enemies.append(Goblin(700,100))
enemies.append(Goblin(200,500))

loot_items = []

font = pygame.font.SysFont(None, 36)

show_inventory = False
show_character = False
selected_item = None
selected_index = None
mouse_down = False
running = True
dragging_item = None
dragging_index = None
drag_offset_x = 0
drag_offset_y = 0
invalid_drop = False
dropped_successfully = False



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
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left click
                mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP and event.button ==1:
            invalid_drop = False
            dropped_successfully = False

            mouse_x, mouse_y = pygame.mouse.get_pos()

            if dragging_item is not None:
                target_slot = get_equipment_slot_at_mouse(mouse_x, mouse_y)

                equipped_successfully = False
                if target_slot is not None:
                    equipped_successfully = equipment_inventory_item(
                        player,
                        dragging_index,
                        target_slot,
                )

                if equipped_successfully:
                    print("VALID DROP")
                    print("Target slot:", target_slot)
                    print("Equipment:", player.equipment)
                    print("Final stats:", player.final_stats)

                invalid_drop = not equipped_successfully
            

                    
            # reset drag and mouse state       
            dragging_item = None
            dragging_index = None
            mouse_down = False

    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_down = True
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if show_inventory:
                slot_index = get_inventory_slot_at_mouse(player, mouse_x, mouse_y)

                if slot_index is not None and slot_index < len(player.inventory):
                    dragging_item = player.inventory[slot_index]
                    dragging_index = slot_index

                    row = slot_index // 5
                    col = slot_index % 5

                    slot_x = 175 + col * (SLOT_SIZE + SLOT_PADDING)
                    slot_y = 170 + row * (SLOT_SIZE + SLOT_PADDING)

                    drag_offset_x = mouse_x - slot_x
                    drag_offset_y = mouse_y - slot_y

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_i:
                show_inventory = not show_inventory
                
            if event.key == pygame.K_c:
                show_character = not show_character
            
            if event.key == pygame.K_ESCAPE:
                show_inventory = False
                show_character = False

    current_time = pygame.time.get_ticks() / 1000

    # Keyboard input
    if player.health > 0:
        
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

    update_enemy_ai(goblin, player)

    player_rect = pygame.Rect(
        player.x,
        player.y,
        player.size,
        player.size
    )

    goblin_rect = pygame.Rect(
        goblin.x,
        goblin.y,
        goblin.size,
        goblin.size
    )

    # player attack using key 1.
    keys = pygame.key.get_pressed()

    if keys[pygame.K_1]:
        player_attack(
            player,
            goblin,
            current_time,
            player_rect.colliderect(goblin_rect),
        )

    process_enemy_death(
        player,
        goblin,
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
    if goblin.health > 0:
        pygame.draw.rect(
            screen,
            goblin.colour,
            (goblin.x, goblin.y, goblin.size, goblin.size)
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
        draw_character(screen, player, font, dragging_item, invalid_drop)
        
            

    # goblin attack player if collide.
    enemy_attack(
        goblin,
        player,
        current_time,
        player_rect.colliderect(goblin_rect),
    )

    draw_hud(screen, player, font)

    # Draw tooltip
    if hovered_item is not None:
        draw_item_tooltip(screen, font, hovered_item)
        #print(f"Hovering over: {hovered_item.name}")

    if dragging_item is not None:
        draw_drag_item(screen, font, dragging_item, drag_offset_x, drag_offset_y)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
