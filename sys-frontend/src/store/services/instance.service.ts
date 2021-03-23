import { Injectable } from '@angular/core';
import {API_INSTANCES_URL} from '../../app/commons';
import {HttpClient} from '@angular/common/http';
import {InstanceItem} from '../models/instance-item.model';
import {Store} from '@ngrx/store';
import {AddInstanceAction} from '../actions/instance.actions';

@Injectable({
  providedIn: 'root'
})
export class InstanceService {

  instanceItems: InstanceItem[];
  constructor(
    private http: HttpClient,
    private store: Store<{AppState}>) { }

  getAllInstances(): void {
    this.http.get(API_INSTANCES_URL)
      .subscribe((instanceItems: InstanceItem[]) => {
        this.instanceItems = instanceItems;
        this.storeRetrievedInstances();
      });
  }

  storeRetrievedInstances(): void {
    console.log(this.instanceItems); // TODO: Remove in production
    for (const instance of this.instanceItems) {
      this.store.dispatch(new AddInstanceAction(instance));
    }
  }

  // getInstanceByID() {
  // }
  //
  // postInstance() {
  //
  // }
  //
  // deleteInstanceByID {
  //
  // }
}
