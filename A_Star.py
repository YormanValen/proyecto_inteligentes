import heapq
import math

def heuristic(a, b):
    # Usa la distancia Manhattan como heurística
    return abs(a['coordenadas']['calle'] - b['coordenadas']['calle']) + abs(a['coordenadas']['carrera'] - b['coordenadas']['carrera'])

def get_node_by_id(node_id, city_data):
    for node in city_data['nodos']:
        if node['id'] == node_id:
            return node
    return None

def neighbors(current_node, city_data):
    neighbors = []
    for adj_id in current_node['adyacentes']:
        adj_node = get_node_by_id(adj_id, city_data)
        if adj_node:
            neighbors.append(adj_node)
    return neighbors

def a_star_search(start_id, goal_id, city_data):
    start_node = get_node_by_id(start_id, city_data)
    goal_node = get_node_by_id(goal_id, city_data)

    open_set = []
    heapq.heappush(open_set, (0, start_node))
    came_from = {}
    cost_so_far = {}
    came_from[start_node['id']] = None
    cost_so_far[start_node['id']] = 0

    while not len(open_set) == 0:
        current = heapq.heappop(open_set)[1]

        if current['id'] == goal_node['id']:
            break

        for next in neighbors(current, city_data):
            new_cost = cost_so_far[current['id']] + 1  # Aquí asumimos un costo constante para cada paso
            if next['id'] not in cost_so_far or new_cost < cost_so_far[next['id']]:
                cost_so_far[next['id']] = new_cost
                priority = new_cost + heuristic(goal_node, next)
                heapq.heappush(open_set, (priority, next))
                came_from[next['id']] = current['id']

    return came_from, cost_so_far
