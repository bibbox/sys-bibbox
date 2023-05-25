import {Injectable} from '@angular/core';
import {Store} from '@ngrx/store';
import {KeycloakService} from 'keycloak-angular';
import {Router} from '@angular/router';
import {AppState} from '../models/app-state.model';
import {environment} from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(
    private store: Store<AppState>,
    private kcService: KeycloakService,
    private router: Router,
  ) {
  }

  getUserID(): string {
    return this.kcService.getKeycloakInstance().subject;
  }

  getUsername(): string {
    return this.kcService.getKeycloakInstance().tokenParsed.preferred_username;
  }

  isRole(role: string): boolean {
    return this.kcService.getKeycloakInstance().hasRealmRole(role);
  }

  async isLoggedIn(): Promise<boolean> {
    return await this.kcService.isLoggedIn();
  }

  logout(): void {
    this.router.navigate(['/info']).then(() => this.kcService.logout());
  }

  login(): void {
    this.kcService.login().then(

      () => this.router.navigate(['/'])

    );
  }
}
