import { Component, OnInit } from '@angular/core';
import {ApplicationGroupItem} from '../../store/models/application-group-item.model';
import {Store} from '@ngrx/store';
import {Observable} from 'rxjs';
import {AppState} from '../../store/models/app-state.model';
import {LoadApplicationGroupAction} from '../../store/actions/applications.actions';

@Component({
  selector: 'app-applications',
  templateUrl: './applications.component.html',
  styleUrls: ['./applications.component.scss']
})
export class ApplicationsComponent implements OnInit {
  applicationGroupItems$: Observable<Array<ApplicationGroupItem>>;
  loading$: Observable<boolean>;
  error$: Observable<Error>;

  constructor(private store: Store<AppState>) { }

  ngOnInit(): void {
    this.applicationGroupItems$ = this.store.select(store => store.applications.list);
    this.loading$ = this.store.select(store => store.applications.loading);
    this.error$ = this.store.select(store => store.applications.error);

    this.store.dispatch(new LoadApplicationGroupAction());
  }
}
