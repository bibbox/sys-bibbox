import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {ActivityItem} from '../models/activity.model';
import {API_ACTIVITY_URL} from '../../commons';

@Injectable({
  providedIn: 'root'
})
export class ActivityService {

  constructor(private http: HttpClient) { }


  getActivities(): Observable<ActivityItem> {
    return this.http.get<ActivityItem>(API_ACTIVITY_URL);
  }

  getActivity(instanceUuid: string): Observable<ActivityItem> {
    return this.http.get<ActivityItem>(API_ACTIVITY_URL + instanceUuid);
  }
}
