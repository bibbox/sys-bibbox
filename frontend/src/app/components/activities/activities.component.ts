import { Component, OnInit } from '@angular/core';
import {SVG_PATHS} from '../../commons';
import {ActivityService} from '../../store/services/activity.service';
import {ActivityItem, LogItem} from '../../store/models/activity.model';

@Component({
  selector: 'app-activities',
  templateUrl: './activities.component.html',
  styleUrls: ['./activities.component.scss']
})
export class ActivitiesComponent implements OnInit {

  svgPaths = SVG_PATHS;
  activityStates = {
    finished : 'assets/done.png',
    error: 'assets/error.png',
    ongoing: 'assets/lock.png'
  };
  activityList: ActivityItem[];
  activityLogs: LogItem[];
  constructor(private activityService: ActivityService) { }

  ngOnInit(): void {
    this.getActivities();
  }

  getActivities(): void {
    this.activityService.getActivities().subscribe(
      (res) => this.activityList = res
    );
    // this.activityList.sort((a, b) => (a.id < b.id) ? 1 : -1);
  }

  getLogsOfActivity(activityID: number): void {
    this.activityService.getLogsOfActivity(activityID).subscribe(
      (res) => this.activityLogs = res
    );
  }
}
