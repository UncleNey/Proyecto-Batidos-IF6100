import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

interface Producto {
  id: number;
  nombre: string;
  emoji: string;
  tipo: string;
  descripcion: string;
  imagen: string;
}

interface Fruta {
  id: number;
  nombre: string;
  emoji: string;
  descripcion: string;
}

interface Postre {
  id: number;
  nombre: string;
  emoji: string;
  descripcion: string;
}

interface ProductoDetalle {
  id: number;
  nombre: string;
  precio: number;
  imagen: string;
  descripcion: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, HttpClientModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  seccionActiva = 'principal';
  productos: Producto[] = [];
  cargando = false;
  mostrarRegistro = false;
  usuarioLogueado = false;
  usuarioActual: any = null;
  productoDetalleActual: any = null;

  loginForm = { email: '', password: '' };
  registroForm = { nombre: '', email: '', password: '', telefono: '' };

  frutas: Fruta[] = [
    { id: 1, nombre: 'Papaya', emoji: '🧡', descripcion: 'Batido de papaya fresco y tropical' },
    { id: 2, nombre: 'Naranja', emoji: '🍊', descripcion: 'Batido de naranja natural y vitamínico' },
    { id: 3, nombre: 'Piña', emoji: '🍍', descripcion: 'Batido de piña tropical y refrescante' },
    { id: 4, nombre: 'Limón', emoji: '🍋', descripcion: 'Batido de limón ácido y energético' },
    { id: 5, nombre: 'Sandía', emoji: '🍉', descripcion: 'Batido de sandía dulce y hidratante' },
    { id: 6, nombre: 'Fresa', emoji: '🍓', descripcion: 'Batido de fresa cremoso y delicioso' },
    { id: 7, nombre: 'Maracuyá', emoji: '🟣', descripcion: 'Batido de maracuyá exótico y sabroso' },
    { id: 8, nombre: 'Banano', emoji: '🍌', descripcion: 'Batido de banano suave y nutritivo' },
    { id: 9, nombre: 'Manzana', emoji: '🍎', descripcion: 'Batido de manzana crujiente y fresco' }
  ];

  frutaSeleccionada: Fruta = this.frutas[0];

  postres: Postre[] = [
    { id: 1, nombre: 'Chocolate', emoji: '🍫', descripcion: 'Torta de chocolate suave y húmeda' },
    { id: 2, nombre: 'Vainilla', emoji: '🧁', descripcion: 'Cupcake de vainilla clásico' },
    { id: 3, nombre: 'Fresa', emoji: '🍓', descripcion: 'Cheesecake de fresa delicioso' },
    { id: 4, nombre: 'Nuez', emoji: '🌰', descripcion: 'Torta de nuez crujiente' },
    { id: 5, nombre: 'Limón', emoji: '🍋', descripcion: 'Pie de limón refrescante' },
    { id: 6, nombre: 'Coco', emoji: '🥥', descripcion: 'Bizcocho de coco tropical' },
    { id: 7, nombre: 'Miel', emoji: '🍯', descripcion: 'Pastel de miel y almendra' },
    { id: 8, nombre: 'Café', emoji: '☕', descripcion: 'Tiramisú de café italiano' },
    { id: 9, nombre: 'Brownie', emoji: '🟫', descripcion: 'Brownie de chocolate intenso' }
  ];

  postreSeleccionado: Postre = this.postres[0];

  ingredienteSeleccionado: any = null;
  productosIngrediente: ProductoDetalle[] = [];
  tipoProducto: 'batidos' | 'reposteria' | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.cargarProductos();
  }

  cargarProductos() {
    this.cargando = true;
    this.http.get('http://127.0.0.1:5000/api/productos').subscribe(
      (data: any) => {
        this.productos = data;
        this.cargando = false;
      },
      (error: any) => {
        console.error('Error al cargar productos:', error);
        this.cargando = false;
        this.productos = [
          {
            id: 1,
            nombre: 'Batido más vendido:',
            emoji: '🥤',
            tipo: 'Fresa-Banano-Avena-Proteína',
            descripcion: 'Nutritivo y cremoso',
            imagen: 'assets/batido-fresa.png'
          },
          {
            id: 2,
            nombre: 'Repostería más vendida:',
            emoji: '🍰',
            tipo: 'Chocolate',
            descripcion: 'Suave, húmedo y con ganache.',
            imagen: 'assets/reposteria-chocolate.png'
          }
        ];
      }
    );
  }

  seleccionarSeccion(seccion: string) {
    this.seccionActiva = seccion;
    this.mostrarRegistro = false;
  }

  cerrarSesion() {
    this.usuarioLogueado = false;
    this.usuarioActual = null;
    this.seleccionarSeccion('login');
  }

  toggleRegistro() {
    this.mostrarRegistro = !this.mostrarRegistro;
  }

  iniciarSesion() {
    if (!this.loginForm.email || !this.loginForm.password) {
      alert('Por favor completa todos los campos');
      return;
    }

    this.http.post('http://127.0.0.1:5000/api/login', this.loginForm).subscribe(
      (response: any) => {
        console.log('Login exitoso:', response);
        this.usuarioLogueado = true;
        this.usuarioActual = response.usuario;
        alert(`✅ ¡Bienvenido ${response.usuario.nombre}!`);
        this.loginForm = { email: '', password: '' };
        this.seleccionarSeccion('principal');
      },
      (error: any) => {
        console.error('Error al iniciar sesión:', error);
        alert('❌ Email o contraseña incorrectos');
      }
    );
  }

  registrarse() {
    if (!this.registroForm.nombre || !this.registroForm.email || !this.registroForm.password || !this.registroForm.telefono) {
      alert('Por favor completa todos los campos');
      return;
    }

    if (this.registroForm.password.length < 6) {
      alert('La contraseña debe tener al menos 6 caracteres');
      return;
    }

    this.http.post('http://127.0.0.1:5000/api/registro', this.registroForm).subscribe(
      (response: any) => {
        console.log('Registro exitoso:', response);
        alert('✅ ¡Cuenta creada exitosamente! Ahora inicia sesión con tus credenciales');
        this.registroForm = { nombre: '', email: '', password: '', telefono: '' };
        this.mostrarRegistro = false;
      },
      (error: any) => {
        console.error('Error al registrarse:', error);
        const mensajeError = error.error?.error || 'Error al crear la cuenta';
        alert(`❌ ${mensajeError}`);
      }
    );
  }

  seleccionarFruta(fruta: Fruta) {
    this.frutaSeleccionada = fruta;
    this.cargarProductosPorFruta(fruta);
  }

  seleccionarPostre(postre: Postre) {
    this.postreSeleccionado = postre;
    this.cargarProductosPorPostre(postre);
  }

  cargarProductosPorFruta(fruta: Fruta) {
    this.ingredienteSeleccionado = fruta;
    this.tipoProducto = 'batidos';
    this.seccionActiva = 'detalle-batidos';

    this.http.get(`http://127.0.0.1:5000/api/batidos/por-ingrediente/${fruta.nombre}`).subscribe(
      (data: any) => {
        console.log('Batidos cargados:', data);
        if (data && data.length > 0) {
          this.productosIngrediente = data.map((batido: any) => ({
            id: batido.id,
            nombre: batido.nombre,
            precio: batido.precio,
            imagen: '🥤',
            descripcion: batido.descripcion
          }));
        } else {
          this.productosIngrediente = [];
        }
      },
      (error: any) => {
        console.error('Error al cargar batidos:', error);
        this.productosIngrediente = [];
      }
    );
  }

  cargarProductosPorPostre(postre: Postre) {
    this.ingredienteSeleccionado = postre;
    this.tipoProducto = 'reposteria';
    this.seccionActiva = 'detalle-reposteria';

    this.http.get(`http://127.0.0.1:5000/api/reposteria/por-ingrediente/${postre.nombre}`).subscribe(
      (data: any) => {
        console.log('Repostería cargada:', data);
        if (data && data.length > 0) {
          this.productosIngrediente = data.map((item: any) => ({
            id: item.id,
            nombre: item.nombre,
            precio: item.precio,
            imagen: '🍰',
            descripcion: item.descripcion
          }));
        } else {
          this.productosIngrediente = [];
        }
      },
      (error: any) => {
        console.error('Error al cargar repostería:', error);
        this.productosIngrediente = [];
      }
    );
  }

  volverAProductos() {
    if (this.tipoProducto === 'batidos') {
      this.seccionActiva = 'batidos';
    } else if (this.tipoProducto === 'reposteria') {
      this.seccionActiva = 'reposteria';
    } else {
      this.seccionActiva = 'principal';
    }
    this.ingredienteSeleccionado = null;
    this.productosIngrediente = [];
  }

  verDetalle(id: number) {
    const producto = this.productos.find((p: any) => p.id === id);
    if (producto) {
      let detalleCompleto: string = '';
      let ingredientes: string[] = [];
      let precio: number = 0;

      if (id === 1) {
        // Batido más vendido
        detalleCompleto = 'Batido nutritivo y de textura cremosa elaborado a base de frutas frescas y avena, complementado con proteína en polvo para aumentar su valor nutricional';
        ingredientes = ['Banano', 'Fresa', 'Avena', 'Proteína'];
        precio = 4.50;
      } else if (id === 2) {
        // Repostería más vendida
        detalleCompleto = 'Se prepara utilizando bananos maduros, y se enriquece con nueces picadas, que aportan un toque crocante y un sabor tostado que complementa perfectamente la suavidad del banano.';
        ingredientes = ['Banano', 'Nueces', 'Harina', 'Huevos', 'Azúcar'];
        precio = 900;
      }

      this.productoDetalleActual = {
        ...producto,
        detalleCompleto: detalleCompleto,
        precio: precio,
        ingredientes: ingredientes
      };
      this.seccionActiva = 'detalle-producto-principal';
    }
  }

  volverAProductosPrincipal() {
    this.seccionActiva = 'principal';
    this.productoDetalleActual = null;
  }
}
