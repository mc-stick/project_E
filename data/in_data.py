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

class RectanglePolygon : 
    
    def __init__(self, v1 : Vector2, v2 : Vector2, v3 : Vector2, v4 : Vector2):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        
    


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

def check_collision_rectanglepolygon(RP_A : RectanglePolygon, RP_B: RectanglePolygon) -> bool:
    
    """
    Verifica si dos polígonos rectangulares colisionan usando el Teorema de Separación de Ejes (SAT).

    - `RP_A`: Instancia de la clase `RectanglePolygon` (con vértices rotados).
    - `RP_B`: Instancia de la clase `RectanglePolygon` (con vértices rotados).
    
    Devuelve `True` si hay colisión, de lo contrario, `False`.
    """

    def get_edges(polygon):
        """ Obtiene los bordes del polígono como vectores. """
        return [
            vector2_subtract(polygon.v2, polygon.v1),
            vector2_subtract(polygon.v3, polygon.v2),
            vector2_subtract(polygon.v4, polygon.v3),
            vector2_subtract(polygon.v1, polygon.v4)
        ]

    def normalize_vector(v):
        """ Normaliza un vector. """
        length = (v.x ** 2 + v.y ** 2) ** 0.5
        if length != 0:
            return Vector2(v.x / length, v.y / length)
        return Vector2(0, 0)

    def dot_product(v1, v2):
        """ Calcula el producto punto de dos vectores. """
        return v1.x * v2.x + v1.y * v2.y

    def project_polygon(polygon, axis):
        """ Proyecta un polígono en un eje y devuelve el mínimo y máximo valores. """
        vertices = [polygon.v1, polygon.v2, polygon.v3, polygon.v4]
        min_proj = dot_product(vertices[0], axis)
        max_proj = min_proj
        for vertex in vertices[1:]:
            projection = dot_product(vertex, axis)
            if projection < min_proj:
                min_proj = projection
            if projection > max_proj:
                max_proj = projection
        return min_proj, max_proj

    def overlap(min_a, max_a, min_b, max_b):
        """ Verifica si dos proyecciones se solapan. """
        return max_a >= min_b and max_b >= min_a

    # Obtener los bordes de ambos polígonos
    edges_A = get_edges(RP_A)
    edges_B = get_edges(RP_B)

    # Probar los ejes de separación (bordes normalizados) de ambos polígonos
    for edge in edges_A + edges_B:
        axis = normalize_vector(Vector2(-edge.y, edge.x))  # Perpendicular al borde

        # Proyectar ambos polígonos en el eje de separación actual
        min_A, max_A = project_polygon(RP_A, axis)
        min_B, max_B = project_polygon(RP_B, axis)

        # Verificar si las proyecciones no se solapan
        if not overlap(min_A, max_A, min_B, max_B):
            return False  # Si no se solapan, no hay colisión

    # Si todas las proyecciones se solapan, hay colisión
    return True


def check_collision_rectanglepolygon_circle(rect: RectanglePolygon, circle: Circle) -> bool:
    """
    Verifica si un rectángulo colisiona con un círculo.

    - `rect`: Instancia de la clase `RectanglePolygon` (con vértices rotados).
    - `circle`: Instancia de la clase `Circle`.
    
    Devuelve `True` si hay colisión, de lo contrario, `False`.
    """

    def vector2_length(v):
        """ Devuelve la longitud (magnitud) de un vector 2D. """
        return (v.x ** 2 + v.y ** 2) ** 0.5

    def vector2_normalize(v):
        """ Normaliza un vector. """
        length = vector2_length(v)
        if length != 0:
            return Vector2(v.x / length, v.y / length)
        return Vector2(0, 0)

    def closest_point_on_line_segment(p, a, b):
        """ Calcula el punto más cercano a `p` en el segmento de línea de `a` a `b`. """
        ab = vector2_subtract(b, a)
        t = dot_product(vector2_subtract(p, a), ab) / dot_product(ab, ab)
        t = max(0, min(1, t))  # Asegurarse de que t esté entre 0 y 1
        return Vector2(a.x + t * ab.x, a.y + t * ab.y)

    def dot_product(v1, v2):
        """ Calcula el producto punto de dos vectores. """
        return v1.x * v2.x + v1.y * v2.y

    # Paso 1: Verificar si el centro del círculo está dentro del rectángulo usando SAT
    def get_edges(polygon):
        """ Obtiene los bordes del polígono como vectores. """
        return [
            vector2_subtract(polygon.v2, polygon.v1),
            vector2_subtract(polygon.v3, polygon.v2),
            vector2_subtract(polygon.v4, polygon.v3),
            vector2_subtract(polygon.v1, polygon.v4)
        ]

    def project_polygon(polygon, axis):
        """ Proyecta un polígono en un eje y devuelve el mínimo y máximo valores. """
        vertices = [polygon.v1, polygon.v2, polygon.v3, polygon.v4]
        min_proj = dot_product(vertices[0], axis)
        max_proj = min_proj
        for vertex in vertices[1:]:
            projection = dot_product(vertex, axis)
            if projection < min_proj:
                min_proj = projection
            if projection > max_proj:
                max_proj = projection
        return min_proj, max_proj

    def project_circle(circle, axis):
        """ Proyecta un círculo en un eje y devuelve el mínimo y máximo valores. """
        center_projection = dot_product(circle.position, axis)
        return center_projection - circle.radius, center_projection + circle.radius

    def overlap(min_a, max_a, min_b, max_b):
        """ Verifica si dos proyecciones se solapan. """
        return max_a >= min_b and max_b >= min_a

    # Obtener los bordes del rectángulo
    edges = get_edges(rect)

    # Probar los ejes de separación (bordes normalizados) del rectángulo
    for edge in edges:
        axis = vector2_normalize(Vector2(-edge.y, edge.x))  # Perpendicular al borde

        # Proyectar el rectángulo y el círculo en el eje de separación actual
        min_rect, max_rect = project_polygon(rect, axis)
        min_circle, max_circle = project_circle(circle, axis)

        # Verificar si las proyecciones no se solapan
        if not overlap(min_rect, max_rect, min_circle, max_circle):
            return False  # Si no se solapan, no hay colisión

    # Paso 2: Verificar si el círculo colisiona con alguno de los bordes del rectángulo
    vertices = [rect.v1, rect.v2, rect.v3, rect.v4]
    for i in range(4):
        # Obtener los dos vértices del borde actual
        v1 = vertices[i]
        v2 = vertices[(i + 1) % 4]

        # Encontrar el punto más cercano en el borde al centro del círculo
        closest_point = closest_point_on_line_segment(circle.position, v1, v2)

        # Verificar si la distancia desde el centro del círculo a ese punto es menor que el radio
        distance = vector2_length(vector2_subtract(circle.position, closest_point))
        if distance < circle.radius:
            return True  # Hay colisión

    return False  # No hay colisión


def check_collision_rectanglepolygon_rectangle(RP: RectanglePolygon, R: Rectangle) -> bool:
    """
    Verifica si un `RectanglePolygon` colisiona con un `Rectangle` no rotado.

    - `RP`: Instancia de la clase `RectanglePolygon` (con vértices rotados).
    - `R`: Instancia de la clase `Rectangle` (alineado con los ejes X e Y).
    
    Devuelve `True` si hay colisión, de lo contrario, `False`.
    """

    def get_edges(polygon):
        """ Obtiene los bordes del polígono como vectores. """
        return [
            vector2_subtract(polygon.v2, polygon.v1),
            vector2_subtract(polygon.v3, polygon.v2),
            vector2_subtract(polygon.v4, polygon.v3),
            vector2_subtract(polygon.v1, polygon.v4)
        ]

    def normalize_vector(v):
        """ Normaliza un vector. """
        length = (v.x ** 2 + v.y ** 2) ** 0.5
        if length != 0:
            return Vector2(v.x / length, v.y / length)
        return Vector2(0, 0)

    def dot_product(v1, v2):
        """ Calcula el producto punto de dos vectores. """
        return v1.x * v2.x + v1.y * v2.y

    def project_polygon(polygon, axis):
        """ Proyecta un polígono en un eje y devuelve el mínimo y máximo valores. """
        vertices = [polygon.v1, polygon.v2, polygon.v3, polygon.v4]
        min_proj = dot_product(vertices[0], axis)
        max_proj = min_proj
        for vertex in vertices[1:]:
            projection = dot_product(vertex, axis)
            if projection < min_proj:
                min_proj = projection
            if projection > max_proj:
                max_proj = projection
        return min_proj, max_proj

    def project_rectangle(rect, axis):
        """ Proyecta un rectángulo alineado con los ejes X e Y sobre un eje. """
        vertices = [
            Vector2(rect.x, rect.y),
            Vector2(rect.x + rect.width, rect.y),
            Vector2(rect.x, rect.y + rect.height),
            Vector2(rect.x + rect.width, rect.y + rect.height)
        ]
        min_proj = dot_product(vertices[0], axis)
        max_proj = min_proj
        for vertex in vertices[1:]:
            projection = dot_product(vertex, axis)
            if projection < min_proj:
                min_proj = projection
            if projection > max_proj:
                max_proj = projection
        return min_proj, max_proj

    def overlap(min_a, max_a, min_b, max_b):
        """ Verifica si dos proyecciones se solapan. """
        return max_a >= min_b and max_b >= min_a

    # Obtener los bordes del RectanglePolygon
    edges_RP = get_edges(RP)

    # Agregar los ejes X e Y del rectángulo alineado
    axes = edges_RP + [Vector2(1, 0), Vector2(0, 1)]  # Agregar ejes X e Y

    # Probar los ejes de separación de ambos
    for edge in axes:
        axis = normalize_vector(Vector2(-edge.y, edge.x))  # Perpendicular al borde

        # Proyectar ambos en el eje de separación actual
        min_RP, max_RP = project_polygon(RP, axis)
        min_R, max_R = project_rectangle(R, axis)

        # Verificar si las proyecciones no se solapan
        if not overlap(min_RP, max_RP, min_R, max_R):
            return False  # Si no se solapan, no hay colisión

    # Si todas las proyecciones se solapan, hay colisión
    return True
