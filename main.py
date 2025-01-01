from pyray import *
import math
from data import *



class Game(Engine):
    def __init__(self, window_size_x, window_size_y, name, use_y_index = False):
        super().__init__(window_size_x, window_size_y, name, use_y_index)
        set_target_fps(60)
        
        self.scena = Scena("Cartas")
        self.scena.use_y_index = False
        
        self.body = Body(parent=self.scena, friction=0.2, position=Vector2(0, 0))
        self.model = Collider(parent=self.body, use_basic_model=True, color=WHITE, use_repel=True, layer={1}, origin=Vector2(0, 0))
        self.model.collision_range_to_use = 10
        self.rays = [
            Raycast(parent=self.model, end_position=Vector2(0, 101), start_positoin=Vector2(0, 50), use_basic_model=True, layer={5}, origin=Vector2(0, 0)),
            Raycast(parent=self.model, end_position=Vector2(50, 101), start_positoin=Vector2(50, 50), use_basic_model=True, layer={5}, origin=Vector2(0, 0)),
            Raycast(parent=self.model, end_position=Vector2(100, 101), start_positoin=Vector2(100, 50), use_basic_model=True, layer={5}, origin=Vector2(0, 0))
            ]
        self.camera.zoom = 0.3
        self.grip = TileMap(parent=self.scena, texture="grass.png", tile_size=Vector2(8, 8), min_activation_distance=2000, use_basic_model_to_collider=True, use_collider=True, layer_collider={1, 5})
        self.grip.min_activation_distance_to_collider = 500
        self.grip.scale = Vector2(10, 10)
        for x in range(-50, 50) : 
            for y in range(10, 30) :  
                self.grip.AddTile(Vector2(x, y), Vector2(0, 0))
        
        #Collider(parent=self.scena, position=Vector2(400, 400), use_basic_model=True)
    def Update(self, dt):

        dir = Vector2(
            int(is_key_down(KEY_D)) - int(is_key_down(KEY_A)),
            int(is_key_down(KEY_S)) - int(is_key_down(KEY_W))
        )
        dir = vector2_normalize(dir)
        ray = False
        for r in self.rays : ray = r.IsCollider()
        self.body.ReloadVelocity()
        self.body.velocity.x += dir.x * 200
        
        if ray == False : self.body.velocity.y += 650
        if ray == True and is_key_pressed(KEY_SPACE):
            self.body.velocity.y -= 1000 * 10
        self.camera.target = vector2_lerp(self.camera.target, self.body.world_position, 0.2)
        
        self.body.MoveVelocity(dt)

        
        self.grip.vector_distance_to_sort = self.body.world_position
        
        return super().Update(dt)
    
    def Draw(self):


        return super().Draw()
    
    def Interface(self):
        draw_text(str(get_fps()), 0, 0, 20, GREEN)
        return super().Interface()
    
    
app = Game(window_size_x=960, window_size_y=540, name="Hola Mundo", use_y_index=True)
app.Run()
