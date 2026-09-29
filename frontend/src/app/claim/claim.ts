import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { ClaimService } from '../services/claim';
import { ToastService } from '../services/toast';
import { Navbar } from '../navbar/navbar';

@Component({
  selector: 'app-claim',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,Navbar
  ],
  templateUrl: './claim.html',
  styleUrl: './claim.css'
})
export class Claim implements OnInit {

  itemId = 0;

  reason = '';

  message = '';

  loading = false;

  constructor(
    private route: ActivatedRoute,
    private claimService: ClaimService,
    private router: Router,
    private toastService: ToastService
  ) {}

  ngOnInit() {

    this.itemId = Number(
      this.route.snapshot.paramMap.get('id')
    );

  }

  submitClaim() {

    if (!this.reason.trim()) {

      this.message =
        'Please enter a reason.';

      return;
    }

    this.loading = true;

    this.claimService.createClaim(
      this.itemId,
      this.reason
    ).subscribe({

      next: (response) => {

        console.log('Claim created:', response);

        this.toastService.show('Claim submitted successfully!', 'success');

        this.loading = false;

        setTimeout(() => {

          this.router.navigate(['/claims']);

        }, 1000);

      },

      error: (error) => {

        console.log('Claim error:', error);

        this.loading = false;

        this.toastService.show(
          error.error?.message ||
          'Failed to submit claim. Please try again.',
          'error'
        );
      }

    });

  }

}
