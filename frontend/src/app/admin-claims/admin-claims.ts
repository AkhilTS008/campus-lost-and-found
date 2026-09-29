// import { Component, OnDestroy, OnInit } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { Router, RouterLink } from '@angular/router';

// import { ClaimService } from '../services/claim';
// import { ToastService } from '../services/toast';
// import { AuthService } from '../services/auth';
// import { FormsModule } from '@angular/forms';

// @Component({
//   selector: 'app-admin-claims',
//   standalone: true,
//   imports: [
//     CommonModule,
//     RouterLink,
//     FormsModule
//   ],
//   templateUrl: './admin-claims.html',
//   styleUrl: './admin-claims.css'
// })
// export class AdminClaims implements OnInit, OnDestroy {

//   claims: any[] = [];
//   message = '';
//   private refreshTimer: any;

//   // Stores the status selected for each claim
//   selectedStatuses: { [key: number]: string } = {};

//   constructor(
//     private claimService: ClaimService,
//     private toastService: ToastService,
//     private authService: AuthService,
//     private router: Router
//   ) {}

//   ngOnInit() {
//     this.loadClaims();

//     this.refreshTimer = setInterval(() => {
//       this.loadClaims();
//     }, 5000);
//   }

//   ngOnDestroy() {
//     clearInterval(this.refreshTimer);
//   }

//   loadClaims() {
//     this.claimService.getAllClaims().subscribe({
//       next: (response) => {
//         // Show completed claims too
//         this.claims = response;
//       },
//       error: (error) => {
//         console.error('Admin claims error:', error);

//         this.message =
//           error.error?.message ||
//           'Unable to load claims.';
//       }
//     });
//   }

//   approveClaim(claimId: number) {
//     this.updateStatus(claimId, 'APPROVED');
//   }

//   rejectClaim(claimId: number) {
//     this.updateStatus(claimId, 'REJECTED');
//   }

//   reopenClaim(claimId: number) {
//     this.updateStatus(claimId, 'PENDING');
//   }

//   completeClaim(claimId: number) {
//     this.updateStatus(claimId, 'COMPLETED');
//   }

//   editStatus(claimId: number) {
//     const status = this.selectedStatuses[claimId];

//     if (!status) {
//       this.toastService.show(
//         'Please select a status.',
//         'error'
//       );
//       return;
//     }

//     this.updateStatus(claimId, status);
//   }

//   updateStatus(claimId: number, status: string) {
//     this.claimService.updateClaimStatus(
//       claimId,
//       status
//     ).subscribe({
//       next: () => {
//         this.toastService.show(
//           `Claim status changed to ${status}.`,
//           'success'
//         );

//         this.loadClaims();
//       },
//       error: (error) => {
//         console.error('Update claim error:', error);

//         this.toastService.show(
//           error.error?.message ||
//           'Failed to update claim.',
//           'error'
//         );
//       }
//     });
//   }

//   logout() {
//     this.authService.logout();
//     this.router.navigate(['/login']);
//   }
// }



// frontend/src/app/admin-claims/admin-claims.ts

import {
  Component,
  OnDestroy,
  OnInit
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { ClaimService } from '../services/claim';
import { ToastService } from '../services/toast';
import { AuthService } from '../services/auth';


@Component({
  selector: 'app-admin-claims',
  standalone: true,

  imports: [
    CommonModule,
    RouterLink,
    FormsModule
  ],

  templateUrl: './admin-claims.html',
  styleUrl: './admin-claims.css'
})
export class AdminClaims
  implements OnInit, OnDestroy {

  claims: any[] = [];

  message = '';

  private refreshTimer: any;

  selectedStatuses: {
    [key: number]: string
  } = {};

  constructor(
    private claimService: ClaimService,
    private toastService: ToastService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {

    this.loadClaims();

    this.refreshTimer =
      setInterval(() => {
        this.loadClaims();
      }, 5000);
  }

  ngOnDestroy() {

    clearInterval(
      this.refreshTimer
    );
  }

  loadClaims() {

    this.claimService
      .getAllClaims()
      .subscribe({

        next: (response) => {

          this.claims =
            response.filter(
              (claim: any) =>
                claim.status !== 'COMPLETED'
            );
        },

        error: (error) => {

          console.error(
            'Admin claims error:',
            error
          );

          this.message =
            error.error?.message ||
            'Unable to load claims.';
        }

      });
  }

  approveClaim(
    claimId: number
  ) {

    this.updateStatus(
      claimId,
      'APPROVED'
    );
  }

  rejectClaim(
    claimId: number
  ) {

    this.updateStatus(
      claimId,
      'REJECTED'
    );
  }

  reopenClaim(
    claimId: number
  ) {

    this.updateStatus(
      claimId,
      'PENDING'
    );
  }

  editStatus(
    claimId: number
  ) {

    const selectedStatus =
      this.selectedStatuses[claimId];

    if (!selectedStatus) {

      this.toastService.show(
        'Please select a status.',
        'error'
      );

      return;
    }

    this.updateStatus(
      claimId,
      selectedStatus
    );
  }

  updateStatus(
    claimId: number,
    status: string
  ) {

    this.claimService
      .updateClaimStatus(
        claimId,
        status
      )
      .subscribe({

        next: () => {

          this.toastService.show(
            `Claim status changed to ${status}.`,
            'success'
          );

          this.loadClaims();
        },

        error: (error) => {

          console.error(
            'Update claim error:',
            error
          );

          this.toastService.show(
            error.error?.message ||
            'Failed to update claim.',
            'error'
          );
        }

      });
  }

  logout() {

    this.authService.logout();

    this.router.navigate([
      '/login'
    ]);
  }
}