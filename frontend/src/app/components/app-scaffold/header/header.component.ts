import { Component, OnInit } from '@angular/core';
import {APP_TITLE_LONG} from '../../../commons';
import {environment} from '../../../../environments/environment';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  title = APP_TITLE_LONG;

  navigation = [
    { link: 'applications', label: 'Store' },
    { link: 'instances', label: 'Instances' },
    { link: 'activities', label: 'Activities' },
    { link: 'http://fdp.' + environment.BASEURL, label: 'FDP' },
    { link: 'sys-logs', label: 'Sys-Logs'},
  ];

  ngOnInit(): void {
  }

}
