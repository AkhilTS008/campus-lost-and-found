import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../services/auth';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [
    RouterLink
  ],
  templateUrl: './admin-dashboard.html',
  styleUrl: './admin-dashboard.css'
})
export class AdminDashboard {

  username = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {

    this.username =
      this.authService.getUsername() || 'Admin';

  }

  logout() {

    this.authService.logout();

    this.router.navigate([
      '/login'
    ]);

  }

}