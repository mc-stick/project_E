from pyray import *
import math
from data import *



class Game(Engine):
    def __init__(self, window_size_x, window_size_y, name, use_y_index = False):
        super().__init__(window_size_x, window_size_y, name, use_y_index)
        set_target_fps(60)
        
        self.scena = Scena("Cartas")
        self.scena.use_y_index = False
        
        
        self.player = ModelBasic(parent=self.scena, position=Vector2(400, 400))
        self.Collider = Collider(parent=self.player, use_repel=True, use_basic_model=False, origin=Vector2(0, 0), repel_power=Vector2(200, 200), how_collider="CIRCLE")
        Collider(parent=self.scena, position=Vector2(400, 600), use_basic_model=True, size=Vector2(600, 50), color=RED, origin=Vector2(0.5, 0.5))
        
        
    def Update(self, dt):
        
        if self.player : 
            dir = Vector2(
                int(is_key_down(KEY_D)) - int(is_key_down(KEY_A)), 
                int(is_key_down(KEY_S)) - int(is_key_down(KEY_W)), 
            )
            
            dir = vector2_normalize(dir)
            
            self.player.position.x += dir.x * 200 * dt
            self.player.position.y += 1 * 200 * dt
        
            if is_key_pressed(KEY_X) : 
                self.player.Delect()
                self.player = None
                
                
                

            if is_key_pressed(KEY_SPACE) : self.player.position.y -= 500 * dt

        return super().Update(dt)
    
    def Draw(self):

    
        return super().Draw()
    
    def Interface(self):
        draw_text(str(get_fps()), 0, 0, 20, GREEN)
        return super().Interface()
    
    
app = Game(window_size_x=800, window_size_y=800, name="Hola Mundo", use_y_index=True)
app.Run()
