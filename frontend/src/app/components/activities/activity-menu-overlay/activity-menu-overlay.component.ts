import { Component, OnInit } from '@angular/core';
import {ACTIVITY_STATES, SVG_PATHS} from '../../../commons';
import {ActivityItem} from '../../../store/models/activity.model';
import {ActivityService} from '../../../store/services/activity.service';
import {AppState} from '../../../store/models/app-state.model';
import {select, Store} from '@ngrx/store';
import * as activitySelector from '../../../store/selectors/activity.selector';
import { UserService } from '../../../store/services/user.service';
import { environment } from '../../../../environments/environment';

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
  showOverlay: boolean = false;
  isAdmin = false;

  constructor(
    private store: Store<AppState>,
    private userService: UserService
  ) {
      this.store.pipe(select(activitySelector.selectAllActivities)).subscribe((res) => {
        this.activityList = res;
        this.countActiveActivities();
        this.setLastActivityStatus();
        this.sortActivities();
      });
  }


  async ngOnInit(): Promise<void> {
    this.isAdmin = await this.userService.isRole(environment.KEYCLOAK_CONFIG.roles.admin);
  }

  countActiveActivities(): void {
    this.activeActivities = 0;
    this.activityList.forEach(value => {
      if (value.finished_time === '') {
        this.activeActivities += 1;
      }
    });
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

  toggleOverlay(): void {
    this.showOverlay = !this.showOverlay;
  }

  getNameOfUser(activity: ActivityItem): string {
    return [activity.user?.firstName, activity.user?.lastName].filter(item => !!item).join(' ') || activity.user?.username;
  }
}
