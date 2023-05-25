import { Component, OnInit } from '@angular/core';
import {APP_TITLE_LONG} from '../../../commons';
import {environment} from '../../../../environments/environment';
import {KeycloakService} from 'keycloak-angular';
import {Router} from '@angular/router';
import {UserService} from '../../../store/services/user.service';
import {SocketioService} from '../../../store/services/socketio.service';
import {KeycloakAdminBackendService} from '../../../store/services/keycloak-admin-backend.service';

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
    { link: 'fdp', label: 'FDP' },
    //{ link: 'sys-logs', label: 'Sys-Logs'},
  ];

  loggedIn = false;
  username = '';

  constructor(
    private ksService: KeycloakService,
    private router: Router,
    private userService: UserService,
    private socketioService: SocketioService,
    private kc_admin_service: KeycloakAdminBackendService,
  ) {
  }

  ngOnInit(): void {
    this.userService.isLoggedIn().then(r => {
      this.loggedIn = r;
      if (r) {
        this.username = this.userService.getUsername();
        this.socketioService.addInstanceUpdatesListener();
        this.socketioService.addActivityUpdatesListener();
      }
    });

    const isAdmin: boolean = this.ksService.isUserInRole(environment.KEYCLOAK_CONFIG.roles.admin)
    if (isAdmin) {

      // is admin user -> add admin tabs to navigation
      this.navigation.push(
        { link: 'sys-logs', label: 'Sys-Logs'},
        { link: 'instance-mgmt', label: 'Dashboard'},
        { link: 'user-mgmt', label: 'Users'},
      );

      // add admin listeners
      this.socketioService.addUserUpdatesListener();
      this.kc_admin_service.refreshStoreUsers();
    }

  }

  initiateLogout(): void {
    this.userService.logout();
  }

  initiateLogin(): void {
    this.userService.login();
  }
}
