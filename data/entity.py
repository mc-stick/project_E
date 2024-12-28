from pyray import *
import math
from .in_data import *
from .scena import *

class Entity(Scena):
    
    """
        Entity representa una entidad en un entorno 2D, que puede tener un padre y otros atributos como posición, escala y rotación.

        Atributos:
        - `parent`: Scena, el objeto padre de la entidad que define su jerarquía.
        - `name`: str, el nombre de la entidad. Si ya existe en el padre, se le añade un identificador único.
        - `position`: Vector2, la posición local de la entidad respecto a su padre. Inicializa en (0, 0).
        - `scale`: Vector2, la escala local de la entidad. Inicializa en (1, 1).
        - `rotation`: float, la rotación local de la entidad en grados.
        - `origin`: Vector2, el origen de la entidad para rotación y escala. Inicializa en (0.5, 0.5).
        - `world_position`: Vector2, la posición mundial calculada de la entidad.
        - `world_scale`: Vector2, la escala mundial acumulada de la entidad.
        - `world_rotation`: float, la rotación mundial acumulada de la entidad.
        - `index`: int, índice usado para ordenar la entidad en la jerarquía.
        - `y_index`: float, posición en el eje Y usada para ordenar la entidad para el renderizado.
        - `use_y_index`: bool, indica si ordenar las entidades por el eje Y.
        - `visible`: bool, determina si la entidad es visible o no.
        - `entitys`: lista, contiene todas las entidades hijas de esta entidad.
        - `type_entitys`: dict, contiene todas las entidades del padre con su nombre como clave.

        Métodos:
        - `__init__(...)`: Inicializa una nueva entidad con los valores proporcionados. Añade la entidad al padre y a las listas/diccionarios globales.
        - `Delect()`: Elimina la entidad de su padre y de las listas/diccionarios globales, eliminando también sus entidades hijas de forma recursiva.
        - `Update(dt)`: Actualiza la posición, escala y rotación mundial de la entidad en función de su padre. Si tiene entidades hijas, también las actualiza y las ordena.
        - `Draw()`: Dibuja la entidad y todas sus entidades hijas, si son visibles.
    """

    
    
    def __init__(
        self, 
        parent,
        name: str = "Entity",
        position=Vector2(0, 0),
        scale=Vector2(1, 1),  
        rotation: float = 0,
        origin=Vector2(0.5, 0.5),        
    ):
        self.parent = parent
        self.name = name if name in self.parent.type_entitys else name + f".{len(self.parent.entitys)+1:003}"
        self.type = "ENTITY"
        
        self.position = position
        self.scale = scale 
        self.rotation = rotation
        
        self.world_position = Vector2()
        self.world_scale = Vector2(1, 1)
        self.world_rotation = 0
        
        self.origin = origin
        
        

        self.index : int = 0
        self.y_index : float = 0
        self.use_y_index : bool = True
        
        self.visible = True

        # Para Guadar el Yntitys en las variables Globales
        self.entitys = []
        self.type_entitys = {}
        
        self.parent.entitys.append(self)
        self.parent.type_entitys[self.name] = self
        Type_Entitys[self.name] = self
        Entitys.append(self)

    def Delect(self):
        if self.entitys :
            for e in self.entitys:
                e.Delect()
                
        if self in self.parent.entitys:
            self.parent.entitys.remove(self)    
            
        if self.parent.type_entitys.get(self.name):
            self.parent.type_entitys.pop(self.name)
            
        if self in Entitys : 
            Entitys.remove(self)
        
        if Type_Entitys.get(self.name):
            Type_Entitys.pop(self.name)
            
    def Update(self, dt):
        if self.parent and self.parent.type != "SCENA":
            # 1. Obtener las propiedades del padre (posición y rotación mundial)
            parent_position = self.parent.world_position
            parent_rotation = self.parent.world_rotation
            parent_scale = self.parent.world_scale

            # 2. Rotar la posición local del hijo alrededor del origen del padre según la rotación del padre
            rotated_position = vector2_rotate(self.position, math.radians(parent_rotation))  # Rotación correcta respecto al origen del padre

            # 3. Ajustar la posición mundial del hijo con respecto al padre
            self.world_position.x = parent_position.x + rotated_position.x * parent_scale.x
            self.world_position.y = parent_position.y + rotated_position.y * parent_scale.y
            
             # 4. Controlar la velocidad de la rotación (ajustar factor para desacelerar la rotación)
            self.world_rotation = parent_rotation+self.rotation

            # 5. Escala acumulada entre la escala del padre y la del hijo
            self.world_scale.x = parent_scale.x * self.scale.x
            self.world_scale.y = parent_scale.y * self.scale.y
        else:
            # Si no tiene padre, la posición mundial es la misma que la local
            self.world_position = self.position
            self.world_rotation = self.rotation
            self.world_scale = self.scale
        
        self.y_index = self.world_position.y

        if self.entitys :
            for e in self.entitys : e.Update(dt)
            if self.use_y_index : self.entitys.sort(key=lambda e: e.y_index)
            else : self.entitys.sort(key=lambda e: e.index)
        
    def Draw(self):
        
        """
        # Normalize the scale by multiplying by 100
        normalized_scale = Vector2(self.world_scale.x * 100, self.world_scale.y * 100)
        """
        if self.entitys :
            for e in self.entitys : 
                if e.visible == True :
                    e.Draw()
                
        

        