import {Injectable} from '@angular/core';
import {User} from '../models/user.model';
import {Store} from '@ngrx/store';
import {KeycloakService} from 'keycloak-angular';
import {Router} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  user: User;

  constructor(
    private store: Store<{AppState}>,
    private kcService: KeycloakService,
    private router: Router,
  ) {
    // just for testing
    this.kcService.getKeycloakInstance();
  }

  getUserID(): string {
    return this.kcService.getKeycloakInstance().tokenParsed.sub;
  }

  getUserRoles(): string[] {
    return this.kcService.getKeycloakInstance().tokenParsed.resource_access['sys-bibbox-frontend'].roles;
  }

  isRole(role: string): boolean {
    return this.getUserRoles().includes(role);
  }

  async isLoggedIn(): Promise<boolean> {
    return await this.kcService.isLoggedIn();
  }

  logout(): void {
    this.kcService.logout().then(r => this.router.navigate(['/info']));
  }

  login(): void {
    this.kcService.login().then(r => this.router.navigate(['/']));
  }
}
