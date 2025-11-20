# Proyecto Batidos IF6100

## Requisitos
- Python 3.8+
- SQL Server (con las tablas y datos de ejemplo)

## Instalación
1. Clona o descarga este repositorio.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura el archivo `.env` con los datos de tu SQL Server (host, usuario, contraseña, base de datos, etc).
4. Ejecuta el servidor FastAPI desde la raíz del proyecto:
   ```bash
   python -m uvicorn backend.main_api:app --reload --host 127.0.0.1 --port 8000
   ```

## Endpoints principales
- `/batidos` — Lista de batidos
- `/contacto` — Guardar mensaje de contacto
- `/categorias`, `/etiquetas`, `/reposteria`, `/utensilios` — Catálogos

Accede a la documentación interactiva en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
