import heapq

# Definición de la clase Nodo
class Nodo:
    def __init__(self, id, es_semaforo, adyacentes, es_punto_interes):
        self.id = id
        self.es_semaforo = es_semaforo
        self.adyacentes = adyacentes
        self.es_punto_interes = es_punto_interes
        self.heuristica = 1  # Valor inicial de la heurística
        self.padre = None
        self.g = float('inf')
        self.f = float('inf')
def calcular_costo(nodo_actual, nodo_destino):
    # Aquí puedes implementar una función de costo específica según tus necesidades
    # Por ejemplo, puedes calcular la distancia entre los nodos o utilizar otras métricas
    return 1

def a_estrella(nodo_inicial, nodo_destino):
    # Inicializar las estructuras de datos
    abiertos = []
    cerrados = set()

    # Inicializar el nodo inicial
    nodo_inicial.g = 0
    nodo_inicial.f = nodo_inicial.g + nodo_inicial.heuristica

    # Agregar el nodo inicial a la lista de abiertos
    heapq.heappush(abiertos, (nodo_inicial.f, nodo_inicial))

    while abiertos:
        # Obtener el nodo con el costo estimado más bajo
        _, nodo_actual = heapq.heappop(abiertos)

        # Verificar si hemos llegado al nodo destino
        if nodo_actual == nodo_destino:
            # Se ha encontrado el camino, regresar el resultado
            camino = []
            while nodo_actual:
                camino.append(nodo_actual)
                nodo_actual = nodo_actual.padre
                print(nodo_actual)
            return list(reversed(camino))

        # Marcar el nodo actual como visitado
        cerrados.add(nodo_actual)
        print(nodo_actual)
        # Explorar los nodos adyacentes
        for nodo_adyacente in nodo_actual.adyacentes:
            if nodo_adyacente in cerrados:
                continue  # Ignorar nodos ya visitados

            # Calcular el nuevo costo desde el nodo inicial hasta el nodo adyacente
            costo = nodo_actual.g + calcular_costo(nodo_actual, nodo_adyacente)

            # Verificar si es la mejor ruta hasta ahora
            if nodo_adyacente not in abiertos or costo < nodo_adyacente.g:
                nodo_adyacente.padre = nodo_actual
                nodo_adyacente.g = costo
                nodo_adyacente.f = nodo_adyacente.g + nodo_adyacente.heuristica

                if nodo_adyacente not in abiertos:
                    # Agregar el nodo adyacente a la lista de abiertos
                    heapq.heappush(abiertos, (nodo_adyacente.f, nodo_adyacente.f))

    # No se ha encontrado un camino válido
    return None
# Creación de nodos
nodo_a = Nodo('A', False, [], False)
nodo_b = Nodo('B', False, [], False)
nodo_c = Nodo('C', False, [], False)
nodo_d = Nodo('D', False, [], False)
nodo_e = Nodo('E', False, [], False)
nodo_f = Nodo('F', False, [], True)

# Establecimiento de los nodos adyacentes
nodo_a.adyacentes = [nodo_b]
nodo_b.adyacentes = [nodo_a, nodo_c, nodo_d]
nodo_c.adyacentes = [nodo_b, nodo_e]
nodo_d.adyacentes = [nodo_b, nodo_e]
nodo_e.adyacentes = [nodo_c, nodo_d, nodo_f]
nodo_f.adyacentes = [nodo_e]

# Establecimiento de la heurística para el nodo objetivo
nodo_f.heuristica = 0

# Definición de la función de costo
def calcular_costo(nodo_actual, nodo_destino):
    return 1

# Aplicación del algoritmo A*
camino = a_estrella(nodo_a, nodo_f)

# Imprimir el resultado
if camino:
    print("Camino encontrado:")
    for nodo in camino:
        print(nodo.id)
else:
    print("No se encontró un camino válido.")