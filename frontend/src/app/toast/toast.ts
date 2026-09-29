import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ToastService } from '../services/toast';

@Component({
  selector: 'app-toast',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './toast.html',
  styleUrl: './toast.css'
})
export class Toast implements OnInit {

  message = '';
  type = 'success';
  visible = false;

  constructor(
    private toastService: ToastService
  ) {}

  ngOnInit() {

    this.toastService.toast$.subscribe(
      (toast: { message: string; type: string }) => {

        this.message = toast.message;
        this.type = toast.type;
        this.visible = true;

        setTimeout(() => {
          this.visible = false;
        }, 3000);

      }
    );

  }

  close() {
    this.visible = false;
  }
}