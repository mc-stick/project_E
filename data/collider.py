from pyray import *
import math
from .in_data import *
from .entity import *



class Collider(Entity) : 
    
    """
    Clase que representa un colisionador para entidades en 2D, como una cápsula, caja o círculo.

    Atributos:
    - `position`: Vector2, posición central del colisionador.
    - `scale`: Vector2, escala del colisionador, que afecta su tamaño.
    - `rotation`: Ángulo de rotación en grados.
    - `layer`: Int, capa en la que se encuentra el rayo, útil para filtrar colisiones.
    - `origin`: Punto de referencia para la posición del colisionador, generalmente el centro.
    - `use_basic_model`: Bool, indica si se usa el modelo base para el colisionador.
    - `how_collider`: Tipo de colisionador, puede ser "BOX", "CIRCLE"
    - `dimension`: Longitud del cuerpo de la cápsula, relevante solo para cápsulas.
    - `direction`: Dirección de la cápsula, "VERTICAL" o "HORIZONTAL".
    - `use_repel`: Bool, indica si se debe aplicar repulsión entre colisionadores.
    - `color`: Color del colisionador para su representación visual.

    Métodos:
    - `__init__()`: Inicializa los atributos del colisionador.
    - `__repel__()`: Aplica la repulsión entre el colisionador actual y otro cuando colisionan.
    - `Collider()`: Crea el modelo del colisionador (caja, círculo o cápsula).
    - `IsCollider()`: Verifica si hay alguna colisión con otros objetos.
    - `GetCollider()`: Obtiene el colisionador con el que está colisionando la entidad.
    - `Delect()`: Elimina el colisionador de la lista de colisionadores.
    - `Update()`: Actualiza el estado del colisionador, aplicando repulsión si es necesario.
    - `Draw()`: Dibuja el colisionador en la pantalla.
    """
    
    
    def __init__(
        self, 
        parent, 
        name = "Collider", 
        position=Vector2(), 
        scale=Vector2(1, 1), 
        size=Vector2(100, 100),
        rotation = 0, 
        origin=Vector2(0.2), 
        use_basic_model = False, 
        how_collider : str = "BOX",
        use_repel : bool = False,
        color : Color = BLUE,
        repel_power : Vector2 = Vector2(),
        layer : int = 0
        ):
        
        super().__init__(parent, name, position, scale, rotation, origin)

        self.type = "COLLIDER"
        self.use_basic_model = use_basic_model
        self.how_collider = how_collider
        self.use_repel = use_repel
        self.color = color
        self.repel_power : Vector2 = repel_power
        self.layer = layer
        self.size = size
        Colliders.append(self)

        
    def __repel__(self, other_obj, dt) -> None:
        """Repels this entity from the other entity based on their collider types."""
        other_obj: Collider = other_obj
        self_obj = self if self.parent.type == "SCENA" else self.parent
        
    
        # Obtener el tipo de colisionador
        self_collider_type = self.how_collider
        other_collider_type = other_obj.how_collider

        normal = Vector2(0, 0)

        if self_collider_type == "BOX" and other_collider_type == "BOX":
            # Obtener los colliders de tipo "BOX"
            self_collider: Rectangle = self.Collider()
            other_collider: Rectangle = other_obj.Collider()

            # Calcular la superposición en el eje X e Y
            overlap_x = min(self_collider.x + self_collider.width - other_collider.x, 
                            other_collider.x + other_collider.width - self_collider.x)
            overlap_y = min(self_collider.y + self_collider.height - other_collider.y,
                            other_collider.y + other_collider.height - self_collider.y)

            # Determinar la dirección de la repulsión
            if overlap_x < overlap_y:
                if self_collider.x + self_collider.width > other_collider.x + other_collider.width:
                    normal = Vector2(1, 0)  # Repulsión hacia la derecha
                else:
                    normal = Vector2(-1, 0)  # Repulsión hacia la izquierda
            else:
                if self_collider.y + self_collider.height > other_collider.y + other_collider.height:
                    normal = Vector2(0, 1)   # Repulsión hacia arriba
                else:
                    normal = Vector2(0, -1)  # Repulsión hacia abajo

        elif self_collider_type == "CIRCLE" and other_collider_type == "CIRCLE":
            # Obtener los colliders de tipo "CIRCLE"
            self_collider: Circle = self.Collider()
            other_collider: Circle = other_obj.Collider()

            # Calcular la repulsión entre círculos
            dist = vector2_length(vector2_subtract(self_collider.position, other_collider.position))
            if dist < self_collider.radius + other_collider.radius:
                # Calcular la dirección de la repulsión
                normal = vector2_normalize(vector2_subtract(self_collider.position, other_collider.position))

        elif self_collider_type == "CIRCLE" and other_collider_type == "BOX":
            # Obtener los colliders de tipo "CIRCLE" y "BOX"
            self_collider: Circle = self.Collider()
            other_collider: Rectangle = other_obj.Collider()

            # Obtener los puntos clave del rectángulo
            corners = other_obj.Get_Corners()
            closest_point = get_closest_point_to_rectangle(self_collider.position, other_collider)

            # Calcular la dirección de la repulsión
            normal = vector2_normalize(vector2_subtract(self_collider.position, closest_point))

        elif self_collider_type == "BOX" and other_collider_type == "CIRCLE":
            # Interacción inversa: RECTÁNGULO con CÍRCULO
            self_collider: Rectangle = self.Collider()
            other_collider: Circle = other_obj.Collider()

            # Obtener los puntos clave del rectángulo
            corners = self.Get_Corners()
            closest_point = get_closest_point_to_rectangle(other_collider.position, self_collider)

            # Calcular la dirección de la repulsión
            normal = vector2_normalize(vector2_subtract(other_collider.position, closest_point))

        # Aplicar la repulsión (ajustar magnitudes según sea necesario)
        
        
        self_obj.position.x += normal.x * self.repel_power.x * dt
        self_obj.position.y += normal.y * self.repel_power.y * dt

    
    def Get_Corners(self) -> list:
        """Obtiene las posiciones clave de acuerdo con el tipo de colisionador."""
        if self.how_collider == "BOX":
            rect: Rectangle = self.Collider()
            return [
                Vector2(rect.x, rect.y),  # Esquina superior izquierda
                Vector2(rect.x + rect.width, rect.y),  # Esquina superior derecha
                Vector2(rect.x, rect.y + rect.height),  # Esquina inferior izquierda
                Vector2(rect.x + rect.width, rect.y + rect.height)  # Esquina inferior derecha
            ]

        elif self.how_collider == "CIRCLE":
            circle: Circle = self.Collider()
            return [
                Vector2(circle.position.x, circle.position.y - circle.radius),
                Vector2(circle.position.x, circle.position.y + circle.radius),
                Vector2(circle.position.x - circle.radius, circle.position.y),
                Vector2(circle.position.x + circle.radius, circle.position.y),
            ]

        return [
            Vector2(), Vector2(), Vector2(), Vector2()
            ]

    # Crea el Collider Basico de las Entidades
    def Collider(self) -> object: 
        
        scale_x = self.world_scale.x * self.size.x
        scale_y = self.world_scale.y * self.size.y
        
        world_post = self.world_position
        origin = self.origin
        
        position_x = world_post.x - (origin.x * self.size.x)
        position_y = world_post.y - (origin.y * self.size.y)
        radius = (self.world_scale.x * self.size.y + self.world_scale.y * self.size.y) / 4
        
        if self.how_collider == "BOX" : 
            return Rectangle(
                position_x, position_y, scale_x, scale_y
            )
        elif self.how_collider == "CIRCLE" : 
            return Circle(
                position=Vector2(position_x, position_y), radius=radius
            )
        
       
    """
    # Detectar el collider con las otras Entitys
    """
    def IsCollider(self) -> bool : 
        if self.GetCollider() : return True
        return False
    
    def GetCollider(self,) -> object:
        for entity in Colliders:
            entity :  Rectangle | Circle | Capsule
            if entity.layer != self.layer : continue
            if self == entity : continue
            
            # Detectar todas las combinaciones de colisionadores
            # Colisiones de BOX con otros tipos
            if self.how_collider == "BOX":
                if entity.how_collider == "BOX":
                    if check_collision_recs(self.Collider(), entity.Collider()):
                        return entity
                
                elif entity.how_collider == "CIRCLE":
                    if check_collision_circle_rectangle(entity.Collider(), self.Collider()):
                        return entity

            # Colisiones de CIRCLE con otros tipos
            elif self.how_collider == "CIRCLE":
                if entity.how_collider == "CIRCLE":
                    if check_collision_circles(self.Collider().position, self.Collider().radius, entity.Collider().position, entity.Collider().radius):
                        return entity
                
                elif entity.how_collider == "BOX":
                    if check_collision_circle_rectangle(self.Collider(), entity.Collider()):
                        return entity

        return None

    
    def Delect(self):
        super().Delect()
        if self in Colliders : 
            Colliders.remove(self)
    
    def Update(self, dt):
        
        if self.use_repel :
            e = self.GetCollider()
            if e : 
                self.__repel__(e, dt) 
        return super().Update(dt)
    
    def Draw(self):
        
        if self.use_basic_model == True :
            collider : Rectangle | Circle | Capsule = self.Collider()
            if self.how_collider == "BOX" :
                draw_rectangle_v(
                    Vector2(collider.x, collider.y), Vector2(collider.width, collider.height), self.color
                    ) 
            elif self.how_collider == "CIRCLE" : 
                draw_circle_v(collider.position, collider.radius, self.color)

        
        super().Draw()
        
        
class Raycast(Entity) : 
    
    
    """
    Clase que representa un rayo para detectar colisiones entre entidades en 2D.

    Atributos:
    - `start_position`: Vector2, posición inicial del rayo en el espacio 2D.
    - `end_position`: Vector2, posición final del rayo en el espacio 2D.
    - `layer`: Int, capa en la que se encuentra el rayo, útil para filtrar colisiones.
    - `use_basic_model`: Bool, indica si se usa un modelo visual básico para representar el rayo.
    - `color`: Color, el color del rayo para su representación visual.
    - `size`: Vector2, tamaño de la entidad (aunque no es directamente relevante para el rayo).
    - `Colliders`: Lista global que almacena todos los colisionadores, incluyendo el rayo.

    Métodos:
    - `__init__()`: Inicializa el rayo con sus atributos, añadiéndolo a la lista de colisionadores.
    - `Delect()`: Elimina el rayo de la lista de colisionadores y lo borra del sistema.
    - `__set_point__(point, use_rot)`: Calcula la posición en el espacio 2D considerando la rotación y la escala.
    - `Collider()`: Calcula el punto final del rayo como un punto de colisión en el mundo.
    - `IsCollider()`: Verifica si el rayo está colisionando con algún objeto en su capa.
    - `GetCollider()`: Comprueba las colisiones del rayo con otros colisionadores (cajas, círculos) y retorna el colisionador con el que choca.
    - `Update(dt)`: Actualiza el estado del rayo, cambiando su color si detecta una colisión.
    - `Draw()`: Dibuja el rayo entre la posición inicial y la final, y dibuja un círculo en el punto de colisión.
    """
    
    
    def __init__(
        self, parent, 
        name = "Entity", 
        position=Vector2(), 
        scale=Vector2(1,1), 
        size = Vector2(100, 100),
        rotation = 0, 
        origin=Vector2(0,0), 
        start_positoin = Vector2(), 
        end_position = Vector2(),
        layer : int = 0,
        use_basic_model = False,
        ):
        super().__init__(parent, name, position, scale, rotation, origin)
        
        self.start_position = start_positoin
        self.end_position = end_position
        self.layer = layer
        self.use_basic_model = use_basic_model
        self.color = BLUE
        self.size = size
        Colliders.append(self)
        
    def Delect(self):
        super().Delect()
        if self in Colliders : 
            Colliders.remove(self)
    
    def __set_point__(self, point : Vector2, use_rot = False) -> Vector2 : 
        world = vector2_subtract(self.world_position, vector2_multiply(self.origin, self.size))
        post = vector2_add(world, point)
        if use_rot :
            post = vector2_rotate(self.position, math.radians(self.world_rotation))
        return post
    
    def Collider(self) -> Vector2 :
        return self.__set_point__(self.end_position, use_rot=True)
    
    def IsCollider(self) -> bool : 
        if self.GetCollider() : return True
        return False
    
    def GetCollider(self,) -> object:
        for entity in Colliders:
            entity :  Rectangle | Circle | Capsule
            if entity.layer != self.layer : continue
            if self == entity : continue
            
            # Detectar todas las combinaciones de colisionadores
            # Colisiones de BOX con otros tipos
            if entity.how_collider == "BOX":
                if check_collision_point_rec(self.Collider(), entity.Collider()):
                    return entity
            
            elif entity.how_collider == "CIRCLE":
                if check_collision_point_circle(self.Collider(), entity.Collider()):
                    return entity
        return None

    def Update(self, dt):
        if self.use_basic_model == True : 
            if self.IsCollider() == True:
                self.color = RED
            else:
                self.color = BLUE
        return super().Update(dt)

    def Draw(self):
        
        if self.use_basic_model == True :
            
            start_pos = self.__set_point__(self.start_position)
            end_pos = self.__set_point__(self.end_position, use_rot=True)
            draw_line_v(start_pos, end_pos, self.color)
            
            draw_circle_v(end_pos, 5, self.color)
        
        return super().Draw()