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
    - `origin`: Punto de referencia para la posición del colisionador, generalmente el centro.
    - `use_basis_model`: Bool, indica si se usa el modelo base para el colisionador.
    - `how_collider`: Tipo de colisionador, puede ser "BOX", "CIRCLE" o "CAPSULE".
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
        rotation = 0, 
        origin=Vector2(0.2), 
        use_basis_model = False, 
        how_collider : str = "BOX",
        dimension: float = 0, 
        direction: str = "VERTICAL",
        use_repel : bool = False,
        color : Color = BLUE,
        velocity : float = 0
        ):
        
        super().__init__(parent, name, position, scale, rotation, origin)

        self.type = "COLLIDER"
        self.use_basis_model = use_basis_model
        self.how_collider = how_collider
        self.dimension = dimension
        self.direction = direction
        self.use_repel = use_repel
        self.color = color
        self.velocity = velocity
        
        Colliders.append(self)

        
    def __repel__(self, other_obj, dt) -> None:
        """Repels this entity from the other entity based on their collider types."""

        self_obj = self if self.parent.type == "SCENA" else self.parent
        
        
        self_collider : Rectangle | Circle | Capsule = self.Collider()
        other_collider : Rectangle | Circle | Capsule = other_obj.Collider()
        
        if self_obj.how_collider == "BOX" and other_obj.how_collider == "BOX":
            
            
            dir = Vector2(self_collider.x - other_collider.x, self_collider.y - other_collider.y)
            dir = vector2_normalize(dir)
            
            self_obj.position.x += dir.x * self.velocity * 2 * dt
            self_obj.position.y += dir.y * self.velocity * 2 * dt


    # Crea el Collider Basico de las Entidades
    def Collider(self) -> object: 
        
        scale_x = self.world_scale.x * 100
        scale_y = self.world_scale.y * 100
        position_x = self.world_position.x - (self.origin.x * 100)
        position_y = self.world_position.y - (self.origin.y * 100)
        radius = (self.world_scale.x * 100 + self.world_scale.y * 100) / 2
        
        if self.how_collider == "BOX" : 
            return Rectangle(
                position_x, position_y, scale_x, scale_y
            )
        elif self.how_collider == "CIRCLE" : 
            return Circle(
                position=Vector2(position_x, position_y), radius=radius
            )
        
        elif self.how_collider == "CAPSULE" : 
            return Capsule(
                Vector2(position_x, position_y), radius=radius, 
                dimension=self.dimension * scale_x if self.direction == "HORIZONTAL" else scale_y, 
                direction=self.direction
            )
    
    """
    # Detectar el collider con las otras Entitys
    """
    def IsCollider(self, filter : list = {}) -> bool : 
        if self.GetCollider(filter) : return True
        return False
    
    def GetCollider(self, filter: list = []) -> object:
        for entity in Colliders:
            entity :  Rectangle | Circle | Capsule
            if entity in filter:
                continue
            
            if self.name == entity.name : continue
            
            # Detectar todas las combinaciones de colisionadores
            # Colisiones de BOX con otros tipos
            if self.how_collider == "BOX":
                if entity.how_collider == "BOX":
                    if check_collision_recs(self.Collider(), entity.Collider()):
                        return entity
                
                elif entity.how_collider == "CIRCLE":
                    if check_collision_circle_rectangle(entity.Collider(), self.Collider()):
                        return entity
                
                elif entity.how_collider == "CAPSULE":
                    # Verificar colisión entre BOX y CAPSULE (puedes implementar esto según sea necesario)
                    if check_collision_capsule_box(entity.Collider(), self.Collider()):
                        return entity

            # Colisiones de CIRCLE con otros tipos
            elif self.how_collider == "CIRCLE":
                if entity.how_collider == "CIRCLE":
                    if check_collision_circles(self.Collider().position, self.Collider().radius, entity.Collider().position, entity.Collider().radius):
                        return entity
                
                elif entity.how_collider == "BOX":
                    if check_collision_circle_rectangle(self.Collider(), entity.Collider()):
                        return entity
                
                
                elif entity.how_collider == "CAPSULE":
                    # Verificar colisión entre CIRCLE y CAPSULE (puedes implementar esto según sea necesario)
                    if check_collision_circle_capsule(self.Collider(), entity.Collider()):
                        return entity

            # Colisiones de CAPSULE con otros tipos
            elif self.how_collider == "CAPSULE":
                if entity.how_collider == "CAPSULE":
                    # Verificar colisión entre CAPSULE y CAPSULE (puedes implementar esto según sea necesario)
                    if check_collision_capsule(self.Collider(), entity.Collider()):
                        return entity
                
                elif entity.how_collider == "BOX":
                    # Verificar colisión entre CAPSULE y BOX (puedes implementar esto según sea necesario)
                    if check_collision_capsule_box(self.Collider(), entity.Collider()):
                        return entity
                
                elif entity.how_collider == "CIRCLE":
                    # Verificar colisión entre CAPSULE y CIRCLE (puedes implementar esto según sea necesario)
                    if check_collision_circle_capsule(entity.Collider(), self.Collider()):
                        return entity

        return None

    
    def Delect(self):
        super().Delect()
        if self in Colliders : 
            Colliders.remove(self)
    
    def Update(self, dt):
        
        if self.use_repel :
            e = self.GetCollider(filter={self,})
            if e : 
                self.__repel__(e, dt) 
        return super().Update(dt)
    
    def Draw(self):
        
        if self.use_basis_model == True :
            collider : Rectangle | Circle | Capsule = self.Collider()
            if self.how_collider == "BOX" :
                draw_rectangle_v(
                    Vector2(collider.x, collider.y), Vector2(collider.width, collider.height), self.color
                    ) 
            elif self.how_collider == "CIRCLE" : 
                draw_circle_v(collider.position, collider.radius, self.color)

        
            elif self.how_collider == "CAPSULE" : 
                draw_capsule_2d(collider, self.color)
        
        super().Draw()
        
        
