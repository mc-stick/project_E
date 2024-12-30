from pyray import *
import math
from .in_data import *
from .entity import *

class TileMap(Entity) : 
    
    def __init__(
        self, parent=None, 
        name = "Tilemap", 
        position=Vector2(0,0), 
        scale=Vector2(1,1), 
        rotation = 0, 
        origin=Vector2(0.5,0.5), 
        color=WHITE, 
        texture="", 
        tile_size : Vector2 = Vector2(0,0),
        
        ):
        super().__init__(parent, name, position, scale, rotation, origin)
        
        self.color = color
        self.type = "TILEMAP"
        self.tile_size = tile_size
        self.texture = load_texture(texture) if texture != "" else None
        self.tile = {
        }
        self.save_tile = {}
        
        
        
    def AddTile(self, tile_position : Vector2, texture_cords : Vector2):
        self.tile[f"({tile_position.x, tile_position.y})"] = {
            "tile_position" : Vector2(tile_position.x * self.tile_size.x, tile_position.y * self.tile_size.y) ,
            "texture_cords" : Vector2(texture_cords.x * self.tile_size.x, texture_cords.y * self.tile_size.y),
        } 
        
    def RemoveTile(self, tile_position : Vector2) :
        name = f"({tile_position.x, tile_position.y})"
        if name in self.tile :
            self.tile.pop(f"({tile_position.x, tile_position.y})")

    def Draw(self):
 
        if self.texture :
            for tile in self.tile.values():
                draw_texture_pro(
                    self.texture,
                    Rectangle(
                        tile["texture_cords"].x, tile["texture_cords"].y, 
                        self.tile_size.x, self.tile_size.y
                    ),
                    Rectangle(
                        (self.scale.x *tile["tile_position"].x) + self.world_position.x, (self.scale.x *tile["tile_position"].y) + self.world_position.y, 
                        (self.scale.x * self.tile_size.x), (self.scale.y * self.tile_size.y)
                    ),
                    vector2_multiply(self.origin, self.tile_size),
                    self.world_rotation,
                    self.color
                )
                