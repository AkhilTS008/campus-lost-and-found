import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { ItemService } from '../services/item';
import { Navbar } from '../navbar/navbar';
import { ToastService } from '../services/toast';

@Component({
  selector: 'app-my-reports',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    Navbar
  ],
  templateUrl: './my-reports.html',
  styleUrl: './my-reports.css'
})
export class MyReports implements OnInit, OnDestroy {

  reports: any[] = [];
  message = '';

  private refreshTimer: any;

  editingReportId: number | null = null;

  editData: any = {};
  selectedImage: File | null = null;
  imagePreview: string | null = null;

  constructor(
    private itemService: ItemService,
    private toastService: ToastService
  ) {}

  ngOnInit() {
    this.loadReports();

    this.refreshTimer = setInterval(() => {
      this.loadReports();
    }, 5000);
  }

  ngOnDestroy() {
    clearInterval(this.refreshTimer);
  }

  loadReports() {
    this.itemService.getMyReports().subscribe({
      next: (response) => {
        this.reports = response;
      },
      error: (error) => {
        console.error('My Reports error:', error);

        this.message =
          error.error?.message ||
          'Unable to load your reports.';
      }
    });
  }

  startEdit(report: any) {
    this.editingReportId = report.id;

    this.editData = {
      item_name: report.item_name,
      category: report.category,
      description: report.description,
      location: report.location,
      date: report.date,
      item_type: report.item_type
    };

    this.selectedImage = null;
    this.imagePreview = report.image
      ? (report.image.startsWith('http')
          ? report.image
          : 'http://127.0.0.1:8000' + report.image)
      : null;
  }

  cancelEdit() {
    this.editingReportId = null;
    this.editData = {};
    this.selectedImage = null;
    this.imagePreview = null;
  }

  selectImage(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (file) {
      this.selectedImage = file;
      this.imagePreview = URL.createObjectURL(file);
    }
  }

  saveEdit(reportId: number) {
    const formData = new FormData();

    formData.append('item_name', this.editData.item_name);
    formData.append('category', this.editData.category);
    formData.append('description', this.editData.description);
    formData.append('location', this.editData.location);
    formData.append('date', this.editData.date);

    if (this.selectedImage) {
      formData.append('image', this.selectedImage);
    }

    this.itemService.updateItem(reportId, formData).subscribe({
      next: () => {
        this.toastService.show(
          'Report updated successfully!',
          'success'
        );

        this.cancelEdit();
        this.loadReports();
      },
      error: (error) => {
        console.error('Update report error:', error);

        this.toastService.show(
          error.error?.message ||
          'Unable to update report.',
          'error'
        );
      }
    });
  }

  deleteReport(reportId: number) {
    const confirmed = confirm(
      'Are you sure you want to delete this report?'
    );

    if (!confirmed) {
      return;
    }

    this.itemService.deleteItem(reportId).subscribe({
      next: () => {
        this.toastService.show(
          'Report deleted successfully!',
          'success'
        );

        this.loadReports();
      },
      error: (error) => {
        console.error('Delete report error:', error);

        this.toastService.show(
          error.error?.message ||
          'Unable to delete this report.',
          'error'
        );
      }
    });
  }
}