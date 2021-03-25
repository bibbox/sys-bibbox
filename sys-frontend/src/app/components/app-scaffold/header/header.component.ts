import { Component, OnInit } from '@angular/core';
import {APP_TITLE_LONG} from '../../../commons';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  title = APP_TITLE_LONG;

  logoPath = '../../../../assets/img/silicolab_logo.svg';
  navigation = [
    { link: 'applications', label: 'Applications' },
    { link: 'instances', label: 'Instances' },
    { link: 'activities', label: 'Activities' },
    { link: 'profile', label: 'Profile' }
  ];

  ngOnInit(): void {
  }

}
