from models.batido import Batido
from models.contacto import Contacto
from models.ubicacion import Ubicacion
from services.batido_service import BatidoService
from services.contacto_service import ContactoService
from services.ubicacion_service import UbicacionService

if __name__ == "__main__":
    # Inicialización de los servicios
    batido_service = BatidoService()
    contacto_service = ContactoService()
    ubicacion_service = UbicacionService()

    # Catálogo de batidos
    batido_service.agregar_batido(Batido(1, "Tropical Mix", ["Piña", "Mango", "Banano"], "tropical.jpg"))
    batido_service.agregar_batido(Batido(2, "Energético Verde", ["Espinaca", "Manzana", "Kiwi"], "verde.jpg"))

    # Información de contacto
    contacto_service.configurar_contacto(Contacto(
        telefono="+506 8827-5213",
        whatsapp="https://wa.me/88275213",
        horario="Lunes a Sábado: 3 p.m. - 9 p.m.",
        direccion_web="https://instagram.com/mixybatidos"
    ))

    # Ubicación del local
    ubicacion_service.configurar_ubicacion(Ubicacion(
        "Limón, Costa Rica"
    ))

    print("📋 LISTADO DE BATIDOS:")
    print(batido_service.listar_batidos())

    print("\n📞 INFORMACIÓN DE CONTACTO:")
    print(contacto_service.obtener_contacto())

    print("\n📍 UBICACIÓN Y REDES:")
    print(ubicacion_service.obtener_ubicacion())
