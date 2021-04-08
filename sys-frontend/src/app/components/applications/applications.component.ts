import { Component, OnInit } from '@angular/core';
import {ApplicationGroupItem} from '../../store/models/application-group-item.model';
import * as applicationGroupActions from '../../store/actions/applications.actions';
import * as applicationGroupSelector from '../../store/selectors/application-group.selector';

import {select, Store} from '@ngrx/store';
import {Observable} from 'rxjs';
import {AppState} from '../../store/models/app-state.model';

@Component({
  selector: 'app-applications',
  templateUrl: './applications.component.html',
  styleUrls: ['./applications.component.scss']
})
export class ApplicationsComponent implements OnInit {
  applicationGroupItems$: Observable<ApplicationGroupItem[]>;
  // loading$: Observable<boolean>;
  // error$: Observable<Error>;

  tags: [
    {name: 'TEST-ADMIN', checked: false, color: 'primary', count: 5},
    {name: 'TEST-ADMINISTRATION', checked: false, color: 'primary', count: 3 },
    {name: 'TEST-BI', checked: false, color: 'primary', count: 3 },
  ];

  constructor(private store: Store<AppState>) { }

  ngOnInit(): void {
    this.store.dispatch(new applicationGroupActions.LoadApplicationGroupsAction());

    this.applicationGroupItems$ = this.store.pipe(select(applicationGroupSelector.loadApplications));
  }


  doNothing(): void {

  }
}
