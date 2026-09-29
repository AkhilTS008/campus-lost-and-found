import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'https://campus-lost-found-backend-j3iz.onrender.com/api';

  constructor(
    private http: HttpClient
  ) {}

  register(userData: any) {

    return this.http.post(
      `${this.apiUrl}/register/`,
      userData
    );

  }

  login(userData: any) {

    return this.http.post(
      `${this.apiUrl}/login/`,
      userData
    );

  }


  // Save token

  saveToken(token: string) {

    localStorage.setItem(
      'token',
      token
    );

  }


  // Get token

  getToken() {

    return localStorage.getItem(
      'token'
    );

  }


  // Save username

  saveUsername(username: string) {

    localStorage.setItem(
      'username',
      username
    );

  }


  // Get username

  getUsername() {

    return localStorage.getItem(
      'username'
    );

  }


  // Logout

logout() {

  localStorage.removeItem('token');

  localStorage.removeItem('username');

  localStorage.removeItem('is_staff');

}


  // Check login

  isLoggedIn() {

    return !!this.getToken();

  }


  saveAdminStatus(isStaff: boolean) {

  localStorage.setItem(
    'is_staff',
    String(isStaff)
  );

}

isAdmin() {

  return localStorage.getItem(
    'is_staff'
  ) === 'true';

}




}