import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

interface Producto {
  id: number;
  nombre: string;
  descripcion: string;
  precio?: number;
}

@Component({
  selector: 'app-reposteria',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './reposteria.component.html',
  styleUrls: ['./reposteria.component.scss']
})
export class RepostoriaComponent implements OnInit {
  reposteria: Producto[] = [];
  cargando: boolean = false;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.cargarReposteria();
  }

  cargarReposteria(): void {
    this.cargando = true;
    this.apiService.getReposteria().subscribe({
      next: (data) => {
        this.reposteria = data;
        this.cargando = false;
      },
      error: (error) => {
        console.error('Error:', error);
        this.cargando = false;
      }
    });
  }
}
