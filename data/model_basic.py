from pyray import *
import math
from .in_data import *
from .entity import *


class ModelBasic(Entity):
    
    """
    ModelBasic es una clase que representa una entidad visual básica, como un rectángulo, círculo o cápsula, en un entorno 2D. Hereda de la clase `Entity` y añade funcionalidad específica para el dibujo de modelos básicos.

    Atributos:
    - `parent`: Scena, el objeto padre de la entidad.
    - `name`: str, el nombre de la entidad. Se inicializa como "Entity" por defecto.
    - `position`: Vector2, la posición local de la entidad.
    - `scale`: Vector2, la escala local de la entidad.
    - `rotation`: float, la rotación local de la entidad.
    - `origin`: Vector2, el origen para la rotación y escala de la entidad. Por defecto es (0.5, 0.5), centrado.
    - `color`: Color, el color del modelo que se va a dibujar. Inicializa en blanco (`WHITE`).
    - `how_model`: str, el tipo de modelo a dibujar. Puede ser "RECTANGLE", "CIRCLE", o "CAPSULE".
    - `dimension`: float, usado para determinar el tamaño extra de ciertas formas como la cápsula.
    - `direction`: str, la dirección de la cápsula (para futuros usos o mejoras), inicializa como "VERTICAL".
    
    Métodos:
    - `__init__(...)`: Inicializa una entidad visual básica con las propiedades proporcionadas, llamando también al constructor de `Entity`.
    - `Draw()`: Dibuja el modelo especificado por `how_model`:
    - Si es "RECTANGLE", dibuja un rectángulo usando las propiedades de escala, rotación y color.
    - Si es "CIRCLE", dibuja un círculo basado en la posición y escala de la entidad.
    - Si es "CAPSULE", dibuja una cápsula utilizando la posición, escala y la propiedad `dimension`.
    Luego, llama al método `Draw()` de la clase padre para dibujar cualquier entidad hija.
    """
        
    def __init__(
        self, parent, 
        name = "Entity", 
        position=Vector2(), 
        scale=Vector2(1, 1), 
        size = Vector2(100,100),
        rotation = 0, 
        origin=Vector2(0.5, 0.5), 
        color : Color = WHITE,
        how_model : str = "RECTANGLE",
        dimension: float = 0, 
        direction: str = "VERTICAL",
        ):
        super().__init__(parent, name, position, scale, rotation, origin)

        self.color = color
        self.how_model = how_model
        self.dimension = dimension
        self.direction = direction
        self.size = size
        
    def Draw(self):
        
        if self.how_model == "RECTANGLE" : 
            draw_rectangle_pro(
                Rectangle(
                    self.world_position.x, self.world_position.y, self.world_scale.x * self.size.x, self.world_scale.y * self.size.y
                ), Vector2(self.origin.x * self.size.y, self.origin.y * self.size.y), self.world_rotation, self.color
            )
        elif self.how_model == "CIRCLE" : 
            draw_circle_v(
                self.world_position, (self.world_scale.x + self.world_scale.y)/2, self.color
            )
        elif self.how_model == "CAPSULE" : 
            draw_capsule_2d(
                Capsule(self.world_position, (self.world_scale.x+self.world_scale.y)/2, dimension=self.dimension), self.color
            )
        
        return super().Draw()
    