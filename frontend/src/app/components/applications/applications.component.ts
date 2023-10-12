import { Component, Inject, OnInit } from '@angular/core';
import {ApplicationGroupItem} from '../../store/models/application-group-item.model';
import * as applicationGroupSelector from '../../store/selectors/application-group.selector';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import {FormControl} from '@angular/forms';
import {LoadApplicationGroupsAction} from '../../store/actions/applications.actions';
import { DOCUMENT } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-applications',
  templateUrl: './applications.component.html',
  styleUrls: ['./applications.component.scss']
})

export class ApplicationsComponent implements OnInit {
  appGroups: ApplicationGroupItem[] = [];
  filteredAppGroups: ApplicationGroupItem[] = [];
  searchFormControl = new FormControl('');
  filterFormControl = new FormControl('');
  sortFormControl = new FormControl('category');

  constructor(private store: Store<AppState>, @Inject(DOCUMENT) private document: Document, private dialog: MatDialog) {
  }

  ngOnInit(): void {
    this.document.body.classList.add('layout-width-wide');

    this.store.dispatch(new LoadApplicationGroupsAction());

    this.store.pipe(select(applicationGroupSelector.loadApplicationGroups)).subscribe((res) => {
      this.appGroups = res.map(group => ({
        group_name: group.group_name,
        group_members: group.group_members.map(member => ({
          ...member,
          isNew: typeof member.decoration === 'string' ? member.decoration === 'new' : member.decoration.includes('new'),
          isFair: typeof member.decoration === 'string' ? member.decoration === 'FAIR' : member.decoration.includes('FAIR')
        }))
      }));

      this.filter();
    });
  }

  ngOnDestroy(): void {
    this.document.body.classList.remove('layout-width-wide');
  }

  filter(): void {
    const searchterm = this.searchFormControl.value.toLowerCase().trim();
    const filter = this.filterFormControl.value;

    this.filteredAppGroups = [];
    
    this.appGroups.forEach((appGroup) => {
      const tempGroupItems = appGroup.group_members
        .filter((item) => !filter || (filter === 'new' && item.isNew) || (filter === 'FAIR' && item.isFair))
        .filter((item) => !searchterm || item.app_display_name.toLowerCase().indexOf(searchterm) !== -1 || item.tags.some(value => value.toLowerCase().indexOf(searchterm) !== -1));

      if(this.sortFormControl.value === 'category') {
        const tempGroup: ApplicationGroupItem = {group_name: appGroup.group_name, group_members: tempGroupItems};

        if (tempGroup.group_members.length) {
          this.filteredAppGroups.push(tempGroup);
        }
      }
      else if(this.sortFormControl.value === 'app') {
        if(this.filteredAppGroups.length === 0) {
          const tempGroup: ApplicationGroupItem = {group_name: appGroup.group_name, group_members: tempGroupItems, hideCategory: true};

          if (tempGroup.group_members.length) {
            this.filteredAppGroups.push(tempGroup);
          }
        }
        else if (tempGroupItems.length) {
          this.filteredAppGroups[0].group_members.push(...tempGroupItems);
        }
      }
    });

    if(this.sortFormControl.value === 'app') {
      this.filteredAppGroups[0].group_members = this.filteredAppGroups[0].group_members.sort((a, b) => {
        if(a.app_display_name.toLowerCase() < b.app_display_name.toLowerCase())
          return -1;
        else if(a.app_display_name.toLowerCase() > b.app_display_name.toLowerCase())
          return 1;

        return 0;
      });
    }
  }

  searchByTag = (tag: string) => {
    this.dialog?.closeAll();
    this.searchFormControl?.setValue(tag);
    this.filter();
  }
}

