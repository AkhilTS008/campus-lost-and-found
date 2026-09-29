import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';

import { ItemService } from '../services/item';
import { AuthService } from '../services/auth';

@Component({
  selector: 'app-admin-items',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink
  ],
  templateUrl: './admin-items.html',
  styleUrl: './admin-items.css'
})
export class AdminItems implements OnInit {

  items: any[] = [];
  message = '';

  constructor(
    private itemService: ItemService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadItems();
  }

  loadItems() {

    this.itemService.getItems().subscribe({

      next: (response) => {
        this.items = response;
      },

      error: (error) => {
        console.log('Admin items error:', error);

        this.message =
          error.error?.message ||
          'Unable to load items.';
      }

    });

  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

}