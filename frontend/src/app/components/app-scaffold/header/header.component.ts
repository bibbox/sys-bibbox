import { Component, OnInit } from '@angular/core';
import {APP_TITLE_LONG} from '../../../commons';
import {environment} from '../../../../environments/environment';
import {KeycloakService} from 'keycloak-angular';
import {Router} from '@angular/router';
import {UserService} from '../../../store/services/user.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  title = APP_TITLE_LONG;


  navigation = [
    { link: 'applications', label: 'Store'},
    { link: 'instances', label: 'Instances' },
    { link: 'activities', label: 'Activities' },
    //{ link: 'sys-logs', label: 'Sys-Logs'},
  ];

  loggedIn = false;
  username = '';

  constructor(
    private ksService: KeycloakService,
    private router: Router,
    private userService: UserService,
  ) {
  }

  ngOnInit(): void {
    // is admin user -> add sys-logs to navigation
    this.ksService.isUserInRole(environment.KEYCLOAK_ROLES.admin) ? this.navigation.push(
      { link: 'sys-logs', label: 'Sys-Logs'},
      { link: 'instance-mgmt', label: 'Dashboard'},
      { link: 'user-mgmt', label: 'Users'},
    ) : null;
    // this.userService.isLoggedIn().then(r => this.loggedIn = r);
    // this.username = this.userService.getUsername();
    this.userService.isLoggedIn().then(r => {
      this.loggedIn = r;
      if (r) {
        this.username = this.userService.getUsername();
      }
    });
  }

  initiateLogout(): void {
    this.userService.logout();
  }

  initiateLogin(): void {
    this.userService.login();
  }
}
