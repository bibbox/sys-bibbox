import {Component, ElementRef, OnDestroy, OnInit, Renderer2} from '@angular/core';
import {ACTIVITY_STATES, SVG_PATHS} from '../../commons';
import {ActivityService} from '../../store/services/activity.service';
import {ActivityItem, LogItem} from '../../store/models/activity.model';
import {ActivatedRoute} from '@angular/router';
import {interval, Subscription} from 'rxjs';
import {startWith, switchMap} from 'rxjs/operators';
import {AppState} from '../../store/models/app-state.model';
import {select, Store} from '@ngrx/store';
import * as activitySelector from '../../store/selectors/activity.selector';
import { FormControl } from '@angular/forms';
import { UpdateActivityFiltersAction } from '../../store/actions/activity.actions';

@Component({
  selector: 'app-activities',
  templateUrl: './activities.component.html',
  styleUrls: ['./activities.component.scss']
})
export class ActivitiesComponent implements OnInit, OnDestroy {
  focussedActivityID: number;

  svgPaths = SVG_PATHS;
  activityStates = ACTIVITY_STATES;

  LOG_TYPES = {
    WARNING : 'WARNING',
    ERROR: 'ERROR',
    INFO: 'INFO'
  };

  activityList: ActivityItem[] = [];
  filteredActivityList: ActivityItem[] = [];
  activityLogs: LogItem[] = [];
  timeInterval: Subscription = interval(1000).subscribe();
  searchFormControl = new FormControl('');
  stateFormControl = new FormControl('');
  typeFormControl = new FormControl('');
  initialized = false;

  // rm route, data$ ...

  constructor(
    private activityService: ActivityService,
    private route: ActivatedRoute,
    private store: Store<AppState>,
    private elementRef: ElementRef,
    private renderer: Renderer2
  ) {
  }

  ngOnInit(): void {
    this.store.pipe(select(activitySelector.selectActivityFilters)).subscribe((res) => {
      if(!this.initialized) {
        this.searchFormControl.setValue(res.searchterm);
        this.stateFormControl.setValue(res.state);
        this.typeFormControl.setValue(res.type);

        this.initialized = true;
      }
    });

    this.route.params.subscribe(params =>
      this.focussedActivityID = params.activity_id
    );

    this.store.pipe(select(activitySelector.selectAllActivities)).subscribe((res) => {
      this.activityList = res.slice(0, 50);
      this.sortActivityList();
      this.filter();
    });

    if (this.focussedActivityID !== undefined) {
      this.getLogsOfActivity(this.focussedActivityID);
    }
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

    this.activityService.getLogsOfActivity(activityID).subscribe((res) => {
      this.activityLogs = res;

      // Scroll to the bottom of the log container element
      setTimeout(() => {
        const logContainer = this.elementRef.nativeElement.querySelector('.logs');
        this.renderer.setProperty(logContainer, 'scrollTop', logContainer?.scrollHeight || 0);
      }, 0);
    });
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

  filter(): void {
    this.filteredActivityList = this.activityList.filter(this.checkIfMatchesFilterCriteria);

    this.updateFiltersInStore();
  }

  checkIfMatchesFilterCriteria = (activity: ActivityItem): boolean => {
    const searchterm = this.searchFormControl.value.toLowerCase().trim();
    const type = this.typeFormControl.value;
    const state = this.stateFormControl.value;

    if(!!state && activity.state !== state)
      return false;

    if(!!type && activity.type !== type)
      return false;
      
    if(!!searchterm && !activity.name.includes(searchterm) &&
      (!activity?.user?.id || ![activity.user.username, activity.user.firstName, activity.user.lastName]
        .filter(item => !!item)
        .join(' ')
        .toLowerCase()
        .includes(searchterm)))
      return false;

    return true;
  };

  updateFiltersInStore(): void {
    this.store.dispatch(new UpdateActivityFiltersAction({
      searchterm: this.searchFormControl.value,
      state: this.stateFormControl.value,
      type: this.typeFormControl.value
    }));
  }
}
