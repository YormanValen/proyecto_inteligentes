import pygame
import sys
import json
import math
import random

# Inicialización de Pygame
pygame.init()

# Configuraciones de la ventana
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Asumiendo que tienes una imagen llamada 'taxi.png' en el mismo directorio que tu script
taxi_image_path = 'taxi.png'
taxi_image = pygame.image.load('images/taxi.png')

# Si necesitas cambiar el tamaño de la imagen
taxi_image = pygame.transform.scale(taxi_image, (50, 40))


# Define la fuente y el tamaño del texto
font_size = 16
font = pygame.font.Font(None, font_size)  # Usa una fuente predeterminada. Cambia None por la ruta a un archivo de fuente si deseas una fuente específica.

# Definir la posición y el tamaño del botón
button_position = (50, 50)  # Cambia según sea necesario
button_size = (200, 50)  # Cambia según sea necesario



# Coordenadas para la esquina superior izquierda (con un pequeño margen)
x = 10  # Margen desde el lado izquierdo
y = 10  # Margen desde el lado superior


# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (192, 192, 192)

taxi_positions = []


# Texto a mostrar
text_str = ""
text_str2 = ""
# Renderiza el texto en un objeto Surface
text_surface = font.render(text_str, True, BLACK)  # El segundo argumento es antialiasing. El tercer argumento es el color del texto.
text_surface = font.render(text_str2, True, BLACK)  # El segundo argumento es antialiasing. El tercer argumento es el color del texto.

# Copia el objeto Surface del texto en la pantalla principal
screen.blit(text_surface, (x, y))



# Tamaño de cada nodo y distancia entre ellos
node_radius = 10
distance_between_nodes = 100

# Cargar la ciudad desde el archivo JSON
def load_city_from_json(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


# Función para obtener una posición aleatoria de un nodo
def get_random_node_position(city_data):
    random_node = random.choice(city_data['nodos'])
    x = (random_node['coordenadas']['calle'] - 1) * distance_between_nodes + offset_x - taxi_image.get_width() / 10
    y = (random_node['coordenadas']['carrera'] - 1) * distance_between_nodes + offset_y - taxi_image.get_height() / 10
    return x, y

# Inicializa una lista vacía para las posiciones de los taxis
taxi_positions = []




def get_map_size_and_offset(city_data):
    max_x = max_y = 0
    min_x = min_y = float('inf')
    for nodo in city_data['nodos']:
        x = nodo['coordenadas']['calle']
        y = nodo['coordenadas']['carrera']
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        min_x = min(min_x, x)
        min_y = min(min_y, y)

    # Calcula el tamaño total del mapa
    map_width = (max_x - min_x + 1) * distance_between_nodes
    map_height = (max_y - min_y + 1) * distance_between_nodes

    # Calcula el desplazamiento para centrar el mapa
    offset_x = (screen_width - map_width) / 2
    offset_y = (screen_height - map_height) / 2

    return (offset_x, offset_y)

# Función auxiliar para dibujar flechas
def draw_arrow(screen, color, start_pos, end_pos, thickness=2, arrow_size=15, node_radius=20):
    # Calcula la dirección de la línea
    direction = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])

    # Ajusta el punto final para evitar la superposición con el círculo
    adjusted_end_pos = (
        end_pos[0] - math.cos(direction) * node_radius,
        end_pos[1] - math.sin(direction) * node_radius
    )



    # Dibuja la línea hasta el punto ajustado
    pygame.draw.line(screen, color, start_pos, adjusted_end_pos, thickness)

    # Calcula los puntos para la cabeza de la flecha
    p1 = (
        adjusted_end_pos[0] + arrow_size * math.cos(direction + math.pi / 6)*-1,
        adjusted_end_pos[1] + arrow_size * math.sin(direction + math.pi / 6)*-1
    )
    p2 = (
        adjusted_end_pos[0] + arrow_size * math.cos(direction - math.pi / 6)*-1,
        adjusted_end_pos[1] + arrow_size * math.sin(direction - math.pi / 6)*-1
    )

    # Dibuja la cabeza de la flecha
    pygame.draw.polygon(screen, color, [adjusted_end_pos, p1, p2])


# Verifica si la conexión es de doble sentido
def es_doble_sentido(nodo_id, adyacente_id, city_data):
    adyacente_nodo = next((n for n in city_data['nodos'] if n['id'] == adyacente_id), None)
    if adyacente_nodo and nodo_id in adyacente_nodo['adyacentes']:
        return True
    return False



def draw_button(screen, text, position, size):
    font = pygame.font.Font(None, 32)
    text_render = font.render(text, True, BLACK)
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, [0, 255, 0], button_rect)  # Color verde del botón
    screen.blit(text_render, (button_rect.x + 5, button_rect.y + 5))
    return button_rect



# Función para dibujar la ciudad
def draw_city(city_data, offset_x, offset_y):
    for nodo in city_data['nodos']:
        for adyacente_id in nodo['adyacentes']:
            adyacente_nodo = next((n for n in city_data['nodos'] if n['id'] == adyacente_id), None)
            if adyacente_nodo:
                start_pos = ((nodo['coordenadas']['calle'] - 1) * distance_between_nodes + node_radius + offset_x,
                             (nodo['coordenadas']['carrera'] - 1) * distance_between_nodes + node_radius + offset_y)
                end_pos = ((adyacente_nodo['coordenadas']['calle'] - 1) * distance_between_nodes + node_radius + offset_x,
                           (adyacente_nodo['coordenadas']['carrera'] - 1) * distance_between_nodes + node_radius + offset_y)
                if es_doble_sentido(nodo['id'], adyacente_id, city_data):  # Si la conexión es de doble sentido
                    pygame.draw.line(screen, GRAY, start_pos, end_pos, 2)
                else:  # Si la conexión es de un sentido
                    draw_arrow(screen, GRAY, start_pos, end_pos)

    # Luego dibujar los nodos
    for nodo in city_data['nodos']:
        position = ((nodo['coordenadas']['calle'] - 1) * distance_between_nodes + node_radius + offset_x,
                    (nodo['coordenadas']['carrera'] - 1) * distance_between_nodes + node_radius + offset_y)
        if nodo['esSemaforo']:
            pygame.draw.circle(screen, RED, position, node_radius)
        elif nodo['esPuntoInteres']:
            pygame.draw.circle(screen, GREEN, position, node_radius)
        else:
            pygame.draw.circle(screen, WHITE, position, node_radius)
        pygame.draw.circle(screen, BLACK, position, node_radius, 1)  # Borde del nodo


# Asegúrate de que el nombre del archivo coincida con el nombre de tu archivo JSON
city = load_city_from_json('city.json')
offset_x, offset_y = get_map_size_and_offset(city)


# Bucle principal de Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    draw_city(city,offset_x, offset_y)

    # Renderizar y mostrar el texto
    text_str = "Color Rojo: semaforos "  # Actualiza este texto según sea necesario
    text_str2 = "Color Verde: Punto interes "
    text_surface = font.render(text_str, True, RED)
    text_surface2 = font.render(text_str2, True, GREEN)

    screen.blit(text_surface, (10, 10))
    screen.blit(text_surface2, (10, 35))

    # Selecciona posiciones aleatorias para los taxis si la lista está vacía
    if not taxi_positions:
        taxi_positions = [get_random_node_position(city) for _ in range(5)]

    # Agregar las imágenes de los taxis
    for taxi_position in taxi_positions:
        screen.blit(taxi_image, taxi_position)

    button_rect = draw_button(screen, "Pedir Taxi", button_position, button_size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del mouse
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    # Aquí llamarías a la función para pedir un taxi
                    print("Se ha pedido un taxi")

    pygame.display.flip()

pygame.quit()
sys.exit()
