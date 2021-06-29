import { Component, OnInit } from '@angular/core';
import {ApplicationGroupItem, ApplicationItem} from '../../store/models/application-group-item.model';
import * as applicationGroupSelector from '../../store/selectors/application-group.selector';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import {FormControl} from '@angular/forms';

@Component({
  selector: 'app-applications',
  templateUrl: './applications.component.html',
  styleUrls: ['./applications.component.scss']
})

export class ApplicationsComponent implements OnInit {
  appGroups: ApplicationGroupItem[] = [];
  filteredAppGroups: ApplicationGroupItem[] = [];
  filterFormControl = new FormControl('');

  constructor(private store: Store<AppState>) {
    this.store.pipe(select(applicationGroupSelector.loadApplicationGroups)).subscribe((res) => {
      this.appGroups = res;
      this.filteredAppGroups = res;
    });
  }

  ngOnInit(): void {}

  filter(newFilterValue: string): void {
    newFilterValue = newFilterValue.toLowerCase().trim();
    this.filteredAppGroups = [];
    this.appGroups.forEach((appGroup) => {
      const tempGroupItems = appGroup.group_members.filter((item) => {
        return !newFilterValue
          || item.app_name.toLowerCase().indexOf(newFilterValue) !== -1
          || item.app_display_name.toLowerCase().indexOf(newFilterValue) !== -1
          || item.tags.some(value => value.toLowerCase().indexOf(newFilterValue) !== -1);
      });
      const tempGroup: ApplicationGroupItem = {group_name: appGroup.group_name, group_members: tempGroupItems};
      if (tempGroup.group_members.length) {
        this.filteredAppGroups.push(tempGroup);
      }
    });
  }
}

