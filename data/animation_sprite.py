from pyray import *
import math
from .in_data import *
from .entity import *

class AnimationSprite(Entity) : 
    def __init__(
        self, parent=None, name = "AnimationSprite", position=Vector2(0,0), 
        scale=Vector2(1,1), rotation = 0, origin=Vector2(0.5,0.5), color=WHITE, 
        texture="", 
        frame_per_second: int = 10,  # Valor predeterminado
        frame_start: int = 0,  # Valor inicial
        frame_end: int = 0,  # Valor final de los frames
        texture_cords : Vector2 = Vector2(0,0),
        texture_size : Vector2 = Vector2(0,0),
        direction_to_animate : Vector2 = Vector2(0,0),
        
        use_with_imagens : bool = False,
        imagens = [],
        
        ):
        super().__init__(parent, name, position, scale, rotation, origin)
        
        self.color = color
        self.type = "ANIMATION_SPRITE"
        self.texture_cords = texture_cords
        self.texture_size = texture_size
        self.direction_to_animate = direction_to_animate
        self.use_with_imagens = use_with_imagens
        self.frame_per_second = frame_per_second
        self.imagens = imagens
        self.frame_start = frame_start
        self.frame_end : int = frame_end if frame_end != 0 else len(imagens)
        self.frame_select : int = frame_start
        self.imganes_list = {}
        if imagens : 
            for i, img in enumerate(imagens) : 
                self.imganes_list[i] = load_texture(img)
        self.textura_rectagle : Rectangle = Rectangle(0, 0, texture_size.x, texture_size.y)
        self.timer_animation : float = 0
        self.texture = load_texture(texture) if texture != "" else None
        
    def Update(self, dt):
        
        self.timer_animation += dt
        if self.timer_animation >= 1.0 / self.frame_per_second:
            self.frame_select += 1
            self.timer_animation = 0
            
        if self.frame_select >= self.frame_end: 
            self.frame_select = self.frame_start
  
        if self.use_with_imagens == False :
            self.textura_rectagle.x = (self.frame_select * self.texture_size.x) * self.direction_to_animate.x
            self.textura_rectagle.y = (self.frame_select * self.texture_size.y) * self.direction_to_animate.y
            
        return super().Update(dt)

    def Draw(self):
        
        if self.use_with_imagens == False :
            if self.texture :
                draw_texture_pro(
                    self.texture,
                    self.textura_rectagle,
                    Rectangle(self.world_position.x, self.world_position.y, self.scale.x * 100, self.scale.y * 100),
                    self.origin, 
                    self.rotation,
                    self.color
                )
        else:
            if self.imganes_list : 
                # Asegúrate de que frame_select esté dentro de los límites
                frame_image = self.imganes_list[self.frame_select % len(self.imganes_list)]
                
                # Dibuja la imagen con las coordenadas y el tamaño correcto
                draw_texture_pro(
                    frame_image,
                    Rectangle(self.texture_cords.x * self.texture_size.x, self.texture_cords.y * self.texture_size.y, frame_image.width, frame_image.height),
                    Rectangle(self.world_position.x, self.world_position.y, self.scale.x * 100, self.scale.y * 100),
                    self.origin,
                    self.rotation,
                    self.color
                )
        