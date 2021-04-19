import { Component, OnInit } from '@angular/core';
import {SVG_PATHS} from '../../commons';

@Component({
  selector: 'app-activities',
  templateUrl: './activities.component.html',
  styleUrls: ['./activities.component.scss']
})
export class ActivitiesComponent implements OnInit {

  svgPaths = SVG_PATHS;
  activityStates = {
    finished : 'assets/img/done.png',
    error: 'assets/img/error.png',
    ongoing: 'assets/img/lock.png'
  };

  constructor() { }

  ngOnInit(): void {
  }

  loadActivityLogs(): void {

  }

}
