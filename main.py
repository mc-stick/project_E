from pyray import *
import math
from data import *



class Game(Engine):
    def __init__(self, window_size_x, window_size_y, name, use_y_index = False):
        super().__init__(window_size_x, window_size_y, name, use_y_index)
        set_target_fps(60)
        
        self.scena = Scena("Cartas")
        self.scena.use_y_index = False
        
        self.tilemap = TileMap(parent=self.scena, position=Vector2(0, 0),  texture="grass.png", tile_size=Vector2(8, 8))
        self.tilemap.scale = Vector2(4, 4)
        for x in range(-5, 5):
            self.tilemap.AddTile(Vector2(x, 0), Vector2(0, 0))
        
        self.model = ModelBasic(parent=self.scena, scale=Vector2(4, 4), size=Vector2(8, 8), color=Color(255, 255, 225, 50))
        
    def Update(self, dt):
        

        target = get_mouse_position()
        step = 8 * 4
        x = int(target.x / step) * step
        y = int(target.y / step) * step
        self.model.position = Vector2(x, y)
        target = Vector2(int(x / step), int(y / step))
        
        if is_mouse_button_down(0) : 
            self.tilemap.AddTile(target, Vector2(0, 0))
        if is_mouse_button_down(1) :
            self.tilemap.RemoveTile(target)
    
        return super().Update(dt)
    
    def Draw(self):

    
        return super().Draw()
    
    def Interface(self):
        draw_text(str(get_fps()), 0, 0, 20, GREEN)
        return super().Interface()
    
    
app = Game(window_size_x=800, window_size_y=800, name="Hola Mundo", use_y_index=True)
app.Run()