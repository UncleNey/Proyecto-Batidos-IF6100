from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import hashlib
import json
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurar base de datos SQLite
DATABASE = 'batidos.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Tabla de usuarios
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        telefono TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tabla de productos
    c.execute('''CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        emoji TEXT,
        tipo TEXT,
        descripcion TEXT,
        imagen TEXT
    )''')
    
    # Tabla de batidos
    c.execute('''CREATE TABLE IF NOT EXISTS batidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        categoria TEXT NOT NULL,
        ingredientes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    
    # Insertar batidos iniciales
    c.execute('SELECT COUNT(*) FROM batidos')
    if c.fetchone()[0] == 0:
        batidos_iniciales = [
            ('Papaya-Naranja-Piña', 'Batido tropical natural', 3.50, 'agua', 'Papaya,Naranja,Piña'),
            ('Limón-Hierba buena', 'Refrescante y energético', 3.00, 'agua', 'Limón,Hierba buena'),
            ('Sandía-Limón', 'Hidratante y ácido', 3.00, 'agua', 'Sandía,Limón'),
            ('Sandía-Fresa', 'Dulce y refrescante', 3.50, 'agua', 'Sandía,Fresa'),
            ('Maracuyá-Piña', 'Exótico y delicioso', 3.50, 'agua', 'Maracuyá,Piña'),
            ('Banano-Papaya-Naranja', 'Suave y nutritivo', 3.50, 'agua', 'Banano,Papaya,Naranja'),
            ('Banano-Fresa-Proteína', 'Alto en proteína', 4.50, 'proteina', 'Banano,Fresa,Proteína'),
            ('Manzana-Avena-Banano-Proteína', 'Cremoso y saludable', 4.50, 'proteina', 'Manzana,Avena,Banano,Proteína'),
            ('Fresa-Banano-Avena-Proteína', 'Antioxidante', 4.50, 'proteina', 'Fresa,Banano,Avena,Proteína'),
            ('Fresa-Papaya-Proteína', 'Frutal y nutritivo', 4.50, 'proteina', 'Fresa,Papaya,Proteína'),
            ('Naranja-Fresa-Limón', 'Vitamínico y ácido', 3.50, 'agua', 'Naranja,Fresa,Limón'),
            ('Piña-Manzana', 'Tropical y crujiente', 3.00, 'agua', 'Piña,Manzana'),
        ]
        
        for batido in batidos_iniciales:
            c.execute('''INSERT INTO batidos (nombre, descripcion, precio, categoria, ingredientes)
                        VALUES (?, ?, ?, ?, ?)''', batido)
        conn.commit()
    
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============= RUTAS API =============

@app.route('/api/batidos', methods=['GET'])
def get_batidos():
    """Obtiene todos los batidos"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, nombre, descripcion, precio, categoria, ingredientes FROM batidos ORDER BY nombre')
        batidos = []
        for row in c.fetchall():
            batidos.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'precio': float(row[3]) if row[3] else 0,
                'categoria': row[4],
                'ingredientes': row[5].split(',') if row[5] else []
            })
        conn.close()
        return jsonify(batidos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batidos/mas-vendido', methods=['GET'])
def get_batido_mas_vendido():
    """Obtiene el batido más vendido (simulado)"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, nombre, descripcion FROM batidos ORDER BY id DESC LIMIT 1')
        row = c.fetchone()
        conn.close()
        
        if row:
            return jsonify({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2]
            })
        return jsonify({'error': 'No hay batidos'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reposteria', methods=['GET'])
def get_reposteria():
    """Obtiene todos los productos de repostería"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id, nombre, descripcion, emoji FROM productos WHERE tipo = 'reposteria'")
        reposteria = []
        for row in c.fetchall():
            reposteria.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'emoji': row[3]
            })
        conn.close()
        return jsonify(reposteria)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reposteria/mas-vendida', methods=['GET'])
def get_reposteria_mas_vendida():
    """Obtiene el producto de repostería más vendido"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT id, nombre, descripcion FROM productos WHERE tipo = 'reposteria' LIMIT 1")
        row = c.fetchone()
        conn.close()
        
        if row:
            return jsonify({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2]
            })
        return jsonify({'error': 'No hay repostería'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categorias', methods=['GET'])
def get_categorias():
    """Obtiene todas las categorías"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT DISTINCT categoria FROM batidos")
        categorias = [{'id': i+1, 'nombre': row[0]} for i, row in enumerate(c.fetchall())]
        conn.close()
        return jsonify(categorias)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Verifica que el servidor esté funcionando"""
    return jsonify({'status': 'ok', 'message': 'Backend funcionando correctamente'})

@app.route('/api/productos', methods=['GET'])
def get_productos():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM productos')
        productos = [dict(row) for row in c.fetchall()]
        conn.close()
        
        if not productos:
            # Retornar datos mock si la tabla está vacía
            return jsonify([
                {
                    'id': 1,
                    'nombre': 'Batido más vendido:',
                    'emoji': '🍓',
                    'tipo': 'Fresa',
                    'descripcion': 'Cremoso, natural y refrescante.',
                    'imagen': 'assets/batido-fresa.png'
                },
                {
                    'id': 2,
                    'nombre': 'Repostería más vendida:',
                    'emoji': '🍫',
                    'tipo': 'Chocolate',
                    'descripcion': 'Suave, húmedo y con ganache.',
                    'imagen': 'assets/reposteria-chocolate.png'
                }
            ])
        
        return jsonify(productos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/registro', methods=['POST'])
def registro():
    try:
        data = request.json
        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')
        telefono = data.get('telefono')
        
        if not all([nombre, email, password, telefono]):
            return jsonify({'error': 'Todos los campos son requeridos'}), 400
        
        # Hash de la contraseña
        password_hash = hash_password(password)
        
        conn = get_db()
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO usuarios (nombre, email, password, telefono)
                        VALUES (?, ?, ?, ?)''',
                     (nombre, email, password_hash, telefono))
            conn.commit()
            conn.close()
            
            return jsonify({
                'mensaje': 'Registro exitoso',
                'usuario': {
                    'nombre': nombre,
                    'email': email,
                    'telefono': telefono
                }
            }), 201
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'El email ya está registrado'}), 409
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email y contraseña requeridos'}), 400
        
        # Hash de la contraseña
        password_hash = hash_password(password)
        
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM usuarios WHERE email = ? AND password = ?',
                 (email, password_hash))
        usuario = c.fetchone()
        conn.close()
        
        if usuario:
            return jsonify({
                'mensaje': 'Login exitoso',
                'usuario': {
                    'id': usuario['id'],
                    'nombre': usuario['nombre'],
                    'email': usuario['email'],
                    'telefono': usuario['telefono']
                }
            }), 200
        else:
            return jsonify({'error': 'Email o contraseña incorrectos'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batidos/crear', methods=['POST'])
def crear_batido():
    try:
        data = request.json
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        precio = data.get('precio')
        categoria = data.get('categoria')  # 'agua' o 'proteina'
        ingredientes = data.get('ingredientes', [])
        
        if not all([nombre, precio, categoria]):
            return jsonify({'error': 'Campos requeridos: nombre, precio, categoria'}), 400
        
        conn = get_db()
        c = conn.cursor()
        
        c.execute('''INSERT INTO batidos (nombre, descripcion, precio, categoria, ingredientes)
                    VALUES (?, ?, ?, ?, ?)''',
                 (nombre, descripcion, precio, categoria, ','.join(ingredientes)))
        conn.commit()
        batido_id = c.lastrowid
        conn.close()
        
        return jsonify({
            'mensaje': 'Batido creado exitosamente',
            'id': batido_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batidos/por-categoria', methods=['GET'])
def get_batidos_por_categoria():
    try:
        categoria = request.args.get('categoria', 'agua')  # 'agua' o 'proteina'
        
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM batidos WHERE categoria = ? ORDER BY nombre', (categoria,))
        batidos = []
        for row in c.fetchall():
            batidos.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'precio': float(row[3]),
                'categoria': row[4],
                'ingredientes': row[5].split(',') if row[5] else []
            })
        conn.close()
        
        return jsonify(batidos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batidos/por-ingrediente/<ingrediente>', methods=['GET'])
def get_batidos_por_ingrediente(ingrediente):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM batidos WHERE ingredientes LIKE ?', (f'%{ingrediente}%',))
        batidos = []
        for row in c.fetchall():
            batidos.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'precio': float(row[3]),
                'categoria': row[4],
                'ingredientes': row[5].split(',') if row[5] else []
            })
        conn.close()
        
        return jsonify(batidos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
