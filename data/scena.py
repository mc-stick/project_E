
from pyray import *
from .in_data import *
from .engine import *

class Scena: 
    
    """
    Scena es una clase que representa una escena dentro del entorno del juego. Gestiona las entidades que forman parte de la escena y se encarga de actualizar y dibujar dichas entidades.

    Atributos:
    - `name`: str, el nombre de la escena. Si el nombre ya existe en `Scenas`, se le agrega un sufijo numérico único.
    - `type`: str, el tipo de entidad, en este caso siempre es "SCENA".
    - `entitys`: list, una lista de entidades (`Entity`) que pertenecen a esta escena.
    - `type_entitys`: dict, un diccionario que almacena las entidades con sus nombres como claves.
    - `use_y_index`: bool, determina si las entidades deben ser ordenadas por su índice `y_index` (posición vertical) al dibujar. Por defecto, es `False`.
    - `index`: int, índice que define el orden de la escena. Si es 0, utiliza la longitud actual de `Scenas` para establecer su valor.
    - `visible`: bool, determina si la escena es visible. Por defecto es `True`.

    Métodos:
    - `__init__(...)`: Inicializa la escena con un nombre, y opcionalmente permite definir si debe usar `y_index` para ordenar sus entidades, su índice y su visibilidad.
    - `Remove_Entity(entity)`: Remueve una entidad dada de la lista de entidades y de los diccionarios de `Entitys` y `Type_Entitys` si existe. Ignora si no la encuentra.
    - `Update(dt)`: Actualiza todas las entidades de la escena. Si `use_y_index` es `True`, ordena las entidades por `y_index`, de lo contrario las ordena por `index`.
    - `Draw()`: Dibuja todas las entidades de la escena que sean visibles (`visible` == True).
    """

    
    
    def __init__(self, name, use_y_index = False, index = 0, visible = True):
        self.name = name if name in Scenas else name + f".{len(Scenas):003}"
        self.type = "SCENA"
        self.entitys = []
        self.type_entitys = {}
        self.use_y_index : bool = use_y_index
        self.index : int = index if index == 0 else len(Scenas)
        self.visible : bool = visible
        Scenas[self.name] = self
    
    
    # Para Remover la Entidades
    def Remove_Entity(self, entity):
        # Intentar eliminar de la lista, si no está, ignorar
        if entity in self.entitys:
            self.entitys.remove(entity)    
        if entity in Entitys : 
            Entitys.remove(entity)
            
        # Intentar eliminar del diccionario, si no está, ignorar
        if Type_Entitys.get(entity.name):
            Type_Entitys.pop(entity.name)
        if self.type_entitys.get(entity.name):
            self.type_entitys.pop(entity.name)
        
    def Update(self, dt):
        
        for e in self.entitys : e.Update(dt)
        if self.use_y_index : self.entitys.sort(key=lambda e: e.y_index)
        else : self.entitys.sort(key=lambda e: e.index)
        
        
        
    def Draw(self):
        for e in self.entitys : 
            if e.visible == True :
                e.Draw()
            
        