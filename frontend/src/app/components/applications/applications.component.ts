import { Component, Inject, OnInit } from '@angular/core';
import {ApplicationGroupItem, ApplicationItem} from '../../store/models/application-group-item.model';
import * as applicationGroupSelector from '../../store/selectors/application-group.selector';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import {FormControl} from '@angular/forms';
import {filter} from 'rxjs/operators';
import {LoadApplicationGroupsAction} from '../../store/actions/applications.actions';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-applications',
  templateUrl: './applications.component.html',
  styleUrls: ['./applications.component.scss']
})

export class ApplicationsComponent implements OnInit {
  appGroups: ApplicationGroupItem[] = [];
  filteredAppGroups: ApplicationGroupItem[] = [];
  filterFormControl = new FormControl('');

  constructor(private store: Store<AppState>, @Inject(DOCUMENT) private document: Document) {
    this.store.dispatch(new LoadApplicationGroupsAction());

    this.store.pipe(select(applicationGroupSelector.loadApplicationGroups)).subscribe((res) => {
      this.appGroups = res.map(group => ({
        group_name: group.group_name,
        group_members: group.group_members.map(member => ({
          ...member,
          isNew: member.decoration === 'new',
          isFair: member.decoration === 'FAIR'
        }))
      }));

      this.filter('');
    });
  }

  ngOnInit(): void {
    this.document.body.classList.add('layout-width-wide');
  }

  ngOnDestroy(): void {
    this.document.body.classList.remove('layout-width-wide');
  }

  filter(newFilterValue: string): void {
    newFilterValue = newFilterValue.toLowerCase().trim();
    this.filteredAppGroups = [];
    this.appGroups.forEach((appGroup) => {
      const tempGroupItems = appGroup.group_members.filter((item) => {
        return !newFilterValue
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

