import {Component, Input, OnInit} from '@angular/core';
import {InstanceItem} from '../../../store/models/instance-item.model';
import {Store} from '@ngrx/store';
import {AppState} from '../../../store/models/app-state.model';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-instance-detail-page',
  templateUrl: './instance-detail-page.component.html',
  styleUrls: ['./instance-detail-page.component.scss']
})
export class InstanceDetailPageComponent implements OnInit {
  instance$: Observable<InstanceItem>;
  constructor(private store: Store<AppState>) {}

  @Input() tabIndex: number;

  ngOnInit(): void {
    // this.instance$ = this.store.select(store => store.instances.list.filter(instanceName => 'wptest02'));
  }

  log(message: string): void {
    console.log(message);
  }
}
