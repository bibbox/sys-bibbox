import { Component, OnInit } from '@angular/core';
import {ApplicationGroupItem} from '../../store/models/application-group-item.model';
import * as applicationGroupActions from '../../store/actions/applications.actions';
import * as applicationGroupSelector from '../../store/selectors/application-group.selector';

import {select, Store} from '@ngrx/store';
import {Observable, pipe} from 'rxjs';
import {AppState} from '../../store/models/app-state.model';
import {group} from '@angular/animations';
import {Dictionary} from '@ngrx/entity';


interface ITag {
  name: string;
  count: number;
  checked: boolean;
}

@Component({
  selector: 'app-applications',
  templateUrl: './applications.component.html',
  styleUrls: ['./applications.component.scss']
})

export class ApplicationsComponent implements OnInit {
  applicationGroupItems$: Observable<ApplicationGroupItem[]> = this.store.pipe(select(applicationGroupSelector.loadApplications));
  // loading$: Observable<boolean>;
  // error$: Observable<Error>;

  // tags: [
  //   {name: 'TEST-ADMIN', checked: false, color: 'primary', count: 5},
  //   {name: 'TEST-ADMINISTRATION', checked: false, color: 'primary', count: 3 },
  //   {name: 'TEST-BI', checked: false, color: 'primary', count: 3 },
  // ];

  appGroups: Dictionary<ApplicationGroupItem> = {};
  tagsMap = new Map<string, number>();
  tagsArray: ITag[] = [];
  constructor(private store: Store<AppState>) { }

  ngOnInit(): void {
    this.store.dispatch(new applicationGroupActions.LoadApplicationGroupsAction());
    this.store.pipe(select(applicationGroupSelector.getApplications)).subscribe({
        next: res => {
          this.appGroups = res;
          this.getAllTags();
        }
      });
    }

  getAllTags(): void {
    for (const key in this.appGroups) {
      if (this.appGroups.hasOwnProperty(key)) {
        const currAppGroup = this.appGroups[key];
        for (const appName in currAppGroup.group_members) {
          if (currAppGroup.group_members.hasOwnProperty(appName)) {
            const tagsOfApp = currAppGroup.group_members[appName].tags;
            for (const tag of tagsOfApp) {
              if (this.tagsMap.has(tag)) {
                const tempTag = this.tagsMap.get(tag);
                this.tagsMap.set(tag, tempTag.valueOf() + 1 );
              } else {
                this.tagsMap.set(tag, 1);
              }
            }
          }
        }
      }
    }
    this.tagsMap.forEach((value, key) => this.tagsArray.push({name: key, count: value, checked: false}));
    this.tagsArray.sort((a, b) => a.name > b.name ? 1 : -1);
    this.tagsMap.clear();
  }

  doNothing(): void {
    const checkedTags = this.tagsArray.filter(tag => tag.checked === true);
    checkedTags.forEach(value => console.log(value.name));
  }
}
