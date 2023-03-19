import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {CommonModule} from '@angular/common';
import {ApplicationsComponent} from './components/applications/applications.component';
import {InstancesComponent} from './components/instances/instances.component';
import {ContactComponent} from './components/about/contact/contact.component';
import {PartnersComponent} from './components/about/partners/partners.component';
import {ImprintComponent} from './components/about/imprint/imprint.component';
import {ActivitiesComponent} from './components/activities/activities.component';
import {InstanceDetailPageComponent} from './components/instances/instance-detail-page/instance-detail-page.component';
import {NotFoundComponent} from './components/not-found/not-found.component';
import {InstallScreenComponent} from './components/applications/install-screen/install-screen.component';
import {SysLogsComponent} from './components/sys-logs/sys-logs.component';
import {AuthGuard} from './guard/auth.guard';
import {KEYCLOAK_ROLES} from './commons';
import {InfoComponent} from './components/info/info.component';

const routes: Routes = [
  // TODO redirect when login does anything
  { path: '', pathMatch: 'full', redirectTo: 'info'}, // upon reaching baseurl, redirect to the login page
  // { path: '', redirectTo: '/applications', pathMatch: 'full'}, // -> upon reaching baseurl we want to redirect to the store page for now
  { path: 'install/:application_name/:version', component: InstallScreenComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: 'instances/:instance_name', component: InstanceDetailPageComponent, pathMatch: 'full', canActivate: [AuthGuard]},

  // top nav
  { path: 'applications', component: ApplicationsComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: 'instances', component: InstancesComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: 'sys-logs', component: SysLogsComponent, pathMatch: 'full', canActivate: [AuthGuard], data: {roles: [KEYCLOAK_ROLES.admin]}},
  // activities need two routes, in case we want to view activities without providing an activity id
  { path: 'activities/:activity_id', component: ActivitiesComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: 'activities', component: ActivitiesComponent, pathMatch: 'full', canActivate: [AuthGuard]},

  // bottom nav
  { path: 'contact', component: ContactComponent, pathMatch: 'full'},
  { path: 'partners', component: PartnersComponent, pathMatch: 'full'},
  { path: 'imprint', component: ImprintComponent, pathMatch: 'full'},

  // info page which is displayed if the user is not logged in
  { path: 'info', component: InfoComponent, pathMatch: 'full'},

  // { path: 'login', component: LoginComponent, pathMatch: 'full'},
  { path: '**', component: NotFoundComponent, canActivate: [AuthGuard]}, // -> 404 page
];

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    RouterModule.forRoot(routes),
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
