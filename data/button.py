from pyray import *
import math
from .in_data import *
from .entity import *


class Button(Entity) : 
    
    def __init__(
        self, 
        parent, 
        name = "Entity", 
        position=Vector2(0, 0), 
        scale=Vector2(1, 1), 
        size=Vector2(100, 100),
        rotation = 0, 
        origin=Vector2(0.5, 0.5), 
        vector_distance_to_sort = Vector2(0, 0), 
        min_activation_distance = 0,
        when_pressing : list = [],
        when_down_pressing : list = [],
        when_up_pressing : list = [],
        use_basic_model : bool = False,
        
        color = BLACK,
        
        ):
        super().__init__(parent, name, position, scale, rotation, origin, vector_distance_to_sort, min_activation_distance)
        
        self.size = size
        
        self.when_pressing : list = when_pressing
        self.when_down_pressing: list = when_down_pressing
        self.when_up_pressing : list = when_up_pressing
        self.use_basic_model = use_basic_model
        self.color = color
        self._save_color = color
        self.pressing : bool = False
        
    def Collider(self) -> Rectangle: 
        origen = vector2_multiply(self.origin, self.size)
        position = Vector2(
            self.world_position.x - origen.x, self.world_position.y - origen.y
        )
        scale = vector2_multiply(self.scale, self.size)
        return Rectangle(
            position.x, position.y, scale.x, scale.y
        )
        
    
    def IsMouseEnter(self) -> bool: 
        
        collider : Rectangle = self.Collider()
        mouse_position = get_mouse_position()
        
        min_x = collider.x
        max_x = collider.x + collider.width
        min_y = collider.y
        max_y = collider.y + collider.height

    
        if mouse_position.y > min_y and mouse_position.y < max_y and mouse_position.x > min_x and mouse_position.x < max_x : 
            return True
        
        return False
    
    def Update(self, dt):
        
        
        if self.IsMouseEnter() :
            
            self.color = Color(
                int(self._save_color[0] + 63), 
                int(self._save_color[1] + 63),
                int(self._save_color[2] + 63),
                self._save_color[3]
            )

            if is_mouse_button_down(0) and self.pressing == False : 
                for f in self.when_down_pressing : 
                    f()
                self.pressing = True
                
                
            if is_mouse_button_up(0) and self.pressing == True : 
                for f in self.when_up_pressing :
                    f()
                self.pressing = False
                
            if is_mouse_button_pressed(0) : 
                for f in self.when_pressing : 
                    f()
                
        else:
            self.color = self._save_color
        return super().Update(dt)

    
    def Interface(self):
        if self.use_basic_model : 
            draw_rectangle_pro(
                self.Collider(), Vector2(0, 0), 0, self.color
            )
        return super().Interface()