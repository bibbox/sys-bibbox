import { Component, OnInit } from '@angular/core';
import {SVG_PATHS} from '../../../commons';
import {ActivityItem} from '../../../store/models/activity.model';
import {ActivityService} from '../../../store/services/activity.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-activity-menu-overlay',
  templateUrl: './activity-menu-overlay.component.html',
  styleUrls: ['./activity-menu-overlay.component.scss']
})
export class ActivityMenuOverlayComponent implements OnInit {

  svgPaths = SVG_PATHS;
  activityStates = {
    finished : 'assets/done.png',
    error: 'assets/error.png',
    ongoing: 'assets/loading.gif'
  };
  activityList: ActivityItem[] = [];
  activeActivities: number;
  constructor(
    private activityService: ActivityService,
    private router: Router) { }

  ngOnInit(): void {
    this.getActivities();
  }

  getActivities(): void {
    this.activityService.getActivities().subscribe(
      (res) => {
        this.activityList = res;
        this.checkForActiveActivities();
      }
    );
  }

  checkForActiveActivities(): void {
    this.activeActivities = 0;
    this.activityList.forEach(value => {
      if (value.finished_time === 'None') {
        this.activeActivities += 1;
      }
    });
    console.log(this.activeActivities);
  }

  openReferredActivity(activityID: number): void {
    this.router.navigate(['activities', {activityID}]).then();
    console.log(activityID);
  }
}
