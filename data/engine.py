from pyray import *
import math
from .in_data import *
from .entity import *

class Engine:
    def __init__(self, window_size_x : int, window_size_y : int, name : str, use_y_index : bool = False):
        
        init_window(window_size_x, window_size_y, name)
        
        self.camera = Camera2D()
        self.camera.target = Vector2(window_size_x / 2, window_size_y / 2)
        self.camera.offset = Vector2(window_size_x / 2, window_size_y / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0
        
        self.window_size = Vector2(window_size_x, window_size_y)
        
        self.use_y_index = use_y_index

    def RemoveEntity(self, Entity: Entity):
        # Intentar eliminar de la lista, si no está, ignorar
        if Entity in Entitys:
            Entitys.remove(Entity)
        else:
            print(f"Entity {Entity} not found in Entitys list.")
        
        # Intentar eliminar del diccionario, si no está, ignorar
        if Entity.name in Type_Entitys:
            Type_Entitys.pop(Entity.name)
        else:
            print(f"Entity name {Entity.name} not found in Type_Entitys.")

    def Update(self, dt):
        for e in Entitys : e.Update(dt)
        if self.use_y_index : Entitys.sort(key=lambda e: e.y_index)
        else : Entitys.sort(key=lambda e: e.index)
        
    def Draw(self):
        for e in Entitys : 
            if e.visible == True :
                e.Draw()
        
    def Interface(self):
        pass
        
    def Rum(self):
        while not window_should_close():
            dt = get_frame_time()
            self.Update(dt)
            begin_drawing()
            clear_background(GRAY)
            begin_mode_2d(self.camera)
            self.Draw()
            end_mode_2d()
            self.Interface()
            end_drawing()

        close_window()
