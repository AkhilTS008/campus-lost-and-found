import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ItemService {

  private apiUrl = 'https://campus-lost-found-backend-j3iz.onrender.com/api/items/';

  constructor(private http: HttpClient) {}

  // Get all items
  getItems(filters: any = {}) {

    let params = new HttpParams();

    if (filters.search) {
      params = params.set('search', filters.search);
    }

    if (filters.item_type) {
      params = params.set('item_type', filters.item_type);
    }

    if (filters.category) {
      params = params.set('category', filters.category);
    }

    if (filters.location) {
      params = params.set('location', filters.location);
    }

    return this.http.get<any[]>(
      this.apiUrl,
      { params }
    );
  }

  // Get one item
  getItem(id: number) {

    return this.http.get<any>(
      `${this.apiUrl}${id}/`
    );
  }

  // Create lost/found item
  createItem(formData: FormData) {

    return this.http.post<any>(
      this.apiUrl,
      formData
    );
  }

  // Update item
  updateItem(id: number, formData: FormData) {

    return this.http.put<any>(
      `${this.apiUrl}${id}/`,
      formData
    );
  }

  // Delete item
  deleteItem(id: number) {

    return this.http.delete(
      `${this.apiUrl}${id}/`
    );
  }

  getMyReports() {

  return this.http.get<any[]>(
    'https://campus-lost-found-backend-j3iz.onrender.com/api/my-reports/'
  );

}
}