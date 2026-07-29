from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class DragState:
    dragging_item: Optional[Any] = None
    dragging_index: Optional[int] = None
    drag_offset_x: int = 0
    drag_offset_y: int = 0
    invalid_drop: bool = False
    mouse_down: bool = False

    def start_drag(
            self,
            item,
            inventory_index,
            offset_x,
            offset_y,
    ):
        self.dragging_item = item
        self.dragging_index = inventory_index
        self.drag_offset_x = offset_x
        self.drag_offset_y = offset_y
        self.invalid_drop = False
        self.mouse_down = False

    def stop_drag(self):
        self.dragging_item = None
        self.dragging_index = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.mouse_down = False

    def mark_invalid_drop(self):
        self.invalid_drop = True

    def clear_invalid_drop(self):
        self.invalid_drop = False