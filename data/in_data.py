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
        
def check_collision_capsule(capsule1: Capsule, capsule2: Capsule) -> bool:
    """
    Comprueba si dos cápsulas colisionan entre sí en 2D.

    - `capsule1`: Primer objeto de la clase Capsule.
    - `capsule2`: Segundo objeto de la clase Capsule.
    
    Retorna True si hay colisión, de lo contrario False.
    """
    
    # Obtener los extremos de ambas cápsulas
    cap1_end1, cap1_end2 = capsule1.get_endpoints()
    cap2_end1, cap2_end2 = capsule2.get_endpoints()

    # Paso 1: Verificar si los círculos de los extremos de capsule1 colisionan con los círculos de los extremos de capsule2
    if (check_collision_circles(cap1_end1, capsule1.radius, cap2_end1, capsule2.radius) or
        check_collision_circles(cap1_end1, capsule1.radius, cap2_end2, capsule2.radius) or
        check_collision_circles(cap1_end2, capsule1.radius, cap2_end1, capsule2.radius) or
        check_collision_circles(cap1_end2, capsule1.radius, cap2_end2, capsule2.radius)):
        return True

    # Paso 2: Verificar si los extremos de capsule1 colisionan con el cuerpo de capsule2
    if (check_collision_point_capsule(cap1_end1, capsule2) or
        check_collision_point_capsule(cap1_end2, capsule2)):
        return True

    # Paso 3: Verificar si los extremos de capsule2 colisionan con el cuerpo de capsule1
    if (check_collision_point_capsule(cap2_end1, capsule1) or
        check_collision_point_capsule(cap2_end2, capsule1)):
        return True

    # Paso 4: Verificar si los cuerpos de ambas cápsulas se superponen (mediante la proyección en el eje de ambas)
    if check_collision_capsule_bodies(capsule1, capsule2):
        return True

    return False

def check_collision_point_capsule(point: Vector2, capsule: Capsule) -> bool:
    """
    Comprueba si un punto colisiona con el cuerpo (rectángulo) de una cápsula.

    - `point`: Vector2, posición del punto.
    - `capsule`: Objeto de la clase Capsule.
    
    Retorna True si el punto colisiona con el cuerpo de la cápsula, de lo contrario False.
    """
    # Obtener los extremos de la cápsula
    end1, end2 = capsule.get_endpoints()

    # Calcular el vector del cuerpo de la cápsula
    capsule_axis = end2 - end1
    capsule_axis_length = capsule_axis.length()

    # Proyectar el punto sobre el eje de la cápsula
    point_to_end1 = point - end1
    projection_length = (point_to_end1.dot(capsule_axis) / capsule_axis_length)

    # Clampear la proyección dentro de los límites del cuerpo de la cápsula
    projection_length = max(0, min(projection_length, capsule_axis_length))

    # Obtener el punto más cercano en el cuerpo de la cápsula
    closest_point = end1 + capsule_axis.normalized() * projection_length

    # Comprobar si el punto está lo suficientemente cerca del cuerpo de la cápsula
    return (point - closest_point).length() <= capsule.radius

def check_collision_capsule_bodies(capsule1: Capsule, capsule2: Capsule) -> bool:
    """
    Comprueba si los cuerpos de dos cápsulas colisionan entre sí.
    
    - `capsule1`: Primer objeto de la clase Capsule.
    - `capsule2`: Segundo objeto de la clase Capsule.
    
    Retorna True si los cuerpos de las cápsulas se superponen, de lo contrario False.
    """
    # Obtener los extremos de ambas cápsulas
    cap1_end1, cap1_end2 = capsule1.get_endpoints()
    cap2_end1, cap2_end2 = capsule2.get_endpoints()

    # Proyectar el cuerpo de una cápsula sobre el eje de la otra y comprobar la superposición
    return (check_collision_point_capsule(cap1_end1, capsule2) or
            check_collision_point_capsule(cap1_end2, capsule2) or
            check_collision_point_capsule(cap2_end1, capsule1) or
            check_collision_point_capsule(cap2_end2, capsule1))

def check_collision_circle_capsule(circle_pos: Vector2, circle_radius: float, capsule: Capsule) -> bool:
    """
    Comprueba si un círculo colisiona con una cápsula 2D.

    - `circle_pos`: Posición del centro del círculo.
    - `circle_radius`: Radio del círculo.
    - `capsule`: Objeto de la clase Capsule.
    
    Retorna True si hay colisión, de lo contrario False.
    """
    
    # Obtiene las posiciones de los extremos de la cápsula
    end1, end2 = capsule.get_endpoints()

    # Verifica la colisión con los círculos en los extremos de la cápsula
    if check_collision_circles(circle_pos, circle_radius, end1, capsule.radius) or \
       check_collision_circles(circle_pos, circle_radius, end2, capsule.radius):
        return True

    # Calcula el vector desde el extremo 1 hasta el extremo 2 de la cápsula
    capsule_axis = end2 - end1
    capsule_axis_length = capsule_axis.length()

    # Proyección del círculo sobre el eje de la cápsula
    circle_to_end1 = circle_pos - end1
    projection_length = (circle_to_end1.dot(capsule_axis) / capsule_axis_length)

    # Clampa la proyección al segmento de la cápsula
    projection_length = max(0, min(projection_length, capsule_axis_length))

    # Calcula la posición proyectada del círculo sobre el eje de la cápsula
    closest_point = end1 + capsule_axis.normalized() * projection_length

    # Comprueba la distancia desde el círculo al punto más cercano en el eje de la cápsula
    return (circle_pos - closest_point).length() <= (circle_radius + capsule.radius)

def check_collision_capsule_box(capsule, box):
    """
    Verifica si una cápsula y una caja colisionan.
    
    - capsule: Es una instancia de la clase Capsule, con posición, radio, dimensión y dirección.
    - box: Es un rectángulo definido por su posición y tamaño.
    
    Retorna True si colisionan, de lo contrario False.
    """

    # Obtener el cuerpo rectangular de la cápsula
    if capsule.direction == "HORIZONTAL":
        capsule_body = Rectangle(
            capsule.position.x - capsule.dimension / 2,  # inicio del cuerpo
            capsule.position.y - capsule.radius,         # parte superior del cuerpo
            capsule.dimension,                           # largo del cuerpo
            capsule.radius * 2                           # altura del cuerpo (diámetro)
        )
    else:  # VERTICAL
        capsule_body = Rectangle(
            capsule.position.x - capsule.radius,          # lado izquierdo del cuerpo
            capsule.position.y - capsule.dimension / 2,   # inicio del cuerpo
            capsule.radius * 2,                           # ancho del cuerpo (diámetro)
            capsule.dimension                            # largo del cuerpo
        )

    # Verificar si el cuerpo de la cápsula colisiona con el box (rectángulo vs rectángulo)
    if check_collision_recs(capsule_body, box):
        return True

    # Verificar si los extremos circulares de la cápsula colisionan con el box (círculo vs rectángulo)
    if capsule.direction == "HORIZONTAL":
        # Los dos extremos son círculos en los extremos del cuerpo de la cápsula
        end1 = Vector2(capsule.position.x - capsule.dimension / 2, capsule.position.y)
        end2 = Vector2(capsule.position.x + capsule.dimension / 2, capsule.position.y)
    else:  # VERTICAL
        end1 = Vector2(capsule.position.x, capsule.position.y - capsule.dimension / 2)
        end2 = Vector2(capsule.position.x, capsule.position.y + capsule.dimension / 2)

    # Verificar colisión círculo vs caja para ambos extremos
    if check_collision_circle_rec(end1, capsule.radius, box) or check_collision_circle_rec(end2, capsule.radius, box):
        return True

    return False

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