import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../services/api.service';

interface Batido {
  id: number;
  nombre: string;
  descripcion: string;
  imagen?: string;
  precio?: number;
  preparacion?: string;
  tiempo_min?: number;
  porciones?: number;
}

@Component({
  selector: 'app-detalle-batido',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './detalle-batido.component.html',
  styleUrls: ['./detalle-batido.component.scss']
})
export class DetalleBatidoComponent implements OnInit {
  batido: Batido | null = null;
  cargando: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const id = params['id'];
      this.cargarBatido(id);
    });
  }

  cargarBatido(id: number): void {
    this.cargando = true;
    this.apiService.getBatidos().subscribe({
      next: (batidos) => {
        this.batido = batidos.find((b: any) => b.id === id) || null;
        this.cargando = false;
      },
      error: (error) => {
        console.error('Error:', error);
        this.cargando = false;
      }
    });
  }

  volver(): void {
    this.router.navigate(['/batidos']);
  }

  agregarAlCarrito(): void {
    console.log('Agregado al carrito:', this.batido?.nombre);
  }
}
