import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

import { ItemService } from '../services/item';
import { ToastService } from '../services/toast';
import { Navbar } from '../navbar/navbar';

@Component({
  selector: 'app-report-item',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,Navbar
  ],
  templateUrl: './report-item.html',
  styleUrl: './report-item.css'
})
export class ReportItem {

  itemName = '';
  category = '';
  description = '';
  location = '';
  date = '';
  itemType = 'LOST';

  selectedImage: File | null = null;

  message = '';

  constructor(
    private itemService: ItemService,
    private route: ActivatedRoute,
    private router: Router,
    private toastService: ToastService
  ) {

    this.route.queryParams.subscribe(params => {

    if (params['type'] === 'FOUND') {
        this.itemType = 'FOUND';
    } else {
        this.itemType = 'LOST';
    }

      

    });

  }

  selectImage(event: any) {

    const file = event.target.files[0];

    if (file) {
      this.selectedImage = file;
    }
  }

  submitItem() {

    const formData = new FormData();

    formData.append('item_name', this.itemName);
    formData.append('category', this.category);
    formData.append('description', this.description);
    formData.append('location', this.location);
    formData.append('date', this.date);
    formData.append('item_type', this.itemType);

    if (this.selectedImage) {

      formData.append(
        'image',
        this.selectedImage
      );

    }

    this.itemService.createItem(formData).subscribe({

      next: (response) => {

        console.log('Item created:', response);

        this.toastService.show('Item reported successfully!', 'success');

        setTimeout(() => {
          this.router.navigate(['/items']);
        }, 1000);

      },

      error: (error) => {

       this.toastService.show(
          error.error?.message ||
          'Failed to report item. Please try again.',
          'error'
        );
      }

    });

  }

}
