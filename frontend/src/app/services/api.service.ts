import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  getBatidos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/batidos`);
  }

  getBatidoMasVendido(): Observable<any> {
    return this.http.get(`${this.apiUrl}/batidos/mas-vendido`);
  }

  getReposteria(): Observable<any> {
    return this.http.get(`${this.apiUrl}/reposteria`);
  }

  getReposteriaMasVendida(): Observable<any> {
    return this.http.get(`${this.apiUrl}/reposteria/mas-vendida`);
  }

  getCategorias(): Observable<any> {
    return this.http.get(`${this.apiUrl}/categorias`);
  }
}
