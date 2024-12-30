from pyray import *
import math


Scenas = {
    
}
Entitys = []
Type_Entitys = {
}
Colliders = [
]




# Objectos que el motor no tiene, pero que se pueden usar.


class Circle: 
    """
    Crea Una Circle en 2D

    - `position`: Vector2, la posición central de la cápsula.
    - `radius`: Radio de los círculos que forman los extremos de la cápsula.
    
    """
    
    def __init__(self, position : Vector2 = Vector2(), radius : float = 0 ):
        self.position = position 
        self.radius = radius

class Capsule :
    
    """
    Crea Una Capsula en 2D

    - `position`: Vector2, la posición central de la cápsula.
    - `radius`: Radio de los círculos que forman los extremos de la cápsula.
    - `dimension`: Longitud del cuerpo de la cápsula (distancia entre los dos círculos).
    - `direction`: Dirección de la cápsula, "VERTICAL" o "HORIZONTAL".
    
    """
    
    def __init__(self, position = Vector2(), radius : float = 0, dimension: float = 0, direction: str = "VERTICAL"):
        self.position = position
        self.radius = radius
        self.dimension = dimension
        self.direction = direction
    
    def get_endpoints(self):
        """
        Calcula las posiciones de los extremos de la cápsula (los centros de los círculos en ambos extremos).
        """
        if self.direction == "HORIZONTAL":
            end1 = Vector2(self.position.x - self.dimension, self.position.y)
            end2 = Vector2(self.position.x + self.dimension, self.position.y)
        elif self.direction == "VERTICAL":
            end1 = Vector2(self.position.x, self.position.y - self.dimension)
            end2 = Vector2(self.position.x, self.position.y + self.dimension)
        return end1, end2



def draw_capsule_2d(capsule : Capsule,  color: Color = WHITE):
    """
    Dibuja una cápsula en 2D con dos círculos en los extremos y un rectángulo que los conecta.

    - `position`: Vector2, la posición central de la cápsula.
    - `radius`: Radio de los círculos que forman los extremos de la cápsula.
    - `dimension`: Longitud del cuerpo de la cápsula (distancia entre los dos círculos).
    - `direction`: Dirección de la cápsula, "VERTICAL" o "HORIZONTAL".
    - `color`: Color de la cápsula (opcional, por defecto es WHITE).
    """
    
    position = capsule.position
    radius = capsule.radius
    dimension = capsule.dimension
    direction = capsule.direction
    
    # Calculamos las posiciones de los dos extremos de la cápsula en función de la dirección
    if direction == "HORIZONTAL":
        end1 = Vector2(position.x - dimension, position.y)  # Extremo 1 (izquierdo)
        end2 = Vector2(position.x + dimension, position.y)  # Extremo 2 (derecho)
        rect_position = Vector2(end1.x, end1.y - radius)  # Posición del rectángulo entre los círculos
        rect_size = Vector2(dimension * 2, radius * 2)  # Ancho = distancia entre círculos, Alto = diámetro de los círculos
        # Dibuja los dos círculos en los extremos de la cápsula
        draw_circle_v(end1, radius, color)  # Círculo en el extremo 1
        draw_circle_v(end2, radius, color)  # Círculo en el extremo 2
        # Dibuja el rectángulo que conecta los dos círculos
        draw_rectangle_v(rect_position, rect_size, color)  # Rectángulo entre los extremos
    elif direction == "VERTICAL":
        end1 = Vector2(position.x, position.y - dimension)  # Extremo 1 (superior)
        end2 = Vector2(position.x, position.y + dimension)  # Extremo 2 (inferior)
        rect_position = Vector2(end1.x - radius, end1.y)  # Posición del rectángulo entre los círculos
        rect_size = Vector2(radius * 2, dimension * 2)  # Ancho = diámetro de los círculos, Alto = distancia entre círculos
        # Dibuja los dos círculos en los extremos de la cápsula
        draw_circle_v(end1, radius, color)  # Círculo en el extremo 1
        draw_circle_v(end2, radius, color)  # Círculo en el extremo 2
        
        # Dibuja el rectángulo que conecta los dos círculos
        draw_rectangle_v(rect_position, rect_size, color)  # Rectángulo entre los extremos
        

def check_collision_circle_rectangle(circle: Circle, rect: Rectangle) -> bool:
    """
    Verifica si un círculo colisiona con un rectángulo.

    - `circle`: Instancia de la clase `Circle`.
    - `rect`: Instancia de la clase `Rectangle`.
    
    Devuelve `True` si hay colisión, de lo contrario, `False`.
    """
    
    # Encontrar el punto más cercano en el rectángulo al centro del círculo
    closest_x = max(rect.x, min(circle.position.x, rect.x + rect.width))
    closest_y = max(rect.y, min(circle.position.y, rect.y + rect.height))
    
    # Calcular la distancia entre el círculo y el punto más cercano en el rectángulo
    distance_x = circle.position.x - closest_x
    distance_y = circle.position.y - closest_y
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
    
    # Si la distancia es menor o igual al radio, hay colisión
    return distance <= circle.radius


def get_closest_point_to_rectangle(point: Vector2, rectangle: Rectangle) -> Vector2:
    """Obtiene el punto más cercano en un rectángulo desde un punto dado."""
    # Clampear las coordenadas del punto dentro de los límites del rectángulo
    closest_x = max(rectangle.x, min(point.x, rectangle.x + rectangle.width))
    closest_y = max(rectangle.y, min(point.y, rectangle.y + rectangle.height))
    
    return Vector2(closest_x, closest_y)