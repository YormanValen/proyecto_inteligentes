class Grafo:
    def __init__(self):
        self.sitio={}
    def anadir_sitio(self, id, nodo):
        self.sitio[id]=nodo
    def obtener_adyacentes(self, id):

        return self.sitio.get(id)['adyacentes']

