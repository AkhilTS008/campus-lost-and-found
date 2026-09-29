import { Routes } from '@angular/router';

import { Login } from './login/login';
import { Register } from './register/register';
import { Dashboard } from './dashboard/dashboard';

import { authGuard } from './auth.guard';
import { ReportItem } from './report-item/report-item';
import { Items } from './items/items';
import { ItemDetails } from './item-details/item-details';
import { Claim } from './claim/claim';
import { Claims } from './claims/claims';
import { AdminClaims } from './admin-claims/admin-claims';
import { Chat } from './chat/chat';
import { MyReports } from './my-reports/my-reports';
import { AdminDashboard } from './admin-dashboard/admin-dashboard';
import { Conversations } from './conversations/conversations';
import { adminGuard } from './admin-guard-guard';
import { AdminItems } from './admin-items/admin-items';

export const routes: Routes = [

  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },

  {
    path: 'login',
    component: Login
  },

  {
    path: 'register',
    component: Register
  },

  {
    path: 'dashboard',
    component: Dashboard,
    canActivate: [authGuard]
  },

  {
  path: 'report-item',
  component: ReportItem,
  canActivate: [authGuard]
  },

  {
  path: 'items',
  component: Items,
  canActivate: [authGuard]
  },

  {
  path: 'item/:id',
  component: ItemDetails,
  canActivate: [authGuard]
  },

  {
  path: 'claim/:id',
  component: Claim,
  canActivate: [authGuard]
  },

  {
  path: 'claims',
  component: Claims,
  canActivate: [authGuard]
  },

  {
  path: 'admin/claims',
  component: AdminClaims,
  canActivate: [adminGuard]
  },

  {
  path: 'chat/:id',
  component: Chat,
  canActivate: [authGuard]
  },
  {
  path: 'my-reports',
  component: MyReports,
  canActivate: [authGuard]
 },
 {
  path: 'admin-dashboard',
  component: AdminDashboard,
  canActivate: [adminGuard]
 },
 {
  path: 'conversations',
  component: Conversations,
  canActivate: [authGuard]
 },
 {
  path: 'admin/items',
  component: AdminItems,
  canActivate: [adminGuard]
},
 



];