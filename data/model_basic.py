from pyray import *
import math
from .in_data import *
from .entity import *


class ModelBasic(Entity):
    def __init__(
        self, parent, 
        name = "Entity", 
        position=Vector2(), 
        scale=Vector2(1, 1), 
        rotation = 0, 
        origin=Vector2(0.5, 0.5), 
        color : Color = WHITE,
        how_model : str = "RECTANGLE",
        dimension: float = 0, 
        direction: str = "VERTICAL",
        ):
        super().__init__(parent, name, position, scale, rotation, origin)

        self.color = color
        self.how_model = how_model
        self.dimension = dimension
        self.direction = direction
        
    def Draw(self):
        
        if self.how_model == "RECTANGLE" : 
            draw_rectangle_pro(
                Rectangle(
                    self.world_position.x, self.world_position.y, self.world_scale.x * 100, self.world_scale.y * 100
                ), Vector2(self.origin.x * 100, self.origin.y * 100), self.world_rotation, self.color
            )
        elif self.how_model == "CIRCLE" : 
            draw_circle_v(
                self.world_position, (self.world_scale.x + self.world_scale.y)/2, self.color
            )
        elif self.how_model == "CAPSULE" : 
            draw_capsule_2d(
                Capsule(self.world_position, (self.world_scale.x+self.world_scale.y)/2, dimension=self.dimension), self.color
            )
        
        return super().Draw()
    