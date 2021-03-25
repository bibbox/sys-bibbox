import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Store} from '@ngrx/store';
import {ApplicationGroupItem} from '../models/application-group-item.model';
import {API_APPLICATIONS_URL} from '../../commons';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApplicationService {

  applicationsGroups: ApplicationGroupItem[];
  constructor(
    private http: HttpClient,
    private store: Store<{AppState}>) { }

  loadApplications(): Observable<ApplicationGroupItem[]> {
    return this.http.get<ApplicationGroupItem[]>(API_APPLICATIONS_URL);
  }

}
