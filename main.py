from pyray import *
import math
from data import *


class Cartas(Entity) : 
    def __init__(self, parent, name = "Entity", position=Vector2(), scale=Vector2(1, 1), rotation = 0, origin=Vector2(0, 0)):
        super().__init__(parent, name, position, scale, rotation, origin)
        
        self.mouse = Collider(parent=self.parent, name="Mouse", scale=Vector2(0.1, 0.1),origin=Vector2(0, 0), color=RED, use_basis_model=True)
        
        self.use_y_index = False
        
        self.model = Entity(parent=self, position=Vector2(0,0), scale=Vector2(1.4, 2), origin=Vector2(1.4/2,1))
        self.model.use_y_index = False
        self.model_shadown = ModelBasic(parent=self.model, position=Vector2(5,5), scale=Vector2(1, 1), color=Color(0, 0, 0, 50), origin=Vector2(1.4/2,1))
        self.model_base = ModelBasic(parent=self.model, position=Vector2(0,0), scale=Vector2(1, 1), color=Color(150, 60, 100, 255), origin=Vector2(1.4/2,1))
        self.model_base_scale : Vector2
        self.model_move : Vector2
        
        self.is_select = False
        self.mouse_enter_position : Vector2 = Vector2()
        self.mouse_position :Vector2 = Vector2()
        self.origin = Vector2(0.5, 0)
        
        self.collider = Collider(
            parent=self, position=Vector2(0,0), name="Collider", 
            scale=Vector2(1.4, 2), use_basis_model=False, 
            how_collider="BOX", color=Color(0, 0, 255, 20), origin=Vector2(1.4/2,1)
        )
    def Update(self, dt):
        
        
        self.mouse.position = get_mouse_position()
                
        if self.collider.IsCollider() and is_mouse_button_pressed(0):
            self.is_select = not self.is_select
            self.mouse_enter_position = self.mouse.position
            self.mouse_position = vector2_subtract(self.mouse.position, self.position)
            self.model_base_scale = vector2_add(self.scale, Vector2(0.1, 0.1))
            self.model_move = Vector2(10, 10)
            
        if self.is_select and is_mouse_button_down(0): 
            
            
            self.model.rotation = lerp(self.model.rotation, ((get_mouse_delta().x + get_mouse_delta().y)/2)*2, .05)
            self.position.x = lerp(self.position.x, self.mouse.position.x - self.mouse_position.x, 0.2)
            self.position.y = lerp(self.position.y, self.mouse.position.y - self.mouse_position.y, 0.2)
            
        else : 
            self.model_base_scale = Vector2(1,1)
            self.model_move = Vector2(2, 2)
            self.model.rotation = lerp(self.model.rotation, 0, .1)
            self.is_select = False
        
        self.model_base.scale = vector2_lerp(self.model_base.scale, self.model_base_scale, 0.5)
        self.model_base.position = vector2_lerp(self.model_base.position,Vector2(self.model_move.x*-1, self.model_move.y*-1), 0.5)
        #self.model_shadown.scale = vector2_lerp(self.model_shadown.scale, self.model_base_scale, 0.5)
        self.model_shadown.position = vector2_lerp(self.model_shadown.position, self.model_move, 0.5)
        
        return super().Update(dt)

class Game(Engine):
    def __init__(self, window_size_x, window_size_y, name, use_y_index = False):
        super().__init__(window_size_x, window_size_y, name, use_y_index)
        set_target_fps(60)
        
        self.scena = Scena("Cartas")
        self.scena.use_y_index = True
        Cartas(parent=self.scena, position=Vector2(400, 400))
        
    def Update(self, dt):

        if is_key_pressed(KEY_A) : 
            Cartas(parent=self.scena, position=get_mouse_position())
        
        return super().Update(dt)
    
    def Draw(self):

    
        return super().Draw()
    
    def Interface(self):
        draw_text(str(get_fps()), 0, 0, 20, GREEN)
        return super().Interface()
    
    
app = Game(window_size_x=800, window_size_y=800, name="Hola Mundo", use_y_index=True)
app.Run()
