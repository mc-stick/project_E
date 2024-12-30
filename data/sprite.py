from pyray import *
import math
from .in_data import *
from .entity import *

class Sprite(Entity) : 
    
    """Sprite es una clase que representa un objeto gráfico basado en texturas, heredando de la clase `Entity`. Puede utilizar una textura cargada para ser dibujada en pantalla con propiedades como tamaño, posición, rotación y color.

    Atributos:
    - `parent`: Referencia al objeto padre de la entidad.
    - `name`: str, el nombre de la entidad. Por defecto es "Sprite".
    - `position`: Vector2, la posición del sprite en la pantalla.
    - `scale`: Vector2, la escala del sprite que afecta su tamaño en pantalla.
    - `size`: Vector2, define el tamaño base del sprite en unidades de píxeles.
    - `rotation`: float, el ángulo de rotación del sprite en grados.
    - `origin`: Vector2, el punto de origen del sprite para las transformaciones (normalmente centrado en (0.5, 0.5)).
    - `color`: Color, el color aplicado al sprite (permite modificar el color o aplicar transparencias).
    - `texture`: str, la ruta de la textura que se utiliza para el sprite. Si está vacía, no se carga ninguna textura.
    - `use_cords_and_size`: bool, determina si se usarán coordenadas específicas y un tamaño de textura para dibujar solo una parte de la textura.
    - `texture_cords`: Vector2, coordenadas dentro de la textura que indican la posición desde la que se dibuja el sprite, si `use_cords_and_size` es `True`.
    - `texture_size`: Vector2, tamaño de la porción de la textura que se dibuja si `use_cords_and_size` es `True`.
    
    Métodos:
    - `__init__(...)`: Inicializa el objeto `Sprite` con la configuración básica, como su posición, tamaño, textura y otros atributos visuales. Si se proporciona una textura, se carga en la variable `self.texture`.
    - `Draw()`: Dibuja el sprite en pantalla. Si se ha cargado una textura, se utiliza `draw_texture_pro` para dibujarla con transformaciones (escala, rotación, origen). Si `use_cords_and_size` es `True`, solo dibuja la parte definida por `texture_cords` y `texture_size` de la textura; si no, se dibuja la textura completa.
    """
  
  
    def __init__(
        self, parent=None, 
        name = "Sprite", 
        position=Vector2(0,0), 
        scale=Vector2(1,1), 
        size = Vector2(100, 100), 
        rotation = 0, 
        origin=Vector2(0.5,0.5), 
        color=WHITE, 
        texture="", 
        use_cords_and_size : bool = True,
        texture_cords : Vector2 = Vector2(0,0),
        texture_size : Vector2 = Vector2(0,0),
        
        ):
        super().__init__(parent, name, position, scale, rotation, origin)
        
        self.size = size
        self.color = color
        self.type = "SPRITE"
        self.texture_cords = texture_cords
        self.texture_size = texture_size
        self.texture = load_texture(texture) if texture != "" else None
        self.use_cords_and_size = use_cords_and_size
        
    def Draw(self):
 
        if self.texture :
            # Dibuja la imagen con las coordenadas y el tamaño correcto
            if self.use_cords_and_size == True :
                rect = Rectangle(self.texture_cords.x * self.texture_size.x, self.texture_cords.y * self.texture_size.y, self.texture_size.x, self.texture_size.y)
            else:
                rect = Rectangle(0, 0, self.texture.width, self.texture.height)
            
            draw_texture_pro(
                self.texture,
                rect,
                Rectangle(self.world_position.x, self.world_position.y, self.scale.x * self.size.x, self.scale.y * self.size.y),
                vector2_multiply(self.origin, self.size),
                self.world_rotation,
                self.color
            )