import {Component, OnInit} from '@angular/core';
import {InstanceItem} from '../../store/models/instance-item.model';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import * as instanceSelector from '../../store/selectors/instance.selector';
import {FormControl} from '@angular/forms';

@Component({
  selector: 'app-instances',
  templateUrl: './instances.component.html',
  styleUrls: ['./instances.component.scss']
})
export class InstancesComponent implements OnInit {
  instanceItems: InstanceItem[] = [];
  filterFormControl = new FormControl('');
  filteredInstances: InstanceItem[] = [];

  constructor(private store: Store<AppState>) {
    this.store.pipe(select(instanceSelector.selectAllInstances)).subscribe((res) => {
      this.instanceItems = res;
      this.filteredInstances = res;
    });
  }

  ngOnInit(): void {
    // this.instanceItems$ = this.store.pipe(select(instanceSelector.selectAllInstances));
    // this.loading$ = this.store.select(store => store.instances.loading);
    // this.error$ = this.store.select(store => store.instances.error);
  }

  filter(newFilterValue: string): void {
    this.filteredInstances = this.instanceItems.filter((item) => {
      return !newFilterValue ||
        item.displayname_short.toLowerCase().indexOf(newFilterValue.toLowerCase()) !== -1 ||
        item.app.name.toLowerCase().indexOf(newFilterValue.toLowerCase()) !== -1 ||
        item.instancename.toLowerCase().indexOf(newFilterValue.toLowerCase()) !== -1;
    });
  }

}
