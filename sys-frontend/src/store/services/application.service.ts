import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Store} from '@ngrx/store';
import {ApplicationGroupItem} from '../models/application-group-item.model';
import {API_APPLICATIONS_URL} from '../../app/commons';
import {AddApplicationGroupAction} from '../actions/applications.actions';

@Injectable({
  providedIn: 'root'
})
export class ApplicationService {

  applicationsGroups: ApplicationGroupItem[];
  constructor(
    private http: HttpClient,
    private store: Store<{AppState}>) { }

  loadApplications(): void {
    this.http.get(API_APPLICATIONS_URL)
      .subscribe((applicationsGroups: ApplicationGroupItem[]) => {
        this.applicationsGroups = applicationsGroups;
        this.storeRetrievedApplications();
      });
  }

  storeRetrievedApplications(): void {
    console.log(this.applicationsGroups); // TODO: Remove in production
    for (const applicationGroup of this.applicationsGroups) {
      this.store.dispatch(new AddApplicationGroupAction(applicationGroup));
    }
  }

}
