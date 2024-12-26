from pyray import *
import math
from .in_data import *

class Entity:
    def __init__(
        self, parent=None,
        name: str = "",
        position=Vector2(0, 0),
        scale=Vector2(1, 1),  
        rotation: float = 0,
        origin=Vector2(0.5, 0.5),
        color=WHITE,
        use_basis_model : bool = False,
        texture = "",
        use_basis_collider : bool = True,
        use_repel_collider : bool = False,
        
    ):
        self.parent = parent
        self.name = name
        self.type = "ENTITY"
        
        self.position = position
        self.scale = scale 
        self.rotation = rotation
        
        self.world_position = Vector2()
        self.world_scale = Vector2(1, 1)
        self.world_rotation = 0
        
        self.origin = origin
        self.color = color
        
        self.use_basis_model = use_basis_model
        self.texture = load_texture(texture) if texture != "" else None
        self.use_basis_collider = use_basis_collider
        self.use_repel_collider = use_repel_collider
        
        self.index : int = 0
        self.y_index : float = 0
        
        self.visible = True
        
        Entitys.append(self)
        Type_Entitys[name] = self
    
    def __repel__(self, other_enemy) -> None:
        """Repels this enemy from the other enemy if they collide."""
        
        # Calcular dirección de repulsión
        direction = Vector2(self.position.x - other_enemy.position.x, self.position.y - other_enemy.position.y)
        direction = vector2_normalize(direction)  # Normalizamos para obtener solo la dirección

        # Aplicar la fuerza de repulsión
        repulsion_strength = 0.2  # Ajusta este valor según la intensidad de la repulsión
        self.position.x += direction.x * repulsion_strength
        self.position.y += direction.y * repulsion_strength
        other_enemy.position.x -= direction.x * repulsion_strength
        other_enemy.position.y -= direction.y * repulsion_strength
    
    def IsCollider(self, filter : list = {}) -> bool : 
        Value : bool = False
        for e in Entitys :
            if e in filter : continue
            if check_collision_recs(e.Collider(), self.Collider()) : 
                Value = True
                break
        return Value
    
    def GetCollider(self, filter : list = {}):
        Value = None
        for e in Entitys :
            if e in filter : continue
            if check_collision_recs(e.Collider(), self.Collider()) : 
                Value = e
                break
        return Value
    
    def Collider(self) -> Rectangle: 
        if self.use_basis_collider == False : return None

        scale_x = self.world_scale.x * 100
        scale_y = self.world_scale.y * 100
        position_x = self.world_position.x - (scale_x / 2)
        position_y = self.world_position.y - (scale_y / 2)
        
        return Rectangle(
            position_x, position_y, scale_x, scale_y
        )
        
    
    def Update(self, dt):
        if self.parent:
            # 1. Obtener las propiedades del padre (posición y rotación mundial)
            parent_position = self.parent.world_position
            parent_rotation = self.parent.world_rotation
            parent_scale = self.parent.world_scale

            # 2. Rotar la posición local del hijo alrededor del origen del padre según la rotación del padre
            rotated_position = vector2_rotate(self.position, math.radians(parent_rotation))  # Rotación correcta respecto al origen del padre

            # 3. Ajustar la posición mundial del hijo con respecto al padre
            self.world_position.x = parent_position.x + rotated_position.x * parent_scale.x
            self.world_position.y = parent_position.y + rotated_position.y * parent_scale.y
            
             # 4. Controlar la velocidad de la rotación (ajustar factor para desacelerar la rotación)
            self.world_rotation = parent_rotation+self.rotation

            # 5. Escala acumulada entre la escala del padre y la del hijo
            self.world_scale.x = parent_scale.x * self.scale.x
            self.world_scale.y = parent_scale.y * self.scale.y
        else:
            # Si no tiene padre, la posición mundial es la misma que la local
            self.world_position = self.position
            self.world_rotation = self.rotation
            self.world_scale = self.scale
        
        if self.use_repel_collider :
            e = self.GetCollider(filter={self,})
            if e : 
                self.__repel__(e) 
        
        self.y_index = self.world_position.y
    
    def Draw(self):
        
        """
        # Normalize the scale by multiplying by 100
        normalized_scale = Vector2(self.world_scale.x * 100, self.world_scale.y * 100)
        """
        
        if self.use_basis_model == False : return
        if not self.texture : 
            draw_rectangle_pro(
                Rectangle(
                    self.world_position.x, self.world_position.y,
                    self.world_scale.x * 100, self.world_scale.y * 100
                ),
                vector2_multiply(self.origin, Vector2(100, 100)),
                self.world_rotation,
                self.color
            )
        else : 
            draw_texture_pro(
                self.texture, 
                Rectangle(), 
                Rectangle(
                    self.world_position.x, self.world_position.y, self.world_scale.x * 100, self.world_scale.y * 100
                )
            )

        