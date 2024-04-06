class ListaCerrados:
    def __init__(self):
        self.nodos = []

    def agregar(self, nodo):
        self.nodos.append(nodo)

    def contiene(self, nodo):
        return nodo in self.nodos