from pyray import *
import math
from data import *



class Game(Engine):
    
    def __init__(self, window_size_x, window_size_y, name, use_y_index = False):
        super().__init__(window_size_x, window_size_y, name, use_y_index)
        set_target_fps(60)
        
        self.scena = Scena("prueba_collider")
        
        def is_presset_down() : 
            print("Presset_down")
        
        def is_presset() : 
            print("Presset")
        
        def is_presset_up() : 
            print("Presset_up")
        
        self.button = Button(parent=self.scena, position=Vector2(400, 225), use_basic_model=True, 
        when_pressing=[is_presset], when_down_pressing=[is_presset_down], when_up_pressing=[is_presset_up])
        
    def Update(self, dt):

        return super().Update(dt)

app = Game(800, 450, "Game")
app.Run()