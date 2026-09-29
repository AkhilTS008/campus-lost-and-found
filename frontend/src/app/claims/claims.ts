// import { Component, OnInit, OnDestroy } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { RouterLink } from '@angular/router';

// import { ClaimService } from '../services/claim';
// import { ToastService } from '../services/toast';
// import { Navbar } from '../navbar/navbar';

// import { interval, Subscription } from 'rxjs';

// @Component({
//   selector: 'app-claims',
//   standalone: true,
//   imports: [
//     CommonModule,
//     RouterLink,
//     Navbar
//   ],
//   templateUrl: './claims.html',
//   styleUrl: './claims.css'
// })
// export class Claims implements OnInit, OnDestroy {

//   claims: any[] = [];

//   message = '';

//   private refreshSubscription?: Subscription;

//   constructor(
//     private claimService: ClaimService,
//     private toastService: ToastService
//   ) {}

//   ngOnInit() {
//     // Load claims when the page opens
//     this.loadClaims();

//     // Automatically refresh claims every 10 seconds
//     this.refreshSubscription = interval(10000).subscribe(() => {
//       this.loadClaims();
//     });
//   }

//   loadClaims() {
//     this.claimService.getMyClaims().subscribe({

//       next: (response) => {
//         this.claims = response;
//         console.log('My claims:', response);
//       },

//       error: (error) => {
//         console.log('Error:', error);

//         this.message =
//           error.error?.message ||
//           'Unable to load claims.';
//       }

//     });
//   }

//   completeClaim(claimId: number) {
//     this.claimService.completeClaim(claimId).subscribe({

//       next: (response) => {
//         console.log('Claim completed:', response);

//         this.toastService.show(
//           'Claim completed successfully. Item has been returned.',
//           'success'
//         );

//         // Reload claims after completion
//         this.loadClaims();
//       },

//       error: (error) => {
//         console.log('Complete claim error:', error);

//         this.toastService.show(
//           error.error?.message ||
//           'Failed to complete claim. Please try again.',
//           'error'
//         );
//       }

//     });
//   }

//   ngOnDestroy() {
//     // Stop automatic refreshing when leaving the page
//     this.refreshSubscription?.unsubscribe();
//   }

//   deleteClaim(claimId: number) {
//   const confirmed = confirm(
//     'Are you sure you want to remove this claim?'
//   );

//   if (!confirmed) {
//     return;
//   }

//   this.claimService.deleteClaim(claimId).subscribe({
//     next: () => {
//       this.toastService.show(
//         'Claim removed successfully.',
//         'success'
//       );

//       this.loadClaims();
//     },

//     error: (error) => {
//       console.error('Delete claim error:', error);

//       this.toastService.show(
//         error.error?.message ||
//         'Unable to remove this claim.',
//         'error'
//       );
//     }
//   });
// }

// }



// frontend/src/app/claims/claims.ts

import {
  Component,
  OnInit,
  OnDestroy
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

import { ClaimService } from '../services/claim';
import { ToastService } from '../services/toast';
import { Navbar } from '../navbar/navbar';

import {
  interval,
  Subscription
} from 'rxjs';


@Component({
  selector: 'app-claims',
  standalone: true,

  imports: [
    CommonModule,
    RouterLink,
    Navbar
  ],

  templateUrl: './claims.html',
  styleUrl: './claims.css'
})
export class Claims
  implements OnInit, OnDestroy {

  claims: any[] = [];

  message = '';

  private refreshSubscription?: Subscription;

  constructor(
    private claimService: ClaimService,
    private toastService: ToastService
  ) {}

  ngOnInit() {

    this.loadClaims();

    this.refreshSubscription =
      interval(10000).subscribe(() => {
        this.loadClaims();
      });
  }

  loadClaims() {

    this.claimService.getMyClaims().subscribe({

      next: (response) => {

        this.claims = response.filter(
          (claim: any) =>
            claim.status !== 'COMPLETED'
        );

        console.log(
          'Active claims:',
          this.claims
        );
      },

      error: (error) => {

        console.log(
          'Error:',
          error
        );

        this.message =
          error.error?.message ||
          'Unable to load claims.';
      }

    });
  }

  completeClaim(
    claimId: number
  ) {

    this.claimService
      .completeClaim(claimId)
      .subscribe({

        next: (response) => {

          console.log(
            'Claim completed:',
            response
          );

          this.toastService.show(
            'Claim completed successfully. Item has been returned.',
            'success'
          );

          this.loadClaims();
        },

        error: (error) => {

          console.log(
            'Complete claim error:',
            error
          );

          this.toastService.show(
            error.error?.message ||
            'Failed to complete claim. Please try again.',
            'error'
          );
        }

      });
  }

  deleteClaim(
    claimId: number
  ) {

    const confirmed = confirm(
      'Are you sure you want to remove this claim?'
    );

    if (!confirmed) {
      return;
    }

    this.claimService
      .deleteClaim(claimId)
      .subscribe({

        next: () => {

          this.toastService.show(
            'Claim removed successfully.',
            'success'
          );

          this.loadClaims();
        },

        error: (error) => {

          console.error(
            'Delete claim error:',
            error
          );

          this.toastService.show(
            error.error?.message ||
            'Unable to remove this claim.',
            'error'
          );
        }

      });
  }

  ngOnDestroy() {

    this.refreshSubscription
      ?.unsubscribe();
  }
}

