from pyray import *
import math
from .in_data import *
from .entity import *

class AnimationSprite(Entity) : 
    
    """
        AnimationSprite es una clase que maneja la animación de sprites, ya sea a partir de una textura o de una lista de imágenes. Hereda de la clase `Entity`.

        Atributos:
        - `parent`: Referencia al objeto padre de la entidad.
        - `name`: str, el nombre de la entidad. Por defecto es "AnimationSprite".
        - `position`: Vector2, la posición del sprite en la pantalla.
        - `scale`: Vector2, la escala del sprite.
        - `rotation`: float, el ángulo de rotación del sprite en grados.
        - `origin`: Vector2, el punto de origen del sprite para las transformaciones.
        - `color`: Color, el color aplicado al sprite.
        - `texture`: str, la ruta de la textura utilizada para la animación.
        - `frame_per_second`: int, cantidad de frames que se muestran por segundo.
        - `frame_start`: int, el índice del frame inicial en la animación.
        - `frame_end`: int, el índice del frame final en la animación.
        - `texture_cords`: Vector2, coordenadas de la textura.
        - `texture_size`: Vector2, tamaño de los cuadros de la textura.
        - `direction_to_animate`: Vector2, dirección en la que avanza la animación en los ejes X e Y.
        - `use_with_imagens`: bool, determina si se utilizan una lista de imágenes en lugar de una textura única para la animación.
        - `imagens`: list, lista de rutas de imágenes para la animación si `use_with_imagens` es True.
        - `frame_select`: int, el índice actual del frame en la animación.
        - `imganes_list`: dict, un diccionario que almacena las texturas cargadas a partir de la lista de imágenes.
        - `textura_rectagle`: Rectangle, un rectángulo que define qué parte de la textura se dibuja.
        - `timer_animation`: float, un temporizador que controla el avance de la animación.

        Métodos:
        - `__init__(...)`: Inicializa el objeto `AnimationSprite`, cargando la textura o las imágenes según sea necesario y configurando los parámetros de la animación.
        - `Update(dt)`: Actualiza el frame actual de la animación basado en el tiempo transcurrido `dt` y ajusta la textura o la imagen mostrada.
        - `Draw()`: Dibuja la animación del sprite en pantalla. Si se utiliza una textura, dibuja la porción correspondiente; si se utiliza una lista de imágenes, dibuja la imagen correcta.
    """

    def __init__(
        self, parent=None, 
        name = "AnimationSprite", 
        position=Vector2(0,0), 
        scale=Vector2(1,1), 
        size = Vector2(100, 100), 
        rotation = 0, 
        origin=Vector2(0.5,0.5), 
        color=WHITE, 
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
        
        self.size = size
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
                    Rectangle(self.world_position.x, self.world_position.y, self.scale.x * self.size.x, self.scale.y * self.size.y),
                    vector2_multiply(self.origin, self.size),
                    self.world_rotation,
                    self.color
                )
        