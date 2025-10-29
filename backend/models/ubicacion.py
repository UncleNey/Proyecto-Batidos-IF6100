class Ubicacion:

    def __init__(self, direccion, google_maps_url, redes_sociales):

        #Constructor de la clase Ubicacion.
        self.direccion = direccion
        self.google_maps_url = google_maps_url
        self.redes_sociales = redes_sociales  # Ejemplo: {"Instagram": "...", "Facebook": "..."}

    def to_dict(self):

        #Devuelve los datos de ubicación en formato de diccionario.
        return {
            "direccion": self.direccion,
            "google_maps": self.google_maps_url,
            "redes_sociales": self.redes_sociales
        }
