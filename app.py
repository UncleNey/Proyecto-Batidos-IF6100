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
    
    # Tabla de reposteria
    c.execute('''CREATE TABLE IF NOT EXISTS reposteria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        ingrediente TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    
    # Insertar batidos iniciales SOLO si la tabla está vacía
    try:
        c.execute('SELECT COUNT(*) FROM batidos')
        count = c.fetchone()[0]
        
        if count == 0:
            batidos_iniciales = [
                ('Papaya-Naranja-Piña', 'Batido tropical natural', 2100, 'agua', 'Papaya,Naranja,Piña'),
                ('Limón-Hierba buena', 'Refrescante y energético', 1800, 'agua', 'Limón,Hierba buena'),
                ('Sandía-Limón', 'Hidratante y ácido', 1800, 'agua', 'Sandía,Limón'),
                ('Sandía-Fresa', 'Dulce y refrescante', 2100, 'agua', 'Sandía,Fresa'),
                ('Maracuyá-Piña', 'Exótico y delicioso', 2100, 'agua', 'Maracuyá,Piña'),
                ('Banano-Papaya-Naranja', 'Suave y nutritivo', 2100, 'agua', 'Banano,Papaya,Naranja'),
                ('Banano-Fresa-Proteína', 'Alto en proteína', 2700, 'proteina', 'Banano,Fresa,Proteína'),
                ('Manzana-Avena-Banano-Proteína', 'Cremoso y saludable', 2700, 'proteina', 'Manzana,Avena,Banano,Proteína'),
                ('Fresa-Banano-Avena-Proteína', 'Batido nutritivo con textura cremosa y frutas frescas', 2700, 'proteina', 'Fresa,Banano,Avena,Proteína'),
                ('Fresa-Papaya-Proteína', 'Frutal y nutritivo', 2700, 'proteina', 'Fresa,Papaya,Proteína'),
                ('Naranja-Fresa-Limón', 'Vitamínico y ácido', 2100, 'agua', 'Naranja,Fresa,Limón'),
                ('Piña-Manzana', 'Tropical y crujiente', 1800, 'agua', 'Piña,Manzana'),
            ]
            
            for batido in batidos_iniciales:
                c.execute('''INSERT INTO batidos (nombre, descripcion, precio, categoria, ingredientes)
                            VALUES (?, ?, ?, ?, ?)''', batido)
            conn.commit()
            print("✅ Batidos iniciales insertados correctamente")
    except Exception as e:
        print(f"❌ Error al insertar batidos: {e}")
    
    # Insertar repostería inicial
    try:
        c.execute('SELECT COUNT(*) FROM reposteria')
        count = c.fetchone()[0]
        
        if count == 0:
            reposteria_inicial = [
                ('Queque de Chocolate', 'Delicioso queque de chocolate', 1000, 'Chocolate'),
                ('Galletas de Chocolate', 'Galletas crujientes de chocolate', 600, 'Chocolate'),
                ('Brownie de Chocolate', 'Brownie intenso y delicioso', 1200, 'Chocolate'),
                ('Cupcakes de Vainilla', 'Cupcakes esponjosos de vainilla', 900, 'Vainilla'),
                ('Queque clásico de Vainilla', 'Queque tradicional de vainilla', 700, 'Vainilla'),
                ('Galletas de Vainilla', 'Galletas suaves de vainilla', 500, 'Vainilla'),
                ('Cheesecake de Fresa', 'Cheesecake cremoso con fresa', 1500, 'Fresa'),
                ('Cupcake de Fresa', 'Cupcake decorado con fresa', 1000, 'Fresa'),
                ('Galletas de Fresa', 'Galletas con sabor a fresa', 600, 'Fresa'),
                ('Galletas con Nueces', 'Galletas crujientes con nueces', 700, 'Nuez'),
                ('Queque de Banano con Nueces', 'Queque suave con nueces', 900, 'Nuez'),
                ('Barrita energética de avena y nuez', 'Barrita nutritiva y deliciosa', 800, 'Nuez'),
                ('Queque de Limón', 'Queque refrescante de limón', 700, 'Limón'),
                ('Galletas de Limón', 'Galletas cítricas y crujientes', 500, 'Limón'),
                ('Cheesecake de Limón', 'Cheesecake ácido y delicioso', 1200, 'Limón'),
                ('Cocadas', 'Cocadas tradicionales', 600, 'Coco'),
                ('Galletas de Coco', 'Galletas tropicales de coco', 500, 'Coco'),
                ('Queque de Coco', 'Queque húmedo de coco', 900, 'Coco'),
                ('Barritas de avena con miel', 'Barritas naturales con miel', 800, 'Miel'),
                ('Galletas de avena y miel', 'Galletas saludables con miel', 600, 'Miel'),
                ('Pan dulce artesanal con miel', 'Pan artesanal endulzado con miel', 700, 'Miel'),
                ('Queque de Café', 'Queque aromático de café', 1000, 'Café'),
                ('Galletas sabor café', 'Galletas con aroma de café', 600, 'Café'),
                ('Tiramisú', 'Tiramisú italiano tradicional', 1500, 'Café'),
                ('Brownie clásico', 'Brownie clásico de chocolate', 1200, 'Brownie'),
                ('Brownie con nuez', 'Brownie crujiente con nueces', 1300, 'Brownie'),
                ('Brownie con chispas de chocolate', 'Brownie con chispas', 1400, 'Brownie'),
            ]
            
            for item in reposteria_inicial:
                c.execute('''INSERT INTO reposteria (nombre, descripcion, precio, ingrediente)
                            VALUES (?, ?, ?, ?)''', item)
            conn.commit()
            print("✅ Repostería inicial insertada correctamente")
    except Exception as e:
        print(f"❌ Error al insertar repostería: {e}")
    
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============= RUTAS API =============

@app.route('/')
def home():
    return {'message': 'Backend funcionando correctamente'}

@app.route('/api/productos', methods=['GET'])
def get_productos():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM productos')
        productos = [dict(row) for row in c.fetchall()]
        conn.close()
        
        if not productos:
            # Obtener el batido más vendido desde la tabla batidos
            conn = get_db()
            c = conn.cursor()
            c.execute('SELECT * FROM batidos WHERE nombre = ?', ('Fresa-Banano-Avena-Proteína',))
            batido_mas_vendido = c.fetchone()
            c.execute('SELECT * FROM reposteria WHERE nombre = ?', ('Queque de Banano con Nueces',))
            reposteria_mas_vendida = c.fetchone()
            conn.close()
            
            if batido_mas_vendido and reposteria_mas_vendida:
                return jsonify([
                    {
                        'id': 1,
                        'nombre': 'Batido más vendido: Fresa-Banano-Avena-Proteína',
                        'emoji': '🥤',
                        'tipo': batido_mas_vendido['nombre'],
                        'descripcion': 'Batido nutritivo y de textura cremosa elaborado a base de frutas frescas y avena, complementado con proteína en polvo para aumentar su valor nutricional',
                        'imagen': 'assets/batido-fresa.png',
                        'precio': '₡2.700'
                    },
                    {
                        'id': 2,
                        'nombre': 'Repostería más vendida: Queque de Banano con Nueces',
                        'emoji': '🍰',
                        'tipo': reposteria_mas_vendida['nombre'],
                        'descripcion': reposteria_mas_vendida['descripcion'],
                        'imagen': 'assets/reposteria-chocolate.png',
                        'precio': '₡900'
                    }
                ])
            else:
                return jsonify([
                    {
                        'id': 1,
                        'nombre': 'Batido más vendido: Fresa-Banano-Avena-Proteína',
                        'emoji': '🥤',
                        'tipo': 'Fresa-Banano-Avena-Proteína',
                        'descripcion': 'Batido nutritivo y de textura cremosa elaborado a base de frutas frescas y avena, complementado con proteína en polvo para aumentar su valor nutricional',
                        'imagen': 'assets/batido-fresa.png',
                        'precio': '₡2.700'
                    },
                    {
                        'id': 2,
                        'nombre': 'Repostería más vendida: Queque de Banano con Nueces',
                        'emoji': '🍰',
                        'tipo': 'Queque de Banano con Nueces',
                        'descripcion': 'Queque suave con nueces',
                        'imagen': 'assets/reposteria-chocolate.png',
                        'precio': '₡900'
                    }
                ])
        
        return jsonify(productos)
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
        print(f"Error en get_batidos_por_ingrediente: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/registro', methods=['POST'])
def registro():
    try:
        data = request.json
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '').strip()
        telefono = data.get('telefono', '').strip()
        
        # Validar campos
        if not all([nombre, email, password, telefono]):
            return jsonify({'error': 'Todos los campos son requeridos'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'La contraseña debe tener al menos 6 caracteres'}), 400
        
        if '@' not in email:
            return jsonify({'error': 'Email inválido'}), 400
        
        password_hash = hash_password(password)
        
        conn = get_db()
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO usuarios (nombre, email, password, telefono)
                        VALUES (?, ?, ?, ?)''',
                     (nombre, email, password_hash, telefono))
            conn.commit()
            usuario_id = c.lastrowid
            conn.close()
            
            print(f"✅ Usuario registrado: {email} (ID: {usuario_id})")
            
            return jsonify({
                'mensaje': 'Registro exitoso',
                'usuario': {
                    'id': usuario_id,
                    'nombre': nombre,
                    'email': email,
                    'telefono': telefono
                }
            }), 201
        except sqlite3.IntegrityError as e:
            conn.close()
            print(f"❌ Error de integridad: {e}")
            return jsonify({'error': 'El email ya está registrado'}), 409
            
    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    """Endpoint para verificar todos los usuarios registrados (solo para debugging)"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, nombre, email, telefono, created_at FROM usuarios')
        usuarios = []
        for row in c.fetchall():
            usuarios.append({
                'id': row[0],
                'nombre': row[1],
                'email': row[2],
                'telefono': row[3],
                'created_at': row[4]
            })
        conn.close()
        return jsonify(usuarios)
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

@app.route('/api/reposteria/por-ingrediente/<ingrediente>', methods=['GET'])
def get_reposteria_por_ingrediente(ingrediente):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM reposteria WHERE ingrediente = ?', (ingrediente,))
        reposteria = []
        for row in c.fetchall():
            reposteria.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'precio': float(row[3]),
                'ingrediente': row[4]
            })
        conn.close()
        
        return jsonify(reposteria)
    except Exception as e:
        print(f"Error en get_reposteria_por_ingrediente: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
