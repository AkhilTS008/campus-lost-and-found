import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { ItemService } from '../services/item';
import { Navbar } from '../navbar/navbar';

@Component({
  selector: 'app-items',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,Navbar
  ],
  templateUrl: './items.html',
  styleUrl: './items.css'
})
export class Items implements OnInit {

  items: any[] = [];

  search = '';
  itemType = '';
  category = '';
  location = '';

  message = '';

  constructor(
    private itemService: ItemService
  ) {}

  ngOnInit() {

    this.loadItems();

  }

  loadItems() {

    const filters = {
      search: this.search,
      item_type: this.itemType,
      category: this.category,
      location: this.location
    };

    this.itemService.getItems(filters).subscribe({

      next: (response) => {

        this.items = response;

        console.log('Items:', response);

      },

      error: (error) => {

        console.log('Error:', error);

        this.message =
          'Unable to load items.';
      }

    });

  }

  searchItems() {

    this.loadItems();

  }

  clearFilters() {

    this.search = '';
    this.itemType = '';
    this.category = '';
    this.location = '';

    this.loadItems();

  }

}