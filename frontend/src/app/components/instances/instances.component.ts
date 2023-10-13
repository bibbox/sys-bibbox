import {FormControl} from '@angular/forms';
import {Component, Inject, OnInit} from '@angular/core';
import {InstanceGroupItem, InstanceItem} from '../../store/models/instance-item.model';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import * as instanceSelector from '../../store/selectors/instance.selector';
import {UserService} from '../../store/services/user.service';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-instances',
  templateUrl: './instances.component.html',
  styleUrls: ['./instances.component.scss']
})
export class InstancesComponent implements OnInit {
  instanceItems: InstanceGroupItem[] = [
    { group_name: 'Running', group_members: [], hideCategory: false },
    { group_name: 'Error', group_members: [], hideCategory: false },
    { group_name: 'Stopped', group_members: [], hideCategory: false }
  ];
  filteredInstanceGroups: InstanceGroupItem[] = this.instanceItems;
  filteredInstanceList: InstanceItem[] = [];
  searchFormControl = new FormControl('');
  statusFormControl = new FormControl('');
  showOnlyOwnedInstances = new FormControl('false');
  showAsList = new FormControl('false');

  constructor(private store: Store<AppState>, private userService: UserService, @Inject(DOCUMENT) private document: Document) {
  }

  ngOnInit(): void {
    this.document.body.classList.add('layout-width-wide');

    this.store.pipe(select(instanceSelector.selectAllInstances)).subscribe((res) => {
      const list = res.sort((a, b) => {
        if(a.displayname_short?.toLowerCase() < b.displayname_short?.toLowerCase())
          return -1;
        else if(a.displayname_short?.toLowerCase() > b.displayname_short?.toLowerCase())
          return 1;

        return 0;
      });

      for(const group of this.instanceItems) {
        group.group_members = [];
      }

      for(const item of list) {
        const index = this.instanceItems.findIndex(group => group.group_name.toLowerCase() === item.state.toLowerCase());

        if(index >= 0) {
          this.instanceItems[index].group_members.push(item);
        }
      }

      this.filterInstances();
    });
  }

  ngOnDestroy(): void {
    this.document.body.classList.remove('layout-width-wide');
  }

  filterInstances(): void {
    let items = structuredClone(this.instanceItems);
    this.filteredInstanceList = [];

    for(let i = 0; i < items.length; i++) {
      items[i].group_members = items[i].group_members.filter(instance => this.instanceMatchesFilters(instance));
      this.filteredInstanceList.push(...items[i].group_members);
    }

    this.filteredInstanceGroups = items.filter(group => group.group_members.length > 0);
  }

  instanceMatchesFilters(instance: InstanceItem): boolean {
    const searchterm = this.searchFormControl.value;
    const status = this.statusFormControl.value;

    // Check if installer ID matches
    if(this.showOnlyOwnedInstances.value === 'true') {
      const userID = this.userService.getUserID();

      if(instance.installed_by_id !== userID) {
        return false;
      }
    }
    
    // Check if status filter matches
    if(!!status && instance.state !== status) {
      return false;
    }

    // Check if searchterm matches
    if(!instance.displayname_short?.toLowerCase().includes(searchterm.toLowerCase()) &&
      !instance.app.name?.toLowerCase().includes(searchterm.toLowerCase()) &&
      !instance.instancename?.toLowerCase().includes(searchterm.toLowerCase())) {

      return false;
    }

    return true;
  }
}
