import {Injectable} from '@angular/core';
import {User} from '../models/user.model';
import {Store} from '@ngrx/store';
import {KeycloakService} from 'keycloak-angular';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  user: User;

  constructor(
    private store: Store<{AppState}>,
    private kcService: KeycloakService
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

  checkIfUserIsRole(role: string): boolean {
    return this.getUserRoles().includes(role);
  }


  canSeeSysLogs(): boolean {
    return this.getUserRoles().includes('can_see_syslogs');
  }

  debug(): void {

    console.warn(this.user.roles);
    // console.warn(this.kcService.getKeycloakInstance().tokenParsed.resource_access['sys-bibbox-frontend'].roles);
    console.log("------------------")
    console.warn(this.kcService.getKeycloakInstance().loadUserInfo());
    console.log("------------------")
    console.warn(this.kcService.getKeycloakInstance().tokenParsed.sub);
    console.log("------------------")
    console.warn(this.kcService.getKeycloakInstance().idTokenParsed);
    console.log("------------------")
  }
}
