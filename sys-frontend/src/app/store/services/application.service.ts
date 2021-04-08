import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {AppInfo, ApplicationGroupItem, EnvironmentParameters} from '../models/application-group-item.model';
import {API_APPLICATIONS_URL} from '../../commons';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApplicationService {

  constructor(private http: HttpClient) { }

  loadApplications(): Observable<ApplicationGroupItem[]> {
    return this.http.get<ApplicationGroupItem[]>(API_APPLICATIONS_URL);
  }

  getAppInfo(url: string): Observable<AppInfo> {
    return this.http.get<AppInfo>(url);
  }

  getAppEnvParams(url: string): Observable<EnvironmentParameters[]> {
    return this.http.get<EnvironmentParameters[]>(url);
  }
}
