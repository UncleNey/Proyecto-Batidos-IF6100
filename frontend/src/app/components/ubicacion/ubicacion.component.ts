import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-ubicacion',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ubicacion.component.html',
  styleUrls: ['./ubicacion.component.scss']
})
export class UbicacionComponent {
  direccion = {
    calle: 'Calle Principal 123',
    ciudad: 'Tu Ciudad',
    telefono: '+1 (555) 123-4567',
    horario: 'Lunes a Domingo: 8:00 AM - 10:00 PM',
    email: 'contacto@batidos.com'
  };
}
