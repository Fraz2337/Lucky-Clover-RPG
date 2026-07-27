import pygame
import random

from entities.entity import Entity 
from entities.player import Player
from entities.goblin import Goblin

pygame.init()

#Screen Size
WIDTH = 1200
HEIGHT = 1000
#Inventory size
SLOT_SIZE = 50
SLOT_PADDING = 10
INVENTORY_X = 50
INVENTORY_Y = 50
INVENTORY_WIDTH = 500
INVENTORY_HEIGHT = 500
CHARACTER_X = 700
CHARACTER_Y = 80
CHARACTER_WIDTH = 450
CHARACTER_HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Henry RPG Game")

clock = pygame.time.Clock()
       



class Item:
    def __init__(self, name, damage=0, armour=0, slot=None, stackable=False, quantity=1, durability=100, quality=None, short_description="", bonuses=None):
        self.name = name
        self.damage = damage
        self.armour = armour
        self.slot = slot
        self.stackable = stackable
        self.quantity = quantity
        self.durability = durability
        self.quality = quality
        self.short_description = short_description
        self.bonuses = bonuses or {}
        self.forge_level = 0
        self.enchantments = []
        self.sockets = []
        self.owner = None
    
    def __repr__(self):
        if self.stackable:
            return f"{self.name} x{self.quantity}"
        return self.name
    
    def get_total_bonuses(self):
        return self.bonuses
    
class Loot:
    def __init__(self, item, x, y):
        self.item = item
        self.x = x
        self.y = y
        self.size = 20
        self.colour = (255, 215, 0)
        self.collected = False

    def __repr__(self):
        return self.item.name

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

GOBLIN_LOOT_TABLE = {
    "rusty_sword": 1.00, # item drop and drop chance
    "iron_sword": 1.00
}

def roll_loot(loot_table):
    dropped_items = []

    for item_id, drop_chance in loot_table.items():
        roll = random.random()

        if roll <= drop_chance:
            dropped_items.append(create_item(item_id))

    return dropped_items

## Item database to store all the items available in game!
ITEM_DATABASE = {
    "rusty_sword": {
        "name": "Rusty Sword",
        # "damage":2,
        "armour": 0,
        "slot": "weapon",
        "stackable": False,
        "durability": 100,
        "quality": "common",
        "short_description": "A weak but useful tool carried by novice adventurers.",
        "bonuses": {
            "damage": 2,
            "strength": 1,
        }
    },
    "iron_sword": {
        "name": "Iron Sword",
        "damage": 10,
        "armour": 0,
        "slot": "weapon",
        "stackable": False,
        "durability": 100,
        "quality": "good",
        "short_description": "A strong and reliable iron blade carred by novice adventurers.",
        "bonuses": {
            "damage": 8,
            "strength": 2,
        }
    },
    "health_potion": {
        "name": "Health Potion",
        "damage": 0,
        "armour": 0,
        "slot": None,
        "stackable": True,
    },
    "iron_ore": {
        "name": "Iron Ore",
        "damage": 0,
        "armour": 0,
        "slot": None,
        "stackable": True,
    },
}

def create_item(item_id):
    item_data = ITEM_DATABASE[item_id]

    return Item(
        name=item_data["name"],
        # damage=item_data["damage"],
        armour=item_data["armour"],
        slot=item_data["slot"],
        stackable=item_data["stackable"],
        durability=item_data["durability"],
        quality=item_data["quality"],
        short_description=item_data["short_description"],
        bonuses=item_data.get("bonuses", {})
    )
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

                if target_slot is not None and dragging_item.slot == target_slot:
                    equipped_item = player.equipment[target_slot]

                    player.equipment[target_slot] = dragging_item
                    print("VALID DROP")
                    print("Target slot:", target_slot)
                    print("Dragging item:", dragging_item.name)
                    print("Item bonuses:", dragging_item.get_total_bonuses())
                    if equipped_item is not None:
                        player.inventory[dragging_index] = equipped_item
                    else:
                        player.inventory.pop(dragging_index)

                    player.calculate_stats()
                    print(player.final_stats)
                    print("Equipment:", player.equipment)
                    print("Equipment stats:", player.equipment_stats)
                    print("Final stats:", player.final_stats)

                else:
                    invalid_drop = True
            
            
                    
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

    # Rule-Based AI for goblin movement towards player.
    if goblin.health > 0:
        
        if goblin.x > player.x:
            goblin.x -= goblin.speed

        if goblin.x < player.x:
            goblin.x += goblin.speed

        if goblin.y > player.y:
            goblin.y -= goblin.speed

        if goblin.y < player.y:
            goblin.y += goblin.speed

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
    # Pick up loot
    for loot in loot_items:
        if not loot.collected:
            loot_rect = pygame.Rect(
                loot.x,
                loot.y,
                loot.size,
                loot.size
                )
            
            if player_rect.colliderect(loot_rect):

                if len(player.inventory) < player.inventory_limit:
                    loot.collected = True
                    #Stackable inventory conditionals
                    if loot.item.stackable:
                        found = False
                        
                        for inv_item in player.inventory:
                            if inv_item.name == loot.item.name:
                                inv_item.quantity += 1
                                found = True
                                break
                        if not found:
                            player.inventory.append(loot.item)
                    else:
                        player.inventory.append(loot.item)
                    
                    print(f"Picked up {loot.item.name}")
                    print(player.inventory)

                else:
                    print(f"Inventory full! Delete or drop an item first.")

    # player attack using key 1.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1] and player.health > 0:
        if player_rect.colliderect(goblin_rect):
            if current_time - player.last_attack_time >= player.attack_cooldown:
                damage = player.final_stats["damage"]
                goblin.health -= damage
                player.last_attack_time = current_time
                print(f"Player hits goblin for {damage} damage!")

    if goblin.health <= 0 and not goblin.reward_given:
        goblin.health = 0
        goblin.reward_given = True
        dropped_items = roll_loot(GOBLIN_LOOT_TABLE)
        
        for item in dropped_items:
            loot_items.append(
            Loot(item, goblin.x, goblin.y)
        )

        player.xp += goblin.xp_reward
        player.gold += goblin.gold_reward

        print(f"Goblin defeated! + {goblin.xp_reward} XP, +{goblin.gold_reward} gold")

        if player.xp >= player.xp_to_next_level:
            player.xp -= player.xp_to_next_level
            player.level += 1
            player.xp_to_next_level *= 2
            print(f"Level up! You are now level {player.level}")

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

    # Draw loot
    for loot in loot_items:
            if not loot.collected:
                pygame.draw.rect(
                    screen,
                    loot.colour,
                    (
                        loot.x,
                        loot.y,
                        loot.size,
                        loot.size
                    )
                )

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
    if goblin.health > 0:
        if player_rect.colliderect(goblin_rect):
            if current_time - goblin.last_attack_time >= goblin.attack_cooldown:
                damage = goblin.damage * (1 - player.defence_percent)
                player.health -= round(damage)
                if player.health < 0:
                    player.health = 0
                goblin.last_attack_time = current_time

                print(
                    f"Goblin hits for {round(damage)} damage!"
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
