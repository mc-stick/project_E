from pyray import *
import math
from .in_data import *


class Engine:
    
    """
    Engine es una clase encargada de gestionar el ciclo principal de un juego o aplicación 2D, usando la librería Pyray. Proporciona funcionalidades básicas como la administración de escenas (`Scenas`), el manejo de la cámara y la captura de la posición global del mouse.

    Atributos:
    - `camera`: Camera2D, la cámara que se utiliza para renderizar el contenido en la pantalla.
    - `window_size`: Vector2, tamaño de la ventana del juego.

    Métodos:
    - `__init__(window_size_x, window_size_y, name, use_y_index=False)`: Inicializa la ventana del juego, configura la cámara y define el tamaño de la ventana.
    - `LookAt(point, target_position)`: Calcula el ángulo entre el punto dado y la posición del objetivo.
    - `Get_Global_Mouse_Position(camera) -> Vector2`: Devuelve la posición global del mouse en el mundo, transformando las coordenadas desde la cámara.
    - `Remove_Scenas(scena)`: Elimina una escena del diccionario `Scenas` si existe.
    - `Update(dt)`: Actualiza todas las escenas activas ordenadas por su índice. Se invoca en cada ciclo de actualización.
    - `Draw()`: Dibuja todas las escenas activas en el orden definido.
    - `Interface()`: Un método vacío preparado para ser sobrescrito con la lógica de interfaz de usuario.
    - `Run()`: Contiene el ciclo principal del juego. Controla la lógica de actualización, renderizado y entrada de usuario hasta que la ventana se cierra.
    """

    
    
    def __init__(self, window_size_x : int, window_size_y : int, name : str, use_y_index : bool = False):
        
        init_window(window_size_x, window_size_y, name)
        
        self.camera = Camera2D()
        self.camera.target = Vector2(window_size_x / 2, window_size_y / 2)
        self.camera.offset = Vector2(window_size_x / 2, window_size_y / 2)
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0
        
        self.window_size = Vector2(window_size_x, window_size_y)

        
    def LookAt(self, point, target_position):
        # Calcular el ángulo entre la posición actual del objeto y la posición del objetivo
        direction = Vector2(target_position.x - point.x, target_position.y - point.y)
        return math.atan2(direction.y, direction.x)
    
    def Get_Global_Mouse_Position(self, camera) -> Vector2:
        return get_screen_to_world_2d(get_mouse_position(), camera)
    
    # Borrar las Scenas
    def Remove_Scenas(self, scena):
        if not scena.name in Scenas : return
        Scenas.pop(scena.name)
            
    
    def Update(self, dt):
        global Scenas
        Scenas = dict(sorted(Scenas.items(), key=lambda item: item[1].index))
        for s in Scenas.values() : s.Update(dt)
        
        
    def Draw(self):
        for s in Scenas.values() : 
            if s.visible == True :
                s.Draw()
        
    def Interface(self):
        pass
        
    def Run(self):
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


        