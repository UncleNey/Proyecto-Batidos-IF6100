\
from typing import List, Optional, Dict, Any
from db import query_all, execute

# CRUD de ejemplo contra SQL Server para la tabla "batido"

def listar_batidos() -> List[Dict[str, Any]]:
    sql = """
    SELECT b.id, b.nombre, b.slug, b.descripcion_corta, b.preparacion,
           b.tiempo_min, b.porciones, b.precio, b.imagen_url,
           b.categoria_id, b.fecha_publicacion
    FROM batido b
    ORDER BY b.id;
    """
    return query_all(sql)

def buscar_batido_por_nombre(nombre: str) -> Optional[Dict[str, Any]]:
    sql = """
    SELECT TOP 1 b.id, b.nombre, b.slug, b.descripcion_corta, b.preparacion,
           b.tiempo_min, b.porciones, b.precio, b.imagen_url,
           b.categoria_id, b.fecha_publicacion
    FROM batido b
    WHERE LOWER(b.nombre) = LOWER(?);
    """
    rows = query_all(sql, [nombre])
    return rows[0] if rows else None

def crear_batido(
    nombre: str,
    slug: str,
    descripcion_corta: Optional[str] = None,
    preparacion: Optional[str] = None,
    tiempo_min: Optional[int] = None,
    porciones: Optional[int] = None,
    precio: Optional[float] = None,
    imagen_url: Optional[str] = None,
    categoria_id: Optional[int] = None,
    fecha_publicacion: Optional[str] = None
) -> None:
    sql = """
    INSERT INTO batido
    (nombre, slug, descripcion_corta, preparacion, tiempo_min, porciones, precio,
     imagen_url, categoria_id, fecha_publicacion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    execute(sql, [
        nombre, slug, descripcion_corta, preparacion, tiempo_min, porciones, precio,
        imagen_url, categoria_id, fecha_publicacion
    ])

def eliminar_batido(id_batido: int) -> None:
    # Borrar relaciones primero para evitar FK violations (si fuera necesario)
    execute("DELETE FROM batido_ingrediente WHERE batido_id = ?", [id_batido])
    execute("DELETE FROM batido_etiqueta    WHERE batido_id = ?", [id_batido])
    execute("DELETE FROM batido_reposteria  WHERE batido_id = ?", [id_batido])
    execute("DELETE FROM batido_utensilio   WHERE batido_id = ?", [id_batido])
    execute("DELETE FROM nutricion          WHERE batido_id = ?", [id_batido])
    execute("DELETE FROM batido WHERE id = ?", [id_batido])
