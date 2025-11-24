import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { BatidosComponent } from './components/batidos/batidos.component';
import { RepostoriaComponent } from './components/reposteria/reposteria.component';
import { UbicacionComponent } from './components/ubicacion/ubicacion.component';
import { DetalleBatidoComponent } from './components/detalle-batido/detalle-batido.component';

export const routes: Routes = [
  { path: '', component: AppComponent },
  { path: 'batidos', component: BatidosComponent },
  { path: 'reposteria', component: RepostoriaComponent },
  { path: 'ubicacion', component: UbicacionComponent },
  { path: 'batido/:id', component: DetalleBatidoComponent }
];
