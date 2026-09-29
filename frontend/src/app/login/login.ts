import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

import { AuthService } from '../services/auth';
import { ToastService } from '../services/toast';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink
  ],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {

  username = '';
  password = '';
  showPassword = false;
  message = '';

  constructor(
    private authService: AuthService,
    private router: Router,
    private toastService: ToastService

  ) {}

  login() {

    const userData = {
      username: this.username,
      password: this.password
    };

    this.authService.login(userData).subscribe({

      next: (response: any) => {

        // Save login token
        this.authService.saveToken(
          response.token
        );

        // Save username
        this.authService.saveUsername(
          response.username
        );

        this.authService.saveAdminStatus(
          response.is_staff
        );

        this.toastService.show(
          'Login successful!',
          'success'
        );

        if (response.is_staff) {

          this.router.navigate([
            '/admin-dashboard'
          ]);

        } 
        else {
          this.router.navigate([
            '/dashboard'
          ]);
        }

      },

      error: (error) => {

        this.toastService.show(
          error.error?.message ||
          'Login failed. Check username and password',
          'error'
        );

      }

    });

  }

}