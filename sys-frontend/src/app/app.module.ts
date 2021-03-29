import {NgModule} from '@angular/core';
import { CommonModule } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {BrowserModule} from '@angular/platform-browser';
import {AppComponent} from './components/app-scaffold/app.component';
import {HeaderComponent} from './components/app-scaffold/header/header.component';
import {FooterComponent} from './components/app-scaffold/footer/footer.component';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { InstancesComponent } from './components/instances/instances.component';
import {ApplicationsComponent} from './components/applications/applications.component';
import { ProfileComponent } from './components/profile/profile.component';
import { ContactComponent } from './components/about/contact/contact.component';
import { PartnersComponent } from './components/about/partners/partners.component';
import { ImprintComponent } from './components/about/imprint/imprint.component';
import { ActivitiesComponent } from './components/activities/activities.component';
import {FlexLayoutModule} from '@angular/flex-layout';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { StoreModule } from '@ngrx/store';
import {FormsModule} from '@angular/forms';
import {ApplicationGroupReducer} from './store/reducers/application.reducer';
import {InstanceReducer} from './store/reducers/instance.reducer';
import {HttpClientModule} from '@angular/common/http';
import {MatCardModule} from '@angular/material/card';
import {FontAwesomeModule} from '@fortawesome/angular-fontawesome';
import {MatTooltipModule} from '@angular/material/tooltip';
import { LoginComponent } from './components/login/login.component';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { InstanceDetailPageComponent } from './components/instances/instance-detail-page/instance-detail-page.component';
import {MatTabsModule} from '@angular/material/tabs';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatListModule} from '@angular/material/list';
import { ApplicationGroupComponent } from './components/applications/application-group/application-group.component';
import {ApplicationTileComponent} from './components/applications/application-group/application-tile/application-tile.component';
import { InstanceTileComponent } from './components/instances/instance-tile/instance-tile.component';
import {EffectsModule} from '@ngrx/effects';
import {InstanceEffects} from './store/effects/instance.effects';
import {ApplicationsEffects} from './store/effects/applications.effects';
import { NotFoundComponent } from './components/not-found/not-found.component';
import { InstallScreenComponent } from './components/applications/install-screen/install-screen.component';
import { InstallScreenDialogComponent } from './components/applications/install-screen-dialog/install-screen-dialog.component';
import {MatDialogModule} from '@angular/material/dialog';
import {MatFormFieldModule} from '@angular/material/form-field';


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    InstancesComponent,
    ApplicationsComponent,
    ProfileComponent,
    ContactComponent,
    PartnersComponent,
    ImprintComponent,
    ActivitiesComponent,
    LoginComponent,
    InstanceDetailPageComponent,
    ApplicationTileComponent,
    ApplicationGroupComponent,
    ApplicationTileComponent,
    InstanceTileComponent,
    NotFoundComponent,
    InstallScreenComponent,
    InstallScreenDialogComponent,
  ],
  imports: [
    // angular
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    AppRoutingModule,

    // http client
    HttpClientModule,

    // design
    MatButtonModule,
    MatToolbarModule,
    MatTooltipModule,
    MatIconModule,
    MatCardModule,
    MatTabsModule,
    MatListModule,
    MatDialogModule,
    MatGridListModule,
    MatFormFieldModule,
    FontAwesomeModule,
    FlexLayoutModule,
    FormsModule,
    NgbModule,

    // store
    StoreModule.forRoot({
      instances: InstanceReducer,
      applications: ApplicationGroupReducer,
    }),
    EffectsModule.forRoot([InstanceEffects, ApplicationsEffects]),
    StoreDevtoolsModule.instrument({maxAge: 25}),
    MatTabsModule,

  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
