import { Component, OnInit } from '@angular/core';
import {APP_TITLE_LONG, KEYCLOAK_ROLES} from '../../../commons';
import {KeycloakService} from 'keycloak-angular';

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

  constructor(
    private ksService: KeycloakService
  ) {
  }


  ngOnInit(): void {
    // is admin user -> add sys-logs to navigation
    this.ksService.isUserInRole(KEYCLOAK_ROLES.admin) ? this.navigation.push({ link: 'sys-logs', label: 'Sys-Logs'}) : null;
  }

  logout(): void {
    // implement keycloak logout
  }
}
