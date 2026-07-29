import pygame

from systems.equipment import equipment_inventory_item

def handle_mouse_event(
        event,
        player,
        show_inventory,
        drag_state,
        get_inventory_slot_at_mouse,
        get_equipment_slot_at_mouse,
        slot_size,
        slot_padding,
):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        handle_left_mouse_down(
            player,
            show_inventory,
            drag_state,
            get_inventory_slot_at_mouse,
            slot_size,
            slot_padding,
        )

    elif event.type == pygame.MOUSEBUTTONUP and event.button ==1:
        handle_left_mouse_up(
            player,
            drag_state,
            get_equipment_slot_at_mouse,
        )

def handle_left_mouse_down(
        player,
        show_inventory,
        drag_state,
        get_inventory_slot_at_mouse,
        slot_size,
        slot_padding,
):
    drag_state.mouse_down = True

    if not show_inventory:
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()

    slot_index = get_inventory_slot_at_mouse(
        player,
        mouse_x,
        mouse_y,
    )

    if slot_index is None:
        return

    if slot_index >= len(player.inventory):
        return

    item = player.inventory[slot_index]

    row = slot_index // 5
    col = slot_index % 5

    slot_x = 175 + col * (slot_size + slot_padding)
    slot_y = 170 + row * (slot_size + slot_padding)

    offset_x = mouse_x - slot_x
    offset_y = mouse_y - slot_y

    drag_state.start_drag(
        item,
        slot_index,
        offset_x,
        offset_y,
    )

def handle_left_mouse_up(
        player,
        drag_state,
        get_equipment_slot_at_mouse,
):
    drag_state.clear_invalid_drop()

    if drag_state.dragging_item is None:
        drag_state.mouse_down = False
        return

    mouse_x, mouse_y = pygame.mouse.get_pos()

    target_slot = get_equipment_slot_at_mouse(
        mouse_x,
        mouse_y,
    )

    equipped_successfully = False

    if target_slot is not None:
        equipped_successfully = equipment_inventory_item(
            player,
            drag_state.dragging_index,
            target_slot,
        )

    if equipped_successfully:
        print("VALID DROP")
        print("Target slot:", target_slot)
        print("Equipment:", player.equipment)
        print("Final stats:", player.final_stats)
    else:
        drag_state.mark_invalid_drop()

    drag_state.stop_drag()