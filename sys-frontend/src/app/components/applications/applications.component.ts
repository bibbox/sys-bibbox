import { Component, OnInit } from '@angular/core';
import {ApplicationGroupItem} from '../../../store/models/application-group-item.model';
import {Store} from '@ngrx/store';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-applications',
  templateUrl: './applications.component.html',
  styleUrls: ['./applications.component.scss']
})
export class ApplicationsComponent implements OnInit {
  applicationGroupItems$: Observable<Array<ApplicationGroupItem>>;
  constructor(private store: Store<{applications: Array<ApplicationGroupItem>}>) { }

  ngOnInit(): void {
    this.applicationGroupItems$ = this.store.select(store => store.applications);
  }
}
