from pyray import *
import math
from .in_data import *
from .entity import *

class Mouse(Entity) : 
    def __init__(self, parent=None, name = "", position=..., scale=..., rotation = 0, origin=..., color=..., use_basis_model = False, texture="", use_basis_collider = True, use_repel_collider = False):
        super().__init__(parent, name, position, scale, rotation, origin, color, use_basis_model, texture, use_basis_collider, use_repel_collider)
        self.scale = Vector2(0.1, 0.1)
        self.name = "Mouse" + f"{len(Entity):003}"
        Entitys.append(self)
        
    def Update(self, dt):
        self.position = get_mouse_position()
        return super().Update(dt)
    