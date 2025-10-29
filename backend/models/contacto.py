class Contacto:

    def __init__(self, telefono, whatsapp, horario, direccion_web=None):

        #Constructor de la clase Contacto.
        self.telefono = telefono
        self.whatsapp = whatsapp
        self.horario = horario
        self.direccion_web = direccion_web

    def to_dict(self):

        #Convierte la información en un diccionario para facilitar su envío o lectura.
        return {
            "telefono": self.telefono,
            "correo": self.correo,
            "whatsapp": self.whatsapp,
            "horario": self.horario,
            "direccion_web": self.direccion_web
        }
