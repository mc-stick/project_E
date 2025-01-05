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
    - `how_collider`: Tipo de colisionador, puede ser "BOX", "CIRCLE", "ROT_BOX".
    - `dimension`: Longitud del cuerpo de la cápsula, relevante solo para cápsulas.
    - `direction`: Dirección de la cápsula, "VERTICAL" o "HORIZONTAL".
    - `vector_distance_to_sort` : Vector2, vector de distancia para ordenar las entidades.
    - `min_activation_distance` : float, distancia mínima para activar la entidad.
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
        origin=Vector2(0.5,0.5), 
        use_basic_model = False, 
        how_collider : str = "BOX",
        use_repel : bool = False,
        color : Color = BLUE,
        layer : dict = {0},
        vector_distance_to_sort : Vector2 = Vector2(0,0),
        min_activation_distance : float = 0 ,
        ):
        
        super().__init__(parent, name, position, scale, rotation, origin, vector_distance_to_sort, min_activation_distance)

        self.type = "COLLIDER"
        self.use_basic_model = use_basic_model
        self.how_collider = how_collider
        self.use_repel = use_repel
        self.color = color
        self.layer = layer
        self.size = size
        self.collision_range_to_use = 10
        
    
        Colliders.append(self)

        
    def __repel__(self, other_obj, dt) -> None:
        """Repels this entity from the other entity based on their collider types."""
        other_obj: Collider = other_obj
        self_obj = self if self.parent.type == "SCENA" else self.parent
        
    
        # Obtener el tipo de colisionador
        self_collider_type = self.how_collider
        other_collider_type = other_obj.how_collider

        normal = Vector2(0, 0)
        penetration_depth = 0
        
        def dot_product(v1, v2):
                """ Calcula el producto punto de dos vectores. """
                return v1.x * v2.x + v1.y * v2.y

        # Función para proyectar un polígono en un eje
        def project_polygon(polygon: RectanglePolygon, axis: Vector2):
            min_proj = float('inf')
            max_proj = float('-inf')
            
            # Proyectar todos los vértices del polígono en el eje dado
            for vertex in [polygon.v1, polygon.v2, polygon.v3, polygon.v4]:
                projection = dot_product(vertex, axis)  # Producto escalar para proyección
                min_proj = min(min_proj, projection)
                max_proj = max(max_proj, projection)
            return min_proj, max_proj
        
        # Función para verificar si hay superposición entre proyecciones
        def overlap_on_axis(polygon1: RectanglePolygon, polygon2: RectanglePolygon, axis: Vector2):
            min1, max1 = project_polygon(polygon1, axis)
            min2, max2 = project_polygon(polygon2, axis)
            
            # Verificar si hay una superposición
            if max1 < min2 or max2 < min1:
                return False, 0  # No hay colisión
            overlap = min(max1, max2) - max(min1, min2)  # Calcular superposición
            return True, overlap
        
        
        
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
                penetration_depth = overlap_x
                if self_collider.x + self_collider.width > other_collider.x + other_collider.width:
                    normal = Vector2(1, 0)  # Repulsión hacia la derecha
                else:
                    normal = Vector2(-1, 0)  # Repulsión hacia la izquierda
            else:
                penetration_depth = overlap_y
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
            penetration_depth = (self_collider.radius + other_collider.radius) - dist

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
            dist = vector2_length(vector2_subtract(self_collider.position, closest_point))
            penetration_depth = self_collider.radius - dist
            
            # Calcular la dirección de la repulsión
            normal = vector2_normalize(vector2_subtract(self_collider.position, closest_point))

        elif self_collider_type == "BOX" and other_collider_type == "CIRCLE":
            # Interacción inversa: RECTÁNGULO con CÍRCULO
            self_collider: Rectangle = self.Collider()
            other_collider: Circle = other_obj.Collider()

            # Obtener los puntos clave del rectángulo
            corners = self.Get_Corners()
            closest_point = get_closest_point_to_rectangle(other_collider.position, self_collider)
            dist = vector2_length(vector2_subtract(other_collider.position, closest_point))
            penetration_depth = other_collider.radius - dist
        
            # Calcular la dirección de la repulsión
            normal = vector2_normalize(vector2_subtract(other_collider.position, closest_point))

        

        elif self_collider_type == "ROT_BOX" and other_collider_type == "ROT_BOX":
            # Obtener los colliders de tipo "ROT_BOX"
            self_collider: RectanglePolygon = self.Collider()
            other_collider: RectanglePolygon = other_obj.Collider()



            # Crear una lista de todos los ejes (normales a los lados de los rectángulos)
            axes = [
                
                vector2_normalize(vector2_subtract(self_collider.v2, self_collider.v1)),
                vector2_normalize(vector2_subtract(self_collider.v3 , self_collider.v2)),
                vector2_normalize(vector2_subtract(other_collider.v2 , other_collider.v1)),
                vector2_normalize(vector2_subtract(other_collider.v3 , other_collider.v2))

            ]

            # Inicializar la menor penetración y el eje de colisión
            min_overlap = float('inf')
            collision_normal = None

            # Verificar colisiones en todos los ejes
            for axis in axes:
                collision, overlap = overlap_on_axis(self_collider, other_collider, axis)
                if not collision:
                    # Si no hay colisión en uno de los ejes, no hay colisión en absoluto
                    return False
                
                # Encontrar el eje con la menor superposición (penetración mínima)
                if overlap < min_overlap:
                    min_overlap = overlap
                    collision_normal = axis

            # Determinar la dirección de la repulsión
            penetration_depth = min_overlap
            normal = collision_normal

            # Ajustar la dirección de la normal si es necesario
            center_self = vector2_subtract(vector2_add(vector2_add(self_collider.v1, self_collider.v2 ), vector2_add(self_collider.v3, self_collider.v4)), Vector2(4, 4))
            center_other = vector2_subtract(vector2_add(vector2_add(other_collider.v1, other_collider.v2 ), vector2_add(other_collider.v3, other_collider.v4)), Vector2(4, 4))
            direction = vector2_normalize(vector2_subtract(center_other, center_self))
            
        elif self_collider_type == "ROT_BOX" and other_collider_type == "BOX":
            # Obtener los colliders de tipo "ROT_BOX" y "BOX"
            self_collider: RectanglePolygon = self.Collider()
            other_collider: Rectangle = other_obj.Collider()

            # Convertir el BOX en un RectanglePolygon para usar el mismo sistema de ejes y proyección
            other_polygon = RectanglePolygon(
                Vector2(other_collider.x, other_collider.y),
                Vector2(other_collider.x + other_collider.width, other_collider.y),
                Vector2(other_collider.x + other_collider.width, other_collider.y + other_collider.height),
                Vector2(other_collider.x, other_collider.y + other_collider.height)
            )

            # Ejes para ambos polígonos
            axes = [
                vector2_normalize(vector2_subtract(self_collider.v2, self_collider.v1)),
                vector2_normalize(vector2_subtract(self_collider.v3, self_collider.v2)),
                vector2_normalize(vector2_subtract(other_polygon.v2, other_polygon.v1)),
                vector2_normalize(vector2_subtract(other_polygon.v3, other_polygon.v2))
            ]

            # Colisión utilizando SAT
            min_overlap = float('inf')
            collision_normal = None

            for axis in axes:
                collision, overlap = overlap_on_axis(self_collider, other_polygon, axis)
                if not collision:
                    return False
                if overlap < min_overlap:
                    min_overlap = overlap
                    collision_normal = axis

            penetration_depth = min_overlap
            normal = collision_normal

            # Ajustar la dirección de la normal si es necesario
            center_self = vector2_subtract(vector2_add(vector2_add(self_collider.v1, self_collider.v2), vector2_add(self_collider.v3, self_collider.v4)), Vector2(4, 4))
            center_other = Vector2(other_collider.x + other_collider.width / 2, other_collider.y + other_collider.height / 2)
            direction = vector2_normalize(vector2_subtract(center_other, center_self))

        elif self_collider_type == "ROT_BOX" and other_collider_type == "CIRCLE":
            # Obtener los colliders de tipo "ROT_BOX" y "CIRCLE"
            self_collider: RectanglePolygon = self.Collider()
            other_collider: Circle = other_obj.Collider()

            # Ejes para el polígono rotado (ROT_BOX)
            axes = [
                vector2_normalize(vector2_subtract(self_collider.v2, self_collider.v1)),
                vector2_normalize(vector2_subtract(self_collider.v3, self_collider.v2))
            ]

            # Ejes adicionales: desde el centro del círculo hacia los vértices más cercanos del ROT_BOX
            closest_vertex = min([self_collider.v1, self_collider.v2, self_collider.v3, self_collider.v4], 
                                key=lambda v: vector2_length(vector2_subtract(v, other_collider.position)))
            axis_circle = vector2_normalize(vector2_subtract(closest_vertex, other_collider.position))
            axes.append(axis_circle)

            # Colisión utilizando SAT
            min_overlap = float('inf')
            collision_normal = None

            for axis in axes:
                collision, overlap = overlap_on_axis(self_collider, other_collider, axis)
                if not collision:
                    return False
                if overlap < min_overlap:
                    min_overlap = overlap
                    collision_normal = axis

            penetration_depth = min_overlap
            normal = collision_normal

            # Ajustar la dirección de la normal si es necesario
            center_self = vector2_subtract(vector2_add(vector2_add(self_collider.v1, self_collider.v2), vector2_add(self_collider.v3, self_collider.v4)), Vector2(4, 4))
            direction = vector2_normalize(vector2_subtract(other_collider.position, center_self))

           
        # Aplicar la repulsión (ajustar magnitudes según sea necesario)
        
        
        self_obj.position.x += normal.x * penetration_depth * (1/dt if dt != 0 else 0) * dt
        self_obj.position.y += normal.y * penetration_depth * (1/dt if dt != 0 else 0) * dt

    
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
        origin = vector2_multiply(self.origin, self.size)
        
        position_x = world_post.x - origin.x
        position_y = world_post.y - origin.y
        
        
        radius = (self.world_scale.x * self.size.x + self.world_scale.y * self.size.y) / 4
        
        if self.how_collider == "BOX" : 
            
            # Usar DrawRe
            return Rectangle(
                position_x, position_y, scale_x, scale_y
            )
        elif self.how_collider == "CIRCLE" : 
            
            return Circle(
                position=Vector2(position_x, position_y), radius=radius
            )
        
        elif self.how_collider == "ROT_BOX":
            # Obtener la posición central del colisionador
            center = Vector2((position_x + origin.x) , (position_y + origin.y) )
            
            # Definir las esquinas del rectángulo sin rotar
            v1 = Vector2(position_x, position_y)  # Esquina superior izquierda
            v2 = Vector2(position_x + scale_x, position_y)  # Esquina superior derecha
            v3 = Vector2(position_x + scale_x, position_y + scale_y)  # Esquina inferior derecha
            v4 = Vector2(position_x, position_y + scale_y)  # Esquina inferior izquierda
            
            # Función para rotar alrededor del centro
            def rotate_around_center(point, center, angle):
                # Trasladar el punto al origen respecto al centro
                translated_point = vector2_subtract(point, center)
                # Aplicar rotación
                rotated_point = vector2_rotate(translated_point, angle)
                # Trasladar de vuelta al espacio del colisionador
                return vector2_add(rotated_point, center)
            
            # Rotar los puntos alrededor del centro usando la rotación local
            angle = math.radians(self.world_rotation)
            v1 = rotate_around_center(v1, center, angle)
            v2 = rotate_around_center(v2, center, angle)
            v3 = rotate_around_center(v3, center, angle)
            v4 = rotate_around_center(v4, center, angle)
            
            return RectanglePolygon(v1, v2, v3, v4)
    """
    # Detectar el collider con las otras Entitys
    """
    def IsCollider(self) -> bool : 
        if self.visible == False : return False
        if self.GetCollider() : return True
        return False
    
    def GetCollider(self,) -> object:
        if self.visible == False : return
        self.distance_to_sort = vector2_distance(self.world_position, self.vector_distance_to_sort)
        for i, entity in enumerate(Colliders):
            entity :  Rectangle | Circle | Capsule
            
            if self.layer in entity.layer: continue
            if self == entity : continue
            if entity.type == "RAYCAST" : continue
            #if self.distance_to_sort > self.min_activation_distance or not self.min_activation_distance == 0 : continue
            if entity.visible == False : continue
            
            # Detectar todas las combinaciones de colisionadores
            # Colisiones de BOX con otros tipos
            if self.how_collider == "BOX":
                if entity.how_collider == "BOX":
                    if check_collision_recs(self.Collider(), entity.Collider()):
                        return entity
                        
                
                elif entity.how_collider == "CIRCLE":
                    if check_collision_circle_rectangle(entity.Collider(), self.Collider()):
                        return entity
                
                elif entity.how_collider == "ROT_BOX":
                    if check_collision_rectanglepolygon_rectangle(entity.Collider(), self.Collider()):
                        return entity

            # Colisiones de CIRCLE con otros tipos
            elif self.how_collider == "CIRCLE":
                if entity.how_collider == "CIRCLE":
                    if check_collision_circles(self.Collider().position, self.Collider().radius, entity.Collider().position, entity.Collider().radius):
                        return entity
                
                elif entity.how_collider == "BOX":
                    if check_collision_circle_rectangle(self.Collider(), entity.Collider()):
                        return entity
                    
                elif entity.how_collider == "ROT_BOX":
                    if check_collision_rectanglepolygon_circle(entity.Collider(), self.Collider()):
                        return entity

            elif self.how_collider == "ROT_BOX":
                
                if entity.how_collider == "BOX":
                    if check_collision_rectanglepolygon_rectangle(self.Collider(), entity.Collider()):
                        return entity
                
                if entity.how_collider == "CIRCLE":
                    if check_collision_rectanglepolygon_circle(self.Collider(), entity.Collider()):
                        return entity
                elif entity.how_collider == "ROT_BOX":
                    if check_collision_rectanglepolygon(entity.Collider(), self.Collider()):
                        return entity
            

            if self.collision_range_to_use != 0 :
                if i > self.collision_range_to_use:
                    break
            
        return None

    
    def Delect(self):
        super().Delect()
        if self in Colliders : 
            Colliders.remove(self)
    
    def Update(self, dt):
        
        if self.visible :
            self.distance_to_sort = vector2_distance(self.world_position, self.vector_distance_to_sort)
            if self.distance_to_sort < self.min_activation_distance or self.min_activation_distance == 0:
                if self.use_repel :
                    e = self.GetCollider()
                    if e is not None: 
                        self.__repel__(e, dt) 
                        
        return super().Update(dt)
    
    def Draw(self):
        
        if self.use_basic_model == True and self.visible:
            if self.distance_to_sort < self.min_activation_distance or self.min_activation_distance == 0 :
                collider : Rectangle | Circle | Capsule | RectanglePolygon = self.Collider()
                if self.how_collider == "BOX" :

                    draw_rectangle_v(
                        Vector2(collider.x, collider.y), Vector2(collider.width, collider.height), self.color
                        ) 
                    rect = Rectangle(collider.x, collider.y, collider.width, collider.height)
                    #color : Color = Color(int(self.color.r*1.2), int(self.color.g*1.2), int(self.color.b*1.2), int(self.color.a*1.2))
                    draw_rectangle_lines_ex(
                        rect, 2, BLACK
                    )
                    
                elif self.how_collider == "CIRCLE" : 
                    draw_circle_v(collider.position, collider.radius, self.color)

                elif self.how_collider == "ROT_BOX" : 
                    draw_line_v(collider.v1, collider.v2, self.color)
                    draw_line_v(collider.v2, collider.v3, self.color)
                    draw_line_v(collider.v3, collider.v4, self.color)
                    draw_line_v(collider.v4, collider.v1, self.color)
        
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
    - `vector_distance_to_sort` : Vector2, vector de distancia para ordenar las entidades.
    - `min_activation_distance` : float, distancia mínima para activar la entidad.

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
        name = "Raycast", 
        position=Vector2(), 
        scale=Vector2(1,1), 
        size = Vector2(100, 100),
        rotation = 0, 
        origin=Vector2(0,0), 
        start_positoin = Vector2(0,0), 
        end_position = Vector2(0,0),
        layer : list = {0},
        use_basic_model = False,
        vector_distance_to_sort : Vector2 = Vector2(0,0),
        min_activation_distance : float = 0 ,
        ):
        super().__init__(parent, name, position, scale, rotation, origin,  vector_distance_to_sort, min_activation_distance)
        
        self.type = "RAYCAST"
        self.start_position = start_positoin
        self.end_position = end_position
        self.layer = layer
        self.use_basic_model = use_basic_model
        self.color = BLUE
        self.size = size
        self.collision_range_to_use = 1
        Colliders.append(self)
        
    def Delect(self):
        super().Delect()
        if self in Colliders : 
            Colliders.remove(self)
    
    def __set_point__(self, point : Vector2) -> Vector2 : 
        world = vector2_subtract(self.world_position, vector2_multiply(self.origin, self.size))
        post = vector2_add(world, point)
        return post
    
    def Collider(self) -> Vector2 :
        return self.__set_point__(self.end_position)
    
    def IsCollider(self) -> bool : 
        if self.visible == False : return False
        if self.GetCollider() : return True
        return False
    
    def GetCollider(self) -> object:
        if self.visible == False : return None
        
        for i, entity in enumerate(Colliders):
            entity :  Rectangle | Circle | Capsule
            if self.layer in entity.layer : continue
            if self.parent == entity: continue
            if self == entity : continue
            if entity.type == "RAYCAST" : continue
            if entity.visible == False : continue
            
            # Detectar todas las combinaciones de colisionadores
            # Colisiones de BOX con otros tipos
            if entity.how_collider == "BOX":
                if check_collision_point_rec(self.Collider(), entity.Collider()):
                    return entity
            
            elif entity.how_collider == "CIRCLE":
                if check_collision_point_circle(self.Collider(), entity.Collider().position , entity.Collider().radius):
                    return entity
        
            if range != 0 : 
                if i > self.collision_range_to_use  : 
                    break
        return None

    def Update(self, dt):
        
        return super().Update(dt)

    def Draw(self):
        
        if self.use_basic_model == True :
            if self.distance_to_sort < self.min_activation_distance or self.min_activation_distance == 0:
                if self.IsCollider() == True:
                    self.color = RED
                else:
                    self.color = BLUE
                start_pos = self.__set_point__(self.start_position)
                end_pos = self.__set_point__(self.end_position)
                draw_line_v(start_pos, end_pos, self.color)
                
                draw_circle_v(end_pos, 5, self.color)
        
        return super().Draw()