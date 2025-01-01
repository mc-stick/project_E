from pyray import *
import math
from .in_data import *
from .entity import *
from .collider import *


class Body(Entity):
    def __init__(self, 
        parent, 
        name="Body", 
        position=Vector2(), 
        scale=Vector2(1, 1), 
        rotation=0, 
        origin=Vector2(0.5, 0.5),
        friction = 0,
        vector_distance_to_sort = Vector2(), 
        min_activation_distance = 0
        ):
        # Llamada al constructor de la clase base (Entity)
        super().__init__(parent, name, position, scale, rotation, origin, vector_distance_to_sort, min_activation_distance)
        
        self.type = "BODY"
        self.velocity: Vector2 = Vector2()  # Inicializa la velocidad a (0,0)
        self.friction = friction
    
    def MoveVelocity(self, dt):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt

    def ReloadVelocity(self):
        """Establece la velocidad de la entidad."""
        self.velocity = vector2_lerp(self.velocity, Vector2(), self.friction)

    
        
        
        