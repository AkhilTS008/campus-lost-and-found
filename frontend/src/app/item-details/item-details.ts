import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { ItemService } from '../services/item';
import { Navbar } from '../navbar/navbar';

@Component({
  selector: 'app-item-details',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,Navbar
  ],
  templateUrl: './item-details.html',
  styleUrl: './item-details.css'
})
export class ItemDetails implements OnInit {

  item: any = null;
  message = '';

  constructor(
    private route: ActivatedRoute,
    private itemService: ItemService,
    private router: Router
  ) {}

  ngOnInit() {

    const id = Number(
      this.route.snapshot.paramMap.get('id')
    );

    this.loadItem(id);
  }

  loadItem(id: number) {

    this.itemService.getItem(id).subscribe({

      next: (response) => {

        this.item = response;

        console.log('Item:', response);

      },

      error: (error) => {

        console.log('Error:', error);

        this.message = 'Item not found.';
      }

    });

  }

  goToClaim() {

    this.router.navigate([
      '/claim',
      this.item.id
    ]);

  }

  getImageUrl(image: string): string {
  if (!image) {
    return '';
  }

  if (image.startsWith('http')) {
    return image;
  }

  return `http://127.0.0.1:8000${image}`;
}

}
