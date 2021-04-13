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
import {MetaReducer, StoreModule} from '@ngrx/store';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {ApplicationGroupReducer} from './store/reducers/application-group.reducer';
import {InstanceReducer} from './store/reducers/instance.reducer';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
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
import {AuthReducer} from './store/reducers/auth.reducer';
import {MatInputModule} from '@angular/material/input';
import {MatOptionModule} from '@angular/material/core';
import {MatSelectModule} from '@angular/material/select';
import {environment} from '../environments/environment';
import {storeFreeze} from 'ngrx-store-freeze';
import {AppState} from './store/models/app-state.model';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { TestComponent } from './components/test/test.component';
import { CheckboxItemComponent } from './components/test/checkbox-item/checkbox-item.component';
import {HttperrorInterceptor} from './httperror.interceptor';
import {MatSnackBar, MatSnackBarModule} from '@angular/material/snack-bar';

export const metaReducers: MetaReducer<AppState>[] = !environment.production ?  [storeFreeze] : [];

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
    TestComponent,
    CheckboxItemComponent,
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
        MatSelectModule,
        MatSnackBarModule,
        MatInputModule,
        MatDialogModule,
        MatGridListModule,
        MatFormFieldModule,
        MatCheckboxModule,
        MatTabsModule,
        MatOptionModule,
        ReactiveFormsModule,
        FontAwesomeModule,
        FlexLayoutModule,
        FormsModule,
        NgbModule,

        // store
        StoreModule.forRoot({
            instances: InstanceReducer,
            applicationGroups: ApplicationGroupReducer,
            auth: AuthReducer,
        }, {metaReducers}),
        EffectsModule.forRoot([InstanceEffects, ApplicationsEffects]),
        StoreDevtoolsModule.instrument({maxAge: 25, name: 'BIBBOX Store'}),

    ],
  bootstrap: [AppComponent],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttperrorInterceptor,
      multi: true,
      deps: [MatSnackBar]
    }
  ]
})
export class AppModule {}
