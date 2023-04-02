import {Injectable} from '@angular/core';
import {User} from '../models/user.model';
import {Store} from '@ngrx/store';
import {KeycloakService} from 'keycloak-angular';
import {Router} from '@angular/router';
import {KEYCLOAK_CONFIG} from '../../commons';
import {AppState} from '../models/app-state.model';

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
    return this.kcService.getKeycloakInstance().hasResourceRole(role, KEYCLOAK_CONFIG.resource_name);
  }

  async isLoggedIn(): Promise<boolean> {
    return await this.kcService.isLoggedIn();
  }

  logout(): void {
    this.router.navigate(['/info']).then(r => this.kcService.logout());
  }

  login(): void {
    this.kcService.login().then(

      r => this.router.navigate(['/'])

    );
  }
}
