from collections import deque
from Nodo import  Nodo

import json

# 1. Abrir el archivo JSON
with open('city.json', 'r') as archivo:
    # 2. Leer su contenido
    contenido_json = archivo.read()

    # 3. Parsear el contenido JSON en un objeto de Python
    datos = json.loads(contenido_json)

# Ahora 'datos' contiene el contenido del archivo JSON como un diccionario de Python
nodos=datos['nodos']
#print(nodos)
listanodos=[]
for nodo in nodos:
    nod= Nodo(nodo['id'], nodo['esSemaforo'], nodo['adyacentes'], nodo['esPuntoInteres'],nodo['coordenadas'])
    listanodos.append(nod)
    #print(nodo['adyacentes'])
#print(listanodos[37].get_id())
def obtener_adyacentes(id):
    listaadyacencia=[]
    for i in listanodos[id-1].get_adyacentes():
        listaadyacencia.append(listanodos[i-1])
    #print(listaadyacencia)
    return listaadyacencia
obtener_adyacentes(5)


def busqueda_estrella(nodo_inicial, meta, heuristica):
    bandera = True
    camino = deque()
    cola = deque()
    acumulado_cola = deque()

    padres = deque()
    visitados = deque()
    acumulado_final = deque()

    visitados.append(nodo_inicial)
    cola.append(nodo_inicial)
    padres.append(nodo_inicial)
    acumulado_final.append(0)
    acumulado_cola.append(0)

    while cola and bandera:
        # Expandir vecinos
        # estado cola
        nodo_actual = cola.popleft()
        acumulado_cola.popleft()

        if nodo_actual.get_id() == meta.get_id():
            bandera = False
        else:
            # Verifique si tiene vecinos el nodo actual
            vecinos = obtener_adyacentes(nodo_actual.get_id())
            if vecinos is not None:
                # Recorra los vecinos del nodo actual
                for tupla in vecinos:
                    if tupla.get_id() != padres[visitados.index(nodo_actual)].get_id():
                        #if tupla.get_nodo_destino() not in visitados:
                        if tupla not in visitados:
                            visitados.append(tupla)
                            cola.append(tupla)
                            padres.append(nodo_actual)
                            acumulado = (tupla.get_peso() + acumulado_final[visitados.index(nodo_actual)] +
                                         1)
                                         #heuristica[tupla.get_id()])
                            acumulado_cola.append(acumulado)
                            acumulado_final.append(acumulado)
                        else:
                            if nodo_actual.get_id() != padres[visitados.index(tupla)].get_id():
                                visitados.append(tupla)
                                padres.append(nodo_actual)
                                cola.append(tupla)
                                acumulado = (tupla.get_peso() + acumulado_final[visitados.index(padres[-1])] +
                                             1)
                                             #heuristica[tupla.get_id()])
                                acumulado_cola.append(acumulado)
                                acumulado_final.append(acumulado)

                # Ordenar
                for i in range(len(acumulado_cola) - 1):
                    for j in range(i + 1, len(acumulado_cola)):
                        if acumulado_cola[i] > acumulado_cola[j]:
                            acumulado_cola[i], acumulado_cola[j] = acumulado_cola[j], acumulado_cola[i]
                            cola[i], cola[j] = cola[j], cola[i]

        # Comprobar ordenamiento, exitoso

    #camino = deque()
    nodo_aux = meta
    camino.appendleft(nodo_aux)
    while nodo_inicial not in camino:
        indice = visitados.index(nodo_aux)
        nodo_aux = padres[indice]
        camino.appendleft(nodo_aux)
        print(nodo_aux.get_id(), ", ", end="")

    return camino


camino=busqueda_estrella(listanodos[3],listanodos[10],1)
print("El camino obtenido es:")
for r in camino:
    print(r)





