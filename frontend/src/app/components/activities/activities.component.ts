import {Component, OnDestroy, OnInit} from '@angular/core';
import {ACTIVITY_STATES, SVG_PATHS} from '../../commons';
import {ActivityService} from '../../store/services/activity.service';
import {ActivityItem, LogItem} from '../../store/models/activity.model';
import {ActivatedRoute, Router} from '@angular/router';
import {interval, Subscription} from 'rxjs';
import {startWith, switchMap} from 'rxjs/operators';
import {AppState} from '../../store/models/app-state.model';
import {select, Store} from '@ngrx/store';
import * as activitySelector from '../../store/selectors/activity.selector';

@Component({
  selector: 'app-activities',
  templateUrl: './activities.component.html',
  styleUrls: ['./activities.component.scss']
})
export class ActivitiesComponent implements OnInit, OnDestroy {
  focussedActivityID: number; // = this.router.getCurrentNavigation().extras.state?.index || undefined;

  svgPaths = SVG_PATHS;
  activityStates = ACTIVITY_STATES;

  LOG_TYPES = {
    WARNING : 'WARNING',
    ERROR: 'ERROR',
    INFO: 'INFO'
  };

  activityList: ActivityItem[] = [];
  activityLogs: LogItem[] = [];
  timeInterval: Subscription = interval(1000).subscribe();

  // rm route, data$ ...

  constructor(
    private activityService: ActivityService,
    private router: Router,
    private route: ActivatedRoute,
    private store: Store<AppState>) {

      this.route.params.subscribe(params =>
        this.focussedActivityID = params.activity_id
      );

      this.store.pipe(select(activitySelector.selectAllActivities)).subscribe((res) => {
        this.activityList = res;
        this.sortActivityList();
      });

      if (this.focussedActivityID !== undefined){
        this.getLogsOfActivity(this.focussedActivityID);
      }
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    this.timeInterval.unsubscribe();
  }

  getLogsOfActivity(activityID: number): void {
    this.timeInterval.unsubscribe();
    this.timeInterval = interval(5000)
      .pipe(
        startWith(0),
        switchMap(() => this.activityService.getLogsOfActivity(activityID))
      ).subscribe((res: LogItem[]) => this.activityLogs = res);
    this.activityService.getLogsOfActivity(activityID).subscribe((res) => this.activityLogs = res);
  }

  unsubscribeFromLogs(): void {
    this.timeInterval.unsubscribe();
  }

  clearLogs(): void {
    this.activityLogs = [];
  }

  sortActivityList(): void {
    this.activityList.sort((a, b) => (a.start_time < b.start_time) ? 1 : 0);
  }
}
