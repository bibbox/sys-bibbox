import {Inject, Injectable} from '@angular/core';
import {Store} from '@ngrx/store';
import {KeycloakService} from 'keycloak-angular';
import {Router} from '@angular/router';
import {AppState} from '../models/app-state.model';
import {environment} from '../../../environments/environment';
import { DOCUMENT } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(
    private store: Store<AppState>,
    private kcService: KeycloakService,
    private router: Router,
    @Inject(DOCUMENT) private document: Document
  ) {
  }

  getUserID(): string {
    return this.kcService.getKeycloakInstance().subject;
  }

  getUsername(): string {
    return this.kcService.getKeycloakInstance().tokenParsed.preferred_username;
  }

  async getFullOrUsername(): Promise<string> {
    const profile = await this.kcService.loadUserProfile();
    return [profile.firstName, profile.lastName].filter(item => !!item).join(' ') || this.getUsername();
  }

  isRole(role: string): boolean {
    return this.kcService.getKeycloakInstance().hasRealmRole(role);
  }

  async isLoggedIn(): Promise<boolean> {
    return await this.kcService.isLoggedIn();
  }

  logout(): void {
    this.kcService.logout(document.location.origin + '/');
  }

  switchAccount(): void {
    this.kcService.logout(document.location.origin + '/instances');
  }

  login(): void {
    this.kcService.login({ redirectUri: document.location.origin + '/instances' });
  }
}
