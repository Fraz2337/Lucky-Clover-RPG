import pygame

def handle_keydown(event, show_inventory, show_character):
    """
    Handle one keyboard press and return the updated UI state.
    """

    if event.type == pygame.KEYDOWN:
    
                # if keys[pygame.K_e] and player.inventory:
                #             player.equip_item(player.inventory[0])
                #             player.calculate_stats()
    
                if event.key == pygame.K_i:
                    show_inventory = not show_inventory
                    
                elif event.key == pygame.K_c:
                    show_character = not show_character
                
                elif event.key == pygame.K_ESCAPE:
                    show_inventory = False
                    show_character = False

                return show_inventory, show_character