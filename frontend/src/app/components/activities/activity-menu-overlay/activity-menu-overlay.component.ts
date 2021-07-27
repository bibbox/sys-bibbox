import { Component, OnInit } from '@angular/core';
import {SVG_PATHS} from '../../../commons';
import {ActivityItem} from '../../../store/models/activity.model';
import {ActivityService} from '../../../store/services/activity.service';
import {AppState} from '../../../store/models/app-state.model';
import {select, Store} from '@ngrx/store';
import * as activitySelector from '../../../store/selectors/activity.selector';

@Component({
  selector: 'app-activity-menu-overlay',
  templateUrl: './activity-menu-overlay.component.html',
  styleUrls: ['./activity-menu-overlay.component.scss']
})
export class ActivityMenuOverlayComponent implements OnInit {

  svgPaths = SVG_PATHS;
  activityList: ActivityItem[] = [];
  activeActivities: 0;
  lastActivityStatus: string;

  constructor(
    private activityService: ActivityService,
    private store: Store<AppState>
  ) {
      this.store.pipe(select(activitySelector.selectAllActivities)).subscribe((res) => {
        this.activityList = res;
        this.countActiveActivities();
        this.setLastActivityStatus();
      });
  }


  ngOnInit(): void {
  }

  countActiveActivities(): void {
    this.activeActivities = 0;
    this.activityList.forEach(value => {
      if (value.finished_time === 'None') {
        this.activeActivities += 1;
      }
    });
    console.log('active activities: ', this.activeActivities);
  }

  setLastActivityStatus(): void {
    if (this.activityList.length) {
      this.lastActivityStatus = this.activityList[this.activityList.length - 1].result;
    }
  }

  // openReferredActivity(activityID?: number): void {
  //   if (activityID) {
  //     this.router.navigate(['activities', {activityID}]).then();
  //     console.log('clicked activity: ', activityID);
  //   } else {
  //     this.router.navigate(['activities']).then();
  //   }
  // }
}
