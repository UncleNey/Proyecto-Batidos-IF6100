from models.ubicacion import Ubicacion

class UbicacionService:

    def __init__(self):
        # Atributo único (solo hay una ubicación principal)
        self.ubicacion = None

    def configurar_ubicacion(self, ubicacion):

        #Define la información de ubicación del emprendimiento.
        self.ubicacion = ubicacion

    def obtener_ubicacion(self):

        #Devuelve la ubicación actual registrada.
        return self.ubicacion.to_dict() if self.ubicacion else {}
