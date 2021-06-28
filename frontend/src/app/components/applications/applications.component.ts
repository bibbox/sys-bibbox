import { Component, OnInit } from '@angular/core';
import {ApplicationGroupItem} from '../../store/models/application-group-item.model';
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
    this.store.pipe(select(applicationGroupSelector.loadApplications)).subscribe((res) => {
      this.appGroups = res;
      this.filter('');
    });
  }

  ngOnInit(): void {}

  filter(newFilterValue: string): void {
    // this.filteredAppGroups = this.appGroups.filter();
  }
}
