from pyray import *
import math
from data import *



class Game(Engine):
    def __init__(self, window_size_x, window_size_y, name, use_y_index = False):
        super().__init__(window_size_x, window_size_y, name, use_y_index)
        set_target_fps(60)
        
        self.scena = Scena("Cartas")
        self.scena.use_y_index = False
        

        self.model = ModelBasic(parent=self.scena)
        self.camera.zoom = 0.5
        self.grip = TileMap(parent=self.scena, texture="grass.png", tile_size=Vector2(8, 8), min_activation_distance=500, use_basic_model_to_collider=False)
        self.grip.scale = Vector2(4, 4)
        for x in range(-40, 40) : 
            for y in range(-40, 40) :  
                self.grip.AddTile(Vector2(x, y), Vector2(0, 0))
        print(Colliders)
        for x in range(-40, 40) : 
            for y in range(-40, 40) :  
                self.grip.RemoveTile(Vector2(x, y))
        print(Colliders)
    def Update(self, dt):


        dir = Vector2(
            int(is_key_down(KEY_D)) - int(is_key_down(KEY_A)),
            int(is_key_down(KEY_S)) - int(is_key_down(KEY_W))
        )
        dir = vector2_normalize(dir)
        
        self.camera.target.x += dir.x * 400 * dt
        self.camera.target.y += dir.y * 400 * dt
        
        
        self.model.position = self.Get_Global_Mouse_Position(self.camera)
        self.grip.vector_distance_to_sort = self.model.position
        print(self.model.position.x, self.model.position.y)
        
        return super().Update(dt)
    
    def Draw(self):


        return super().Draw()
    
    def Interface(self):
        draw_text(str(get_fps()), 0, 0, 20, GREEN)
        return super().Interface()
    
    
app = Game(window_size_x=960, window_size_y=540, name="Hola Mundo", use_y_index=True)
app.Run()
