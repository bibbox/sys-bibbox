import { Component, OnInit } from '@angular/core';
import {ACTIVITY_STATES, SVG_PATHS} from '../../../commons';
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
  activityStates = ACTIVITY_STATES;

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
        this.sortActivities();
      });
  }


  ngOnInit(): void {
  }

  countActiveActivities(): void {
    this.activeActivities = 0;
    this.activityList.forEach(value => {
      if (value.finished_time === '') {
        this.activeActivities += 1;
      }
    });
    // console.log('active activities: ', this.activeActivities);
  }

  sortActivities(): void {
    this.activityList.sort((a, b) => (a.id < b.id) ? 1 : -1);
  }

  setLastActivityStatus(): void {
    if (this.activityList.length) {
      this.lastActivityStatus = this.activityList.reduce(
        (prev, current) => (prev.finished_time > current.finished_time) ? prev : current).result;
    }
  }
}
