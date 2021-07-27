import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {ActivityItem, LogItem} from '../models/activity.model';
import {API_ACTIVITY_URL} from '../../commons';
import {Store} from '@ngrx/store';
import {AppState} from '../models/app-state.model';
import {LoadActivitiesAction} from '../actions/activity.actions';

@Injectable({
  providedIn: 'root'
})
export class ActivityService {

  constructor(private http: HttpClient, private store: Store<AppState>) { }


  getActivities(): Observable<ActivityItem[]> {
    return this.http.get<ActivityItem[]>(API_ACTIVITY_URL);
  }

  getLogsOfActivity(activityID: number): Observable<LogItem[]> {
    return this.http.get<LogItem[]>(API_ACTIVITY_URL + 'logs/' + activityID);
  }

  getSysLogs(): Observable<JSON> {
    return this.http.get<JSON>(API_ACTIVITY_URL + '/syslogs');
  }

  refreshStoreActivities(): void {
    this.store.dispatch(new LoadActivitiesAction());
  }
}
