class Nodo:
    def __init__(self, id, es_semaforo, adyacentes, es_punto_interes, coordenadas):
        self.id = id
        self.es_semaforo = es_semaforo
        self.adyacentes = adyacentes
        self.es_punto_interes = es_punto_interes
        self.coordenadas = coordenadas
        self.heuristica=1
        self.peso=1

    def set_id(self, id):
        self.id = id

    def get_peso(self):
        return self.peso
    def get_id(self):
        return self.id
    def get_adyacentes(self):
        return self.adyacentes

    def get_x(self):
        return self.coordenadas.carrera

    def get_y(self):
        return self.coordenadas.calle

    def get_es_semaforo(self):
        return self.es_semaforo

    def conectar_nodos(self, nodo1, nodo2):
        pass

    def get_heuristica(self):
        return self.heuristica

    def set_heuristica(self, heuristica):
        self.heuristica = heuristica


    def __str__(self):
        return '{0}'.format(self.id)