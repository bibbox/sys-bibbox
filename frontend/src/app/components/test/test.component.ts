// import { Component, OnInit } from '@angular/core';
//
// @Component({
//   selector: 'app-test',
//   templateUrl: './test.component.html',
//   styleUrls: ['./test.component.scss']
// })
// export class TestComponent implements OnInit {
//
//   tags: [
//     {name: 'TEST-ADMIN', checked: false, color: 'primary', count: 5},
//     {name: 'TEST-ADMINISTRATION', checked: false, color: 'primary', count: 3 },
//     {name: 'TEST-BI', checked: false, color: 'primary', count: 3 },
//   ];
//
//   constructor() { }
//
//   ngOnInit(): void {
//   }
//
//   doNothing(tag): void {
//     console.log(tag);
//   }
//
// }
import {Component, OnInit} from '@angular/core';
import {select, Store} from '@ngrx/store';
import * as applicationGroupSelector from '../../store/selectors/application-group.selector';

export interface Tag {
  name: string;
  count: number;
}


@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})

export class TestComponent implements OnInit {
  sumTags = 12;
  tasks = [
    {name: 'Primary', checked: false, count: 2, facetBarStyle: { width: 2 / this.sumTags}},
    {name: 'Accent', checked: false, count: 3},
    {name: 'Warn', checked: false, count: 7}
  ];

  allComplete = false;

  constructor(private store: Store<{AppState}>) { }

  ngOnInit(): void {
    this.getAllTags();
  }

  getAllTags(): void {
    const appGroups = this.store.pipe(select(applicationGroupSelector.loadApplications));
    console.log(appGroups);
    appGroups.forEach(data => (
      console.log(data)
    )).then() ;
  }

  updateAllComplete(): any {
    this.allComplete = this.tasks != null && this.tasks.every(t => t.checked);
  }

  someComplete(): boolean {
    if (this.tasks == null) {
      return false;
    }
    return this.tasks.filter(t => t.checked).length > 0 && !this.allComplete;
  }

  setAll(completed: boolean): any {
    this.allComplete = completed;
    if (this.tasks == null) {
      return;
    }
    this.tasks.forEach(t => t.checked = completed);
  }

  log(tag): any {
    console.log(tag);
  }
}
