import {Component, Inject, OnInit} from '@angular/core';
import {InstanceItem} from '../../store/models/instance-item.model';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import * as instanceSelector from '../../store/selectors/instance.selector';
import {FormControl} from '@angular/forms';
import {ThemePalette} from '@angular/material/core';
import {UserService} from '../../store/services/user.service';
import { DOCUMENT } from '@angular/common';

@Component({
  selector: 'app-instances',
  templateUrl: './instances.component.html',
  styleUrls: ['./instances.component.scss']
})
export class InstancesComponent implements OnInit {
  instanceItems: InstanceItem[] = [];
  filterFormControl = new FormControl('');
  filteredInstances: InstanceItem[] = [];
  slideThemePalette: ThemePalette = 'primary';
  showOnlyOwnedInstances = false;


  constructor(private store: Store<AppState>,
      private userService: UserService,
      @Inject(DOCUMENT) private document: Document
    ) {

    this.store.pipe(select(instanceSelector.selectAllInstances)).subscribe((res) => {
      this.instanceItems = res;
      this.filterInstances(this.filterFormControl.value);
    });
  }

  ngOnInit(): void {
    this.document.body.classList.add('layout-width-wide');
  }

  ngOnDestroy(): void {
    this.document.body.classList.remove('layout-width-wide');
  }

  filterInstances(newFilterValue: string): void {
    this.filteredInstances = this.instanceItems.filter((item) => {
      return !newFilterValue ||
        item.displayname_short.toLowerCase().indexOf(newFilterValue.toLowerCase()) !== -1 ||
        item.app.name.toLowerCase().indexOf(newFilterValue.toLowerCase()) !== -1 ||
        item.instancename.toLowerCase().indexOf(newFilterValue.toLowerCase()) !== -1;
    });

    // Filter only own instances
    if (this.showOnlyOwnedInstances) {
      const userID = this.userService.getUserID();
      this.filteredInstances = this.filteredInstances.filter((item) => {
        return item.installed_by_id === userID;
      });
    }
  }

  filterOnlyOwnInstances(): void {
    this.showOnlyOwnedInstances = !this.showOnlyOwnedInstances;
    this.filterInstances(this.filterFormControl.value);
  }

}
