from models.batido import Batido

class BatidoService:

    def __init__(self):

        #Lista local para almacenar los batidos
        self.batidos = []

    def agregar_batido(self, batido):

        #Agrega un nuevo batido a la lista.
        self.batidos.append(batido)

    def listar_batidos(self):

        #Devuelve la lista completa de batidos registrados.
        return [b.to_dict() for b in self.batidos]

    def buscar_batido(self, nombre):

        #Busca un batido por nombre.
        return next((b.to_dict() for b in self.batidos if b.nombre.lower() == nombre.lower()), None)
