class Tupla:
    def __init__(self, nodo_destino, peso):
        self.nodo_destino = nodo_destino
        self.peso = peso

    def get_nodo_destino(self):
        return self.nodo_destino

    def set_nodo_destino(self, nodo_destino):
        self.nodo_destino = nodo_destino

    def get_peso(self):
        return self.peso

    def set_peso(self, peso):
        self.peso = peso
