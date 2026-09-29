import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private apiUrl =
    'http://127.0.0.1:8000/api/chat/';

  constructor(
    private http: HttpClient
  ) {}

  getConversations() {
    return this.http.get<any[]>(
      this.apiUrl
    );
  }

  getMessages(itemId: number) {
    return this.http.get<any[]>(
      `${this.apiUrl}${itemId}/`
    );
  }

  sendMessage(
    itemId: number,
    message: string
  ) {
    return this.http.post<any>(
      `${this.apiUrl}${itemId}/`,
      {
        message
      }
    );
  }
}