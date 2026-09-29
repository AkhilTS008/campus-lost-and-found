// import { Injectable } from '@angular/core';
// import { HttpClient } from '@angular/common/http';

// @Injectable({
//   providedIn: 'root'
// })
// export class ClaimService {

//   private apiUrl = 'http://127.0.0.1:8000/api/claims/';
//   private adminUrl = 'http://127.0.0.1:8000/api/admin/claims/';

//   constructor(private http: HttpClient) {}

//   // Create claim
//   createClaim(itemId: number, reason: string) {

//     return this.http.post<any>(
//       this.apiUrl,
//       {
//         item: itemId,
//         reason: reason
//       }
//     );
//   }

//   // Get my claims
//   getMyClaims() {

//     return this.http.get<any[]>(
//       this.apiUrl
//     );
//   }

//   // Admin - get all claims
//   getAllClaims() {

//     return this.http.get<any[]>(
//       this.adminUrl
//     );
//   }

//   // Admin - approve/reject claim
//   updateClaimStatus(
//     claimId: number,
//     status: string
//   ) {

//     return this.http.put<any>(
//       `${this.adminUrl}${claimId}/`,
//       {
//         status: status
//       }
//     );
//   }

//   // Complete claim
//   completeClaim(claimId: number) {

//     return this.http.put<any>(
//       `${this.apiUrl}${claimId}/complete/`,
//       {}
//     );
//   }

//   // Delete my own claim
//   deleteClaim(claimId: number) {
//     return this.http.delete<any>(
//     `${this.apiUrl}${claimId}/`
//     );
//   }

// }


// frontend/src/app/services/claim.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ClaimService {

  private apiUrl =
    'https://campus-lost-found-backend-j3iz.onrender.com/api/claims/';

  private adminUrl =
    'https://campus-lost-found-backend-j3iz.onrender.com/api/admin/claims/';

  constructor(
    private http: HttpClient
  ) {}

  createClaim(
    itemId: number,
    reason: string
  ) {
    return this.http.post<any>(
      this.apiUrl,
      {
        item: itemId,
        reason: reason
      }
    );
  }

  getMyClaims() {
    return this.http.get<any[]>(
      this.apiUrl
    );
  }

  getAllClaims() {
    return this.http.get<any[]>(
      this.adminUrl
    );
  }

  updateClaimStatus(
    claimId: number,
    status: string
  ) {
    return this.http.put<any>(
      `${this.adminUrl}${claimId}/`,
      {
        status: status
      }
    );
  }

  completeClaim(
    claimId: number
  ) {
    return this.http.put<any>(
      `${this.apiUrl}${claimId}/complete/`,
      {}
    );
  }

  deleteClaim(
    claimId: number
  ) {
    return this.http.delete<any>(
      `${this.apiUrl}${claimId}/`
    );
  }
}