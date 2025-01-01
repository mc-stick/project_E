from pyray import *
import math
from .in_data import *
from .entity import *
from .collider import *

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
        use_collider : bool = True,
        vector_distance_to_sort : Vector2 = Vector2(0,0),
        min_activation_distance : float = 0 ,
        use_basic_model_to_collider = False, 
        
        ):
        super().__init__(parent, name, position, scale, rotation, origin, vector_distance_to_sort, min_activation_distance)
        
        self.color = color
        self.type = "TILEMAP"
        self.tile_size = tile_size
        self.texture = load_texture(texture) if texture != "" else None
        self.tile = {
        }
        self.save_tile = {}
        self.vector_distance_to_sort : Vector2 = vector_distance_to_sort
        self.min_activation_distance : float = min_activation_distance
        self.use_basic_model_to_collider = use_basic_model_to_collider
        self.use_collider = use_collider
        
        
    def AddTile(self, tile_position : Vector2, texture_cords : Vector2):
        
        position = Vector2(
            (self.scale.x *(tile_position.x * self.tile_size.x)) + self.world_position.x, (self.scale.x *(tile_position.y * self.tile_size.y)) + self.world_position.y
        )
        
        if self.use_collider :
            self.tile[f"({tile_position.x, tile_position.y})"] = {
                "tile_position" : position ,
                "texture_cords" : Vector2(texture_cords.x * self.tile_size.x, texture_cords.y * self.tile_size.y),
                "collider" : Collider(
                    parent=self.parent, name="slopt", position=position, 
                    use_basic_model=self.use_basic_model_to_collider, 
                    size=Vector2((self.scale.x * self.tile_size.x), (self.scale.y * self.tile_size.y)),
                    min_activation_distance=self.min_activation_distance
                    )
                } 
        else:
            self.tile[f"({tile_position.x, tile_position.y})"] = {
                "tile_position" : position ,
                "texture_cords" : Vector2(texture_cords.x * self.tile_size.x, texture_cords.y * self.tile_size.y),
                } 
        
    def RemoveTile(self, tile_position : Vector2) :
        name = f"({tile_position.x, tile_position.y})"
        if name in self.tile :
            self.tile.get(name)["collider"].Delect()
            self.tile.pop(f"({tile_position.x, tile_position.y})")

    def Update(self, dt):
        if self.use_collider :
            for tile in self.tile.values():
                tile["collider"].vector_distance_to_sort = self.vector_distance_to_sort
        return super().Update(dt)
    
    def Draw(self):
 
        if self.texture :
            for tile in self.tile.values():
                dis = vector2_distance(tile["tile_position"], self.vector_distance_to_sort)
                if dis <= self.min_activation_distance or self.min_activation_distance == 0:
                    draw_texture_pro(
                        self.texture,
                        Rectangle(
                            tile["texture_cords"].x, tile["texture_cords"].y, 
                            self.tile_size.x, self.tile_size.y
                        ),
                        Rectangle(
                            tile["tile_position"].x, tile["tile_position"].y, 
                            (self.scale.x * self.tile_size.x), (self.scale.y * self.tile_size.y)
                        ),
                        vector2_multiply(self.origin, self.tile_size),
                        self.world_rotation,
                        self.color
                    )
                