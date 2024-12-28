
from pyray import *
from .in_data import *
from .engine import *

class Scena: 
    
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
            
        