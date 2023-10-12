import { Component, HostListener, Inject, OnInit } from '@angular/core';
import {APP_TITLE, APP_SUB_TITLE} from '../../../commons';
import {environment} from '../../../../environments/environment';
import {KeycloakService} from 'keycloak-angular';
import {Router} from '@angular/router';
import {UserService} from '../../../store/services/user.service';
import {SocketioService} from '../../../store/services/socketio.service';
import {KeycloakAdminBackendService} from '../../../store/services/keycloak-admin-backend.service';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  title = APP_TITLE;
  subtitle = APP_SUB_TITLE;

  navigation = [
    { link: 'applications', label: 'Store'},
    { link: 'instances', label: 'Instances' },
    { link: 'activities', label: 'Activities' },
    { link: 'fdp', label: 'FDP' }
  ];

  loggedIn = false;
  userFullname = '';
  isScrolled = false;
  isMobileMenuVisible = false;

  constructor(
    private ksService: KeycloakService,
    private router: Router,
    private userService: UserService,
    private socketioService: SocketioService,
    private kc_admin_service: KeycloakAdminBackendService,
    @Inject(DOCUMENT) private document: Document
  ) {
  }

  ngOnInit(): void {
    this.userService.isLoggedIn().then(async r => {
      this.loggedIn = r;
      if (r) {
        this.userFullname = await this.userService.getFullOrUsername();
        this.socketioService.addInstanceUpdatesListener();
        this.socketioService.addActivityUpdatesListener();
      }
    });

    const isAdmin: boolean = this.ksService.isUserInRole(environment.KEYCLOAK_CONFIG.roles.admin)
    if (isAdmin) {

      // is admin user -> add admin tabs to navigation
      this.navigation.push(
        { link: 'sys-logs', label: 'Sys-Logs'},
        // { link: 'instance-mgmt', label: 'Dashboard'},
        { link: 'user-mgmt', label: 'Users'},
      );

      // add admin listeners
      this.socketioService.addUserUpdatesListener();
      this.kc_admin_service.refreshStoreUsers();
    }

    this.checkScroll();
  }

  @HostListener('window:scroll', [])
  checkScroll() {
    if (document.body.scrollTop > 0 || document.documentElement.scrollTop > 0) {
      this.isScrolled = true;
    }
    else {
      this.isScrolled = false;
    }
  }

  initiateLogout(): void {
    this.userService.logout();
  }

  initiateLogin(): void {
    this.userService.login();
  }

  toggleMobileMenu(): void {
    this.isMobileMenuVisible = !this.isMobileMenuVisible;

    if(this.isMobileMenuVisible) {
      this.document.body.classList.add('mobile-menu-open');
    }
    else {
      this.document.body.classList.remove('mobile-menu-open');
    }
  }
}
