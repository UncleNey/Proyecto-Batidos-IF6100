from models.contacto import Contacto

class ContactoService:

    def __init__(self):
        self.contacto = None

    def configurar_contacto(self, contacto):

        #Define o actualiza la información de contacto.
        self.contacto = contacto

    def obtener_contacto(self):

        #Devuelve la información de contacto configurada.
        return self.contacto.to_dict() if self.contacto else {}
