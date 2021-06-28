import {Component, OnDestroy, OnInit} from '@angular/core';
import {Observable} from 'rxjs';
import {InstanceItem} from '../../store/models/instance-item.model';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import {LoadInstancesAction} from '../../store/actions/instance.actions';
import * as instanceSelector from '../../store/selectors/instance.selector';
import * as applicationGroupSelector from '../../store/selectors/application-group.selector';

@Component({
  selector: 'app-instances',
  templateUrl: './instances.component.html',
  styleUrls: ['./instances.component.scss']
})
export class InstancesComponent implements OnInit {
  // instanceItems$: Observable<InstanceItem[]>;
  // loading$: Observable<boolean>;
  // error$: Observable<Error>;

  instanceItems: InstanceItem[] = [];

  constructor(private store: Store<AppState>) {
    this.store.pipe(select(instanceSelector.selectAllInstances)).subscribe((res) => this.instanceItems = res);
    // this.store.dispatch(new LoadInstancesAction()); // rm after websockets work
  }

  ngOnInit(): void {
    // this.instanceItems$ = this.store.pipe(select(instanceSelector.selectAllInstances));
    // this.loading$ = this.store.select(store => store.instances.loading);
    // this.error$ = this.store.select(store => store.instances.error);
  }

}
