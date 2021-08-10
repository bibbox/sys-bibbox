import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {CommonModule} from '@angular/common';
import {ApplicationsComponent} from './components/applications/applications.component';
import {InstancesComponent} from './components/instances/instances.component';
import {ContactComponent} from './components/about/contact/contact.component';
import {PartnersComponent} from './components/about/partners/partners.component';
import {ImprintComponent} from './components/about/imprint/imprint.component';
import {ActivitiesComponent} from './components/activities/activities.component';
import {LoginComponent} from './components/login/login.component';
import {InstanceDetailPageComponent} from './components/instances/instance-detail-page/instance-detail-page.component';
import {NotFoundComponent} from './components/not-found/not-found.component';
import {InstallScreenComponent} from './components/applications/install-screen/install-screen.component';
import {SysLogsComponent} from './components/sys-logs/sys-logs.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full'}, // -> upon reaching baseurl we want to redirect to the login page
  { path: 'install/:application_name/:version', component: InstallScreenComponent, pathMatch: 'full'},
  { path: 'instances/:instance_name', component: InstanceDetailPageComponent, pathMatch: 'full'},

  // top nav
  { path: 'applications', component: ApplicationsComponent, pathMatch: 'full'},
  { path: 'instances', component: InstancesComponent, pathMatch: 'full'},
  { path: 'sys-logs', component: SysLogsComponent, pathMatch: 'full'},
  // activities need two routes, in case we want to view activities without providing an activity id
  { path: 'activities/:activity_id', component: ActivitiesComponent, pathMatch: 'full'},
  { path: 'activities', component: ActivitiesComponent, pathMatch: 'full'},

  // bottom nav
  { path: 'contact', component: ContactComponent, pathMatch: 'full'},
  { path: 'partners', component: PartnersComponent, pathMatch: 'full'},
  { path: 'imprint', component: ImprintComponent, pathMatch: 'full'},

  // auth
  { path: 'login', component: LoginComponent, pathMatch: 'full'},
  { path: '**', component: NotFoundComponent}, // -> 404 page
];

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    RouterModule.forRoot(routes,
     // {useHash: true}
    ),
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
