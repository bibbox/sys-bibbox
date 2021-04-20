import { Component, OnInit } from '@angular/core';
import {SVG_PATHS} from '../../commons';
import {ActivityService} from '../../store/services/activity.service';
import {ActivityItem} from '../../store/models/activity.model';

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
  activityList: ActivityItem[];
  constructor(private activityService: ActivityService) { }

  ngOnInit(): void {
    this.loadActivityLogs();
  }

  loadActivityLogs(): void {
    this.activityService.getActivities().subscribe(
      (res) => this.activityList = res
    );
  }

}
