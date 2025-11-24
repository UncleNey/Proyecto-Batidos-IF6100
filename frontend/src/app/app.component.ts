import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { ApiService } from './services/api.service';

interface Producto {
  id: number;
  nombre: string;
  descripcion: string;
  imagen?: string;
  precio?: number;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [ApiService]
})
export class AppComponent implements OnInit {
  seccionActiva: string = 'principal';
  batidoDestacado: Producto | null = null;
  reposteriDestacada: Producto | null = null;
  cargando: boolean = false;

  constructor(private apiService: ApiService, private router: Router) {}

  ngOnInit(): void {
    console.log('🚀 AppComponent iniciado');
    this.cargarBatidoDestacado();
    this.cargarReposteriDestacada();
  }

  cargarBatidoDestacado(): void {
    this.cargando = true;
    this.apiService.getBatidoMasVendido().subscribe({
      next: (data) => {
        console.log('✅ Batido cargado:', data);
        this.batidoDestacado = data;
        this.cargando = false;
      },
      error: (error) => {
        console.error('❌ Error:', error);
        this.cargando = false;
      }
    });
  }

  cargarReposteriDestacada(): void {
    this.cargando = true;
    this.apiService.getReposteriaMasVendida().subscribe({
      next: (data) => {
        console.log('✅ Repostería cargada:', data);
        this.reposteriDestacada = data;
        this.cargando = false;
      },
      error: (error) => {
        console.error('❌ Error:', error);
        this.cargando = false;
      }
    });
  }

  seleccionarSeccion(seccion: string): void {
    this.seccionActiva = seccion;
    this.router.navigate([seccion]);
  }

  verDetalle(producto: Producto): void {
    this.router.navigate(['/batido', producto.id]);
  }

  cerrarSesion(): void {
    console.log('🚪 Cerrar sesión');
  }
}
