class Batido:

    def __init__(self, id_batido, nombre, ingredientes, imagen):

        #Constructor de la clase Batido.
        self.id_batido = id_batido
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.imagen = imagen

    def to_dict(self):

        #Convierte la información del batido en un diccionario.
        return {
            "id": self.id_batido,
            "nombre": self.nombre,
            "ingredientes": self.ingredientes,
            "imagen": self.imagen
        }
