import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { Router } from '@angular/router';

interface Batido {
  id: number;
  nombre: string;
  descripcion: string;
  imagen?: string;
  precio?: number;
}

@Component({
  selector: 'app-batidos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './batidos.component.html',
  styleUrls: ['./batidos.component.scss']
})
export class BatidosComponent implements OnInit {
  batidos: Batido[] = [];
  batidosFiltrados: Batido[] = [];
  cargando: boolean = false;
  filtroActivo: string = 'todos';

  frutas = [
    { id: 'fresa', nombre: 'Fresa', emoji: '🍓' },
    { id: 'platano', nombre: 'Plátano', emoji: '🍌' },
    { id: 'manzana', nombre: 'Manzana', emoji: '🍎' },
    { id: 'naranja', nombre: 'Naranja', emoji: '🍊' },
    { id: 'uva', nombre: 'Uva', emoji: '🍇' }
  ];

  constructor(private apiService: ApiService, private router: Router) {}

  ngOnInit(): void {
    this.cargarBatidos();
  }

  cargarBatidos(): void {
    this.cargando = true;
    this.apiService.getBatidos().subscribe({
      next: (data) => {
        this.batidos = data;
        this.batidosFiltrados = data;
        this.cargando = false;
      },
      error: (error) => {
        console.error('Error:', error);
        this.cargando = false;
      }
    });
  }

  filtrarPorFruta(fruta: string): void {
    this.filtroActivo = fruta;
    if (fruta === 'todos') {
      this.batidosFiltrados = this.batidos;
    } else {
      this.batidosFiltrados = this.batidos.filter(b => 
        b.nombre.toLowerCase().includes(fruta.toLowerCase())
      );
    }
  }

  verDetalle(batido: Batido): void {
    this.router.navigate(['/batido', batido.id]);
  }
}
