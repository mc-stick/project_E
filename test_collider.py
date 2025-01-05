from pyray import *
import math
from data import *



class Game(Engine):
    
    def __init__(self, window_size_x, window_size_y, name, use_y_index = False):
        super().__init__(window_size_x, window_size_y, name, use_y_index)
        set_target_fps(60)
        
        self.scena = Scena("prueba_collider")
        
        
        self.e = Entity(parent=self.scena, position=Vector2(0, 0), scale=Vector2(1, 1), rotation=0)
        self.collider = Collider(
            parent=self.e, use_basic_model=True, position=Vector2(0, 100), color=RED, size=Vector2(100, 100), how_collider="", origin=Vector2(0, 0)
        )
        self.collider_2 = Collider(
            parent=self.scena, use_basic_model=True, position=Vector2(0, 100), color=RED, size=Vector2(100, 100), how_collider="ROT_BOX", origin=Vector2(0.5, 0), use_repel=True
        )
        ModelBasic(parent=self.e, size=Vector2(10, 10))
        self.camera.target = Vector2(-50, 0)
    
    def Update(self, dt):
        self.e.rotation += 50 * dt
        if self.collider_2.IsCollider() : self.collider_2.color = GREEN
        else : self.collider_2.color = RED
        return super().Update(dt)

app = Game(800, 450, "Game")
app.Run()