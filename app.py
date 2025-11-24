from flask import Flask, jsonify, request
from flask_cors import CORS
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de conexión a BD
DATABASE_CONFIG = {
    'Driver': '{ODBC Driver 17 for SQL Server}',
    'Server': 'localhost',
    'Database': 'batidos',
    'Trusted_Connection': 'yes'
}

def get_db_connection():
    try:
        conn_str = ';'.join([f'{k}={v}' for k, v in DATABASE_CONFIG.items()])
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        print(f"Error de conexión: {e}")
        return None

# ============= RUTAS API =============

@app.route('/api/batidos', methods=['GET'])
def get_batidos():
    """Obtiene todos los batidos"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'No hay conexión a la BD'}), 500
        
        cursor = conn.cursor()
        cursor.execute('SELECT TOP 10 id, nombre, descripcion_corta, imagen_url, precio FROM batido ORDER BY fecha_publicacion DESC')
        batidos = []
        for row in cursor.fetchall():
            batidos.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'imagen': row[3],
                'precio': float(row[4]) if row[4] else 0
            })
        conn.close()
        return jsonify(batidos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batidos/mas-vendido', methods=['GET'])
def get_batido_mas_vendido():
    """Obtiene el batido más vendido (simulado)"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'No hay conexión a la BD'}), 500
        
        cursor = conn.cursor()
        cursor.execute('SELECT TOP 1 id, nombre, descripcion_corta, imagen_url FROM batido ORDER BY id DESC')
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return jsonify({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'imagen': row[3]
            })
        return jsonify({'error': 'No hay batidos'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reposteria', methods=['GET'])
def get_reposteria():
    """Obtiene todos los productos de repostería"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'No hay conexión a la BD'}), 500
        
        cursor = conn.cursor()
        cursor.execute('SELECT TOP 10 id, nombre, descripcion, precio FROM reposteria')
        reposteria = []
        for row in cursor.fetchall():
            reposteria.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'precio': float(row[3]) if row[3] else 0
            })
        conn.close()
        return jsonify(reposteria)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reposteria/mas-vendida', methods=['GET'])
def get_reposteria_mas_vendida():
    """Obtiene el producto de repostería más vendido"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'No hay conexión a la BD'}), 500
        
        cursor = conn.cursor()
        cursor.execute('SELECT TOP 1 id, nombre, descripcion, precio FROM reposteria')
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return jsonify({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'precio': float(row[3]) if row[3] else 0
            })
        return jsonify({'error': 'No hay repostería'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categorias', methods=['GET'])
def get_categorias():
    """Obtiene todas las categorías"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'No hay conexión a la BD'}), 500
        
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre FROM categoria')
        categorias = [{'id': row[0], 'nombre': row[1]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(categorias)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Verifica que el servidor esté funcionando"""
    return jsonify({'status': 'ok', 'message': 'Backend funcionando correctamente'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
