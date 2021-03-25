import { Component, OnInit } from '@angular/core';
import {Observable} from 'rxjs';
import {InstanceItem} from '../../store/models/instance-item.model';
import {Store} from '@ngrx/store';

@Component({
  selector: 'app-instances',
  templateUrl: './instances.component.html',
  styleUrls: ['./instances.component.scss']
})
export class InstancesComponent implements OnInit {
  instanceItems$: Observable<Array<InstanceItem>>;

  constructor(private store: Store<{instances: Array<InstanceItem>}>) {}
  ngOnInit(): void {
    this.instanceItems$ = this.store.select(store => store.instances);
  }
}
