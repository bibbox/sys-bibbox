import { Component, OnInit } from '@angular/core';
import {InstanceItem} from '../../store/models/instance-item.model';
import {ThemePalette} from '@angular/material/core';
import {select, Store} from '@ngrx/store';
import {AppState} from '../../store/models/app-state.model';
import * as instanceSelector from '../../store/selectors/instance.selector';
import {MatTableDataSource} from '@angular/material/table';
import {SVG_PATHS} from '../../commons';
import {environment} from '../../../environments/environment';
import {UserService} from '../../store/services/user.service';
import {InstanceService} from '../../store/services/instance.service';
import {FormControl} from '@angular/forms';


@Component({
  selector: 'app-admin-panel',
  templateUrl: './admin-panel-instances.component.html',
  styleUrls: ['./admin-panel-instances.component.scss']
})
export class AdminPanelInstancesComponent implements OnInit {
  instanceItems: InstanceItem[] = [];
  dataSource = new MatTableDataSource<InstanceItem>();
  svgPaths = SVG_PATHS;
  filterFormControl = new FormControl('');
  filteredInstances: InstanceItem[] = [];

  // displayedColumns: string[] = ['displayname_short', 'app.name', 'instancename', 'installed_by_id', 'installed_at', 'actions'];

  constructor(
    private store: Store<AppState>,
    private instanceService: InstanceService,

  ) {
    this.store.pipe(select(instanceSelector.selectAllInstances)).subscribe((res) => {
      this.instanceItems = res;
      this.filterInstances(this.filterFormControl.value);
    });
  }

  ngOnInit(): void {
  }

  filterInstances(newFilterValue: string): void {
    this.filteredInstances = this.instanceItems.filter((item) => {
      return !newFilterValue ||
        item.displayname_short.toLowerCase().indexOf(newFilterValue.toLowerCase()) !== -1 ||
        item.app.name.toLowerCase().indexOf(newFilterValue.toLowerCase()) !== -1 ||
        item.instancename.toLowerCase().indexOf(newFilterValue.toLowerCase()) !== -1;
    });
  }

  convertToDate(dateString: string): string {
    if (!dateString || dateString === '-') {
      return '';
    }
    let newDate = new Date(parseInt(dateString) * 1000);
    return newDate.toLocaleString("de-DE");
  }

  // logInstance(InstanceItem): void {
  //   console.log(InstanceItem);
  // }
  //
  // applyFilter(event: Event): void {
  //   const filterValue = (event.target as HTMLInputElement).value;
  //   this.dataSource.filter = filterValue.trim().toLowerCase();
  // }


  deleteInstance(instanceItem: InstanceItem): void {
    // const isAdmin = this.userService.isRole(KEYCLOAK_ROLES.admin);
    // const doesInstanceOwnerMatch = this.userService.getUserID() === this.instanceItem.installed_by;
    //
    // if (!(isAdmin || doesInstanceOwnerMatch)) {
    //   this.snackbar.open('You are not allowed to delete this instance', 'OK', {duration: 4000});
    //   return;
    // }

    this.instanceService.deleteInstance(instanceItem.instancename).subscribe(
      (res) => console.log(res)
    );
    this.instanceItems = this.instanceItems.filter((item) => item.instancename !== instanceItem.instancename);
  }

  manageInstance(instanceItem: InstanceItem, operation: string): void {
    this.instanceService.manageInstance(instanceItem.instancename, operation).subscribe((res) => console.log(res));
  }
}
