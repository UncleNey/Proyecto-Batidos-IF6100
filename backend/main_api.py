

from fastapi import FastAPI, HTTPException
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from .db import query_all, execute

app = FastAPI()


class Batido(BaseModel):
    id: int
    nombre: str
    ingredientes: List[str]
    imagen: str

class Contacto(BaseModel):
    nombre: str
    correo: str
    mensaje: str

class InfoContacto(BaseModel):
    telefono: str
    whatsapp: str
    horario: str
    direccion_web: Optional[str] = None

class Ubicacion(BaseModel):
    direccion: str
    google_maps: Optional[str] = None
    redes_sociales: Optional[Dict[str, str]] = None




# Endpoint para listar batidos con ingredientes
@app.get("/batidos", response_model=List[Batido])
def listar_batidos():
    sql = '''
        SELECT b.id, b.nombre, b.imagen_url AS imagen
        FROM batido b
    '''
    try:
        batidos = query_all(sql)
        for batido in batidos:
            # Obtener ingredientes para cada batido
            sql_ing = '''
                SELECT i.nombre
                FROM batido_ingrediente bi
                JOIN ingrediente i ON bi.ingrediente_id = i.id
                WHERE bi.batido_id = ?
            '''
            ingredientes = query_all(sql_ing, [batido["id"]])
            batido["ingredientes"] = [i["nombre"] for i in ingredientes]
        return batidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para guardar mensaje de contacto
@app.post("/contacto")
def guardar_contacto(contacto: Contacto):
    sql = "INSERT INTO contacto (nombre, correo, mensaje) VALUES (?, ?, ?)"
    try:
        execute(sql, [contacto.nombre, contacto.correo, contacto.mensaje])
        return {"mensaje": "Mensaje recibido correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener información de contacto (info del negocio)
@app.get("/contacto/info", response_model=InfoContacto)
def obtener_info_contacto():
    sql = "SELECT TOP 1 telefono, whatsapp, horario, direccion_web FROM contacto_info ORDER BY id DESC"
    try:
        row = query_all(sql)
        if not row:
            raise HTTPException(status_code=404, detail="No hay información de contacto disponible.")
        return row[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener ubicación y redes sociales
@app.get("/ubicacion", response_model=Ubicacion)
def obtener_ubicacion():
    sql = "SELECT TOP 1 direccion, google_maps, redes_sociales FROM ubicacion ORDER BY id DESC"
    try:
        row = query_all(sql)
        if not row:
            raise HTTPException(status_code=404, detail="No hay información de ubicación disponible.")
        # redes_sociales debe ser un dict, asumimos que está guardado como JSON en la base de datos
        import json
        if row[0]["redes_sociales"]:
            try:
                row[0]["redes_sociales"] = json.loads(row[0]["redes_sociales"])
            except Exception:
                row[0]["redes_sociales"] = {}
        return row[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para listar categorías
@app.get("/categorias")
def listar_categorias() -> list[Any]:
    sql = "SELECT id, nombre, slug FROM categoria"
    try:
        return query_all(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para listar etiquetas
@app.get("/etiquetas")
def listar_etiquetas() -> list[Any]:
    sql = "SELECT id, nombre, slug FROM etiqueta"
    try:
        return query_all(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para listar repostería
@app.get("/reposteria")
def listar_reposteria() -> list[Any]:
    sql = "SELECT id, nombre, slug, descripcion, precio FROM reposteria"
    try:
        return query_all(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para listar utensilios
@app.get("/utensilios")
def listar_utensilios() -> list[Any]:
    sql = "SELECT id, nombre, slug, descripcion FROM utensilio"
    try:
        return query_all(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
