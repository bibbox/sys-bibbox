import {NgModule, isDevMode, APP_INITIALIZER} from '@angular/core';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {BrowserModule} from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import {initializeKeycloak} from './keycloak-init.factory';

// design design modules
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {FlexLayoutModule} from '@angular/flex-layout';
// import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {MatCardModule} from '@angular/material/card';
import {FontAwesomeModule} from '@fortawesome/angular-fontawesome';
import {MatTooltipModule} from '@angular/material/tooltip';
import {MatTabsModule} from '@angular/material/tabs';
// import {MatGridListModule} from '@angular/material/grid-list';
// import {MatListModule} from '@angular/material/list';
import {MatDialogModule} from '@angular/material/dialog';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatOptionModule} from '@angular/material/core';
import {MatSelectModule} from '@angular/material/select';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatSnackBar, MatSnackBarModule} from '@angular/material/snack-bar';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatMenuModule} from '@angular/material/menu';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';


// ngrx store
import {MetaReducer, StoreModule} from '@ngrx/store';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import {EffectsModule} from '@ngrx/effects';
import {storeFreeze} from 'ngrx-store-freeze';
import {AppState} from './store/models/app-state.model';
import {InstanceReducer} from './store/reducers/instance.reducer';
import {ActivityReducer} from './store/reducers/activity.reducer';
import {ApplicationGroupReducer} from './store/reducers/application-group.reducer';
import {ActivityEffects} from './store/effects/activity.effects';
import {InstanceEffects} from './store/effects/instance.effects';
import {ApplicationsEffects} from './store/effects/applications.effects';

// app root modules
import { AppRoutingModule } from './app-routing.module';
import {environment} from '../environments/environment';
import {HttperrorInterceptor} from './httperror.interceptor';

// services
import {SocketioService} from './store/services/socketio.service';

// component modules
import { AppComponent } from './components/app-scaffold/app.component';
import { HeaderComponent } from './components/app-scaffold/header/header.component';
import { FooterComponent } from './components/app-scaffold/footer/footer.component';
import { InstancesComponent } from './components/instances/instances.component';
import { ApplicationsComponent } from './components/applications/applications.component';
import { ContactComponent } from './components/about/contact/contact.component';
import { PartnersComponent } from './components/about/partners/partners.component';
import { ImprintComponent } from './components/about/imprint/imprint.component';
import { ActivitiesComponent } from './components/activities/activities.component';
import { LoginComponent } from './components/login/login.component';
import { InstanceDetailPageComponent } from './components/instances/instance-detail-page/instance-detail-page.component';
import { ApplicationGroupComponent } from './components/applications/application-group/application-group.component';
import { ApplicationTileComponent} from './components/applications/application-group/application-tile/application-tile.component';
import { InstanceTileComponent } from './components/instances/instance-tile/instance-tile.component';
import { NotFoundComponent } from './components/not-found/not-found.component';
import { InstallScreenComponent } from './components/applications/install-screen/install-screen.component';
import { InstallScreenDialogComponent } from './components/applications/install-screen-dialog/install-screen-dialog.component';
import { ActivityMenuOverlayComponent } from './components/activities/activity-menu-overlay/activity-menu-overlay.component';
import { AdminPanelSysLogsComponent } from './components/admin-panel-sys-logs/admin-panel-sys-logs.component';
import { KeycloakAngularModule, KeycloakService } from 'keycloak-angular';
import { InfoComponent } from './components/info/info.component';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { AdminPanelInstancesComponent } from './components/admin-panel-instances/admin-panel-instances.component';
import {MatTableModule} from '@angular/material/table';
import { AdminPanelUsersComponent } from './components/admin-panel-users/admin-panel-users.component';
import {MatRadioModule} from '@angular/material/radio';
import { CreateUserDialogComponent } from './components/admin-panel-users/create-user-dialog/create-user-dialog.component';
import { ConfirmationDialogComponent } from './components/admin-panel-users/confirmation-dialog/confirmation-dialog.component';


export const metaReducers: MetaReducer<AppState>[] = !environment.production ?  [storeFreeze] : [];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    InstancesComponent,
    ApplicationsComponent,
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
    ActivityMenuOverlayComponent,
    AdminPanelSysLogsComponent,
    InfoComponent,
    AdminPanelInstancesComponent,
    AdminPanelUsersComponent,
    CreateUserDialogComponent,
    ConfirmationDialogComponent,
  ],
    imports: [
        // angular
        BrowserModule,
        BrowserAnimationsModule,
        CommonModule,
        AppRoutingModule,

        // http client
        HttpClientModule,

        // keycloak
        KeycloakAngularModule,

        // design
        MatButtonModule,
        MatToolbarModule,
        MatTooltipModule,
        MatMenuModule,
        MatIconModule,
        MatCardModule,
        MatTabsModule,

        // MatListModule,
        MatSelectModule,
        MatSnackBarModule,
        MatInputModule,
        MatDialogModule,

        // MatGridListModule,
        MatFormFieldModule,
        MatCheckboxModule,
        MatTabsModule,
        MatOptionModule,
        MatExpansionModule,
        MatProgressSpinnerModule,
        ReactiveFormsModule,
        FontAwesomeModule,
        FlexLayoutModule,
        FormsModule,
//    NgbModule,
        // store
        StoreModule.forRoot({
            instances: InstanceReducer,
            applicationGroups: ApplicationGroupReducer,
            activities: ActivityReducer
        }, {metaReducers}),
        EffectsModule.forRoot([InstanceEffects, ApplicationsEffects, ActivityEffects,]),
        StoreDevtoolsModule.instrument({maxAge: 25, name: 'BIBBOX Store'}),
        // StoreModule.forRoot({}, {}),
        StoreDevtoolsModule.instrument({maxAge: 25, logOnly: !isDevMode()}),
        MatSlideToggleModule,
        MatTableModule,
        MatRadioModule,
    ],
  bootstrap: [AppComponent],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttperrorInterceptor,
      multi: true,
      deps: [MatSnackBar]
    },
    {
      provide: APP_INITIALIZER,
      useFactory: initializeKeycloak,
      multi: true,
      deps: [KeycloakService],
    },
    SocketioService,
  ]
})
export class AppModule {}
