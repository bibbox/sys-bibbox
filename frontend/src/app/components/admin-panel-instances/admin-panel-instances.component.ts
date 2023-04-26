import { Component, OnInit } from '@angular/core';
import {InstanceItem} from '../../store/models/instance-item.model';
import {ThemePalette} from '@angular/material/core';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import * as instanceSelector from '../../store/selectors/instance.selector';
import {MatTableDataSource} from '@angular/material/table';


@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel-instances.component.html',
  styleUrls: ['./admin-panel-instances.component.scss']
})
export class AdminPanelInstancesComponent implements OnInit {
  instanceItems: InstanceItem[] = [];
  slideThemePalette: ThemePalette = 'primary';
  dataSource = new MatTableDataSource<InstanceItem>();

  constructor(private store: Store<AppState>) {
    this.store.pipe(select(instanceSelector.selectAllInstances)).subscribe((res) => {
      this.instanceItems = res;
      this.dataSource = new MatTableDataSource<InstanceItem>(this.instanceItems);
    });
  }

  ngOnInit(): void {
  }



  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

}
