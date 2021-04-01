import { Component, OnInit } from '@angular/core';
import {ApplicationGroupItem} from '../../store/models/application-group-item.model';
import {Store} from '@ngrx/store';
import {Observable} from 'rxjs';
import {AppState} from '../../store/models/app-state.model';
import {LoadApplicationGroupsAction} from '../../store/actions/applications.actions';

@Component({
  selector: 'app-applications',
  templateUrl: './applications.component.html',
  styleUrls: ['./applications.component.scss']
})
export class ApplicationsComponent implements OnInit {
  applicationGroupItems$: Observable<Array<ApplicationGroupItem>>;
  // loading$: Observable<boolean>;
  // error$: Observable<Error>;

  tags: [
    {name: 'TEST-ADMIN', checked: false, color: 'primary', count: 5},
    {name: 'TEST-ADMINISTRATION', checked: false, color: 'primary', count: 3 },
    {name: 'TEST-BI', checked: false, color: 'primary', count: 3 },
  ];

  constructor(private store: Store<AppState>) { }

  ngOnInit(): void {
    this.store.dispatch(new LoadApplicationGroupsAction());

    this.applicationGroupItems$ = this.store.select(store => store.applicationGroups.list);
    // this.loading$ = this.store.select(store => store.applicationGroups.loading);
    // this.error$ = this.store.select(store => store.applicationGroups.error);
  }


  doNothing(): void {

  }
}
