import { NgModule } from '@angular/core';
import {ActivatedRouteSnapshot, RouterModule, RouterStateSnapshot, Routes} from '@angular/router';
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
import {AdminPanelSysLogsComponent} from './components/admin-panel-sys-logs/admin-panel-sys-logs.component';
import {AuthGuard} from './guard/auth.guard';
import {InfoComponent} from './components/info/info.component';
import {environment} from '../environments/environment';
import {AdminPanelInstancesComponent} from './components/admin-panel-instances/admin-panel-instances.component';
import {AdminPanelUsersComponent} from './components/admin-panel-users/admin-panel-users.component';

const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'info'}, // upon reaching baseurl, redirect to the login page
  // { path: '', redirectTo: '/applications', pathMatch: 'full'}, // -> upon reaching baseurl we want to redirect to the store page for now
  { path: 'install/:application_name/:version', component: InstallScreenComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: 'instances/:instance_name', component: InstanceDetailPageComponent, pathMatch: 'full', canActivate: [AuthGuard]},

  // top nav
  { path: 'applications', component: ApplicationsComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: 'instances', component: InstancesComponent, pathMatch: 'full', canActivate: [AuthGuard]},
  { path: 'fdp', component: ApplicationsComponent, resolve: { url: 'externalUrlRedirectResolver'}, data: {externalUrl: 'http://fdp.' + environment.BASEURL}, canActivate: [AuthGuard]},
  { path: 'activities/:activity_id', component: ActivitiesComponent, pathMatch: 'full', canActivate: [AuthGuard]}, // activities need two routes, in case we want to view activities without providing an activity id
  { path: 'activities', component: ActivitiesComponent, pathMatch: 'full', canActivate: [AuthGuard]},

  // top nav admin
  { path: 'sys-logs', component: AdminPanelSysLogsComponent, pathMatch: 'full', canActivate: [AuthGuard], data: {roles: [environment.KEYCLOAK_CONFIG.roles.admin]}},
  { path: 'instance-mgmt', component: AdminPanelInstancesComponent, pathMatch: 'full', canActivate: [AuthGuard], data: {roles: [environment.KEYCLOAK_CONFIG.roles.admin]}},
  { path: 'user-mgmt', component: AdminPanelUsersComponent, pathMatch: 'full', canActivate: [AuthGuard], data: {roles: [environment.KEYCLOAK_CONFIG.roles.admin]}},


  // { path: 'applications', component: ApplicationsComponent, pathMatch: 'full'},
  // { path: 'instances', component: InstancesComponent, pathMatch: 'full'},
  // { path: 'sys-logs', component: SysLogsComponent, pathMatch: 'full'},



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
  exports: [RouterModule],
  providers: [
    {
      provide: 'externalUrlRedirectResolver',
      useValue: (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) =>
      {
        //window.location.href = (route.data as any).externalUrl;
        // Open in new tab instead of same window
        window.open((route.data as any).externalUrl, "_blank");
      }
    }
  ]
})

export class AppRoutingModule { }


