import { Component, OnInit } from '@angular/core';
import {APP_TITLE_LONG} from '../../../commons';

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
    { link: 'sys-logs', label: 'Sys-Logs'},
  ];

  ngOnInit(): void {
  }

}
