import { Component, OnInit } from '@angular/core';
import {Observable} from 'rxjs';
import {InstanceItem} from '../../store/models/instance-item.model';
import {Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import {LoadInstancesAction} from '../../store/actions/instance.actions';

@Component({
  selector: 'app-instances',
  templateUrl: './instances.component.html',
  styleUrls: ['./instances.component.scss']
})
export class InstancesComponent implements OnInit {
  instanceItems$: Observable<Array<InstanceItem>>;
  loading$: Observable<boolean>;
  error$: Observable<Error>;

  constructor(private store: Store<AppState>) {}
  ngOnInit(): void {
    this.instanceItems$ = this.store.select(store => store.instances.list);
    this.loading$ = this.store.select(store => store.instances.loading);
    this.error$ = this.store.select(store => store.instances.error);

    this.store.dispatch(new LoadInstancesAction());
  }
}
